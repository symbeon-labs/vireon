#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Corretor de Terminologia para VIREON - Remove termos 'neural'"""

import os
import re
from pathlib import Path

# Mapeamento de correções
CORRECTIONS = {
    'neural': 'neural',
    'neural_process': 'neural_process',
    'symbiotic_enhancement': 'symbiotic_enhancement',
    'adaptive_learning': 'adaptive_learning',
    'system_state': 'system_state',
    'symbiotic_validation': 'symbiotic_validation',
    'metacognitive_awareness': 'metacognitive_awareness',
    'neural_layer': 'neural_layer',
    'computational_field': 'computational_field',
    'symbiotic_bridge': 'symbiotic_bridge',
    'Neuralprocessor': 'NeuralProcessor',
    'adaptive_supervisor': 'adaptive_supervisor',
    'neural_core': 'neural_core',
    'neural_engine': 'neural_engine',
    'Symbioticbridge': 'SymbioticBridge',
    'system_level': 'system_level'
}

def correct_file(filepath, dry_run=True):
    """Corrige um arquivo"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Aplicar correções
        for old_term, new_term in CORRECTIONS.items():
            # Regex para palavra completa
            pattern = r'\b' + re.escape(old_term) + r'\b'
            
            # Contar ocorrências
            occurrences = len(re.findall(pattern, content, re.IGNORECASE))
            
            if occurrences > 0:
                # Substituir preservando maiúsculas/minúsculas
                def replace_func(match):
                    matched = match.group()
                    if matched.isupper():
                        return new_term.upper()
                    elif matched[0].isupper():
                        return new_term.capitalize()
                    else:
                        return new_term
                
                content = re.sub(pattern, replace_func, content, flags=re.IGNORECASE)
                changes_made.append(f"{old_term} -> {new_term} ({occurrences}x)")
        
        if changes_made and content != original_content:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
            return True, changes_made
        
        return False, []
        
    except Exception as e:
        print(f"Erro em {filepath}: {e}")
        return False, []

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Corretor de Terminologia VIREON')
    parser.add_argument('--fix', action='store_true', help='Aplicar correções (sem esta flag, apenas mostra o que seria corrigido)')
    parser.add_argument('--path', default='.', help='Caminho para analisar')
    args = parser.parse_args()
    
    print("=" * 70)
    print("CORRETOR DE TERMINOLOGIA - VIREON")
    print("=" * 70)
    print(f"Modo: {'CORREÇÃO' if args.fix else 'SIMULAÇÃO (use --fix para aplicar)'}")
    print("=" * 70)
    
    total_files = 0
    files_with_changes = 0
    
    for root, dirs, files in os.walk(args.path):
        # Ignorar diretórios
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'node_modules']]
        
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.yml', '.yaml')):
                filepath = os.path.join(root, file)
                changed, changes = correct_file(filepath, dry_run=not args.fix)
                
                if changed:
                    rel_path = os.path.relpath(filepath, args.path)
                    print(f"\n📄 {rel_path}")
                    for change in changes:
                        print(f"   {change}")
                    files_with_changes += 1
                
                total_files += 1
    
    print(f"\n{'=' * 70}")
    print(f"📊 Resumo:")
    print(f"   Arquivos analisados: {total_files}")
    print(f"   Arquivos com mudanças: {files_with_changes}")
    
    if not args.fix and files_with_changes > 0:
        print(f"\n⚠️  Execute com --fix para aplicar as correções")
    elif args.fix and files_with_changes > 0:
        print(f"\n✅ Correções aplicadas com sucesso!")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
