#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Analisador de Terminologia Simplificado para VIREON"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Termos problemáticos e suas substituições
PROBLEMATIC_TERMS = {
    'neural': 'algorítmico/neural/avançado',
    'neural_process': 'processo_neural',
    'symbiotic_enhancement': 'aprimoramento_simbiótico',
    'adaptive_learning': 'aprendizado_adaptativo',
    'system_state': 'estado_do_sistema',
    'symbiotic_validation': 'validação_simbiótica',
    'metacognitive_awareness': 'consciência_metacognitiva',
    'neural_layer': 'camada_neural',
    'computational_field': 'campo_computacional',
    'symbiotic_bridge': 'ponte_simbiótica',
    'Neuralprocessor': 'ProcessadorNeural',
    'adaptive_supervisor': 'supervisor_adaptativo'
}

# Padrões para ignorar (comentários sobre o problema)
IGNORE_PATTERNS = [
    r'#.*neural.*problema',
    r'#.*substituir.*neural',
    r'""".*evitar.*neural.*"""',
    r"'''.*evitar.*neural.*'''"
]

def analyze_file(filepath):
    """Analisa um arquivo em busca de termos problemáticos"""
    violations = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # Pular linhas que são sobre o problema
            if any(re.search(pattern, line, re.IGNORECASE) for pattern in IGNORE_PATTERNS):
                continue
                
            # Procurar por termos problemáticos
            for term, replacement in PROBLEMATIC_TERMS.items():
                if re.search(r'\b' + term + r'\b', line, re.IGNORECASE):
                    violations.append({
                        'file': filepath,
                        'line': line_num,
                        'term': term,
                        'context': line.strip(),
                        'suggestion': replacement
                    })
    except Exception as e:
        pass
    
    return violations

def analyze_project(root_path):
    """Analisa todo o projeto"""
    all_violations = []
    files_analyzed = 0
    
    for root, dirs, files in os.walk(root_path):
        # Ignorar diretórios específicos
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'node_modules']]
        
        for file in files:
            if file.endswith(('.py', '.md', '.txt', '.yml', '.yaml')):
                filepath = os.path.join(root, file)
                violations = analyze_file(filepath)
                all_violations.extend(violations)
                files_analyzed += 1
    
    return all_violations, files_analyzed

def main():
    print("=" * 70)
    print("ANÁLISE DE TERMINOLOGIA - VIREON")
    print("=" * 70)
    
    # Analisar o projeto
    project_root = Path(__file__).parent.parent
    violations, files_analyzed = analyze_project(project_root)
    
    print(f"\n📊 Estatísticas:")
    print(f"  Arquivos analisados: {files_analyzed}")
    print(f"  Violações encontradas: {len(violations)}")
    
    if violations:
        print("\n⚠️  VIOLAÇÕES DE TERMINOLOGIA ENCONTRADAS:")
        print("-" * 70)
        
        # Agrupar por arquivo
        by_file = defaultdict(list)
        for v in violations:
            by_file[v['file']].append(v)
        
        # Mostrar apenas os primeiros 10 arquivos
        for i, (filepath, file_violations) in enumerate(list(by_file.items())[:10]):
            rel_path = os.path.relpath(filepath, project_root)
            print(f"\n📄 {rel_path}")
            
            for v in file_violations[:3]:  # Máximo 3 por arquivo
                print(f"  Linha {v['line']}: '{v['term']}' → '{v['suggestion']}'")
                print(f"    Contexto: {v['context'][:60]}...")
            
            if len(file_violations) > 3:
                print(f"    ... e mais {len(file_violations) - 3} violações")
        
        if len(by_file) > 10:
            print(f"\n... e mais {len(by_file) - 10} arquivos com violações")
        
        # Resumo por termo
        print("\n📈 Resumo por termo:")
        term_count = defaultdict(int)
        for v in violations:
            term_count[v['term']] += 1
        
        for term, count in sorted(term_count.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  '{term}': {count} ocorrências")
    else:
        print("\n✅ Nenhuma violação de terminologia encontrada!")
    
    print("\n" + "=" * 70)
    print("💡 Recomendação: Execute correções automáticas com --fix")
    print("=" * 70)

if __name__ == "__main__":
    main()
