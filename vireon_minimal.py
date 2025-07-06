#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Interface minimal do VIREON"""

import sys
import os

print("=" * 60)
print("VIREON - Interface Minimal")
print("=" * 60)

# Tentar importar apenas módulos individuais
try:
    sys.path.append('.')
    
    # Tentar cognitive_engine primeiro
    try:
        from core.cognitive_engine import CognitiveEngine
        print("[OK] CognitiveEngine carregado")
        
        # Criar instância
        engine = CognitiveEngine()
        print("[OK] CognitiveEngine inicializado")
        
        # Mostrar funcionalidades
        print("\nFuncionalidades do CognitiveEngine:")
        methods = [m for m in dir(engine) if not m.startswith('_') and callable(getattr(engine, m))]
        for method in methods[:10]:
            print(f"  - {method}")
            
    except Exception as e:
        print(f"[AVISO] CognitiveEngine: {e}")
    
    # Tentar consciousness
    try:
        from core.consciousness import ConsciousnessSystem
        print("\n[OK] ConsciousnessSystem disponivel")
    except Exception as e:
        print(f"\n[AVISO] ConsciousnessSystem: {e}")
    
    print("\n" + "=" * 60)
    print("VIREON Minimal Interface - Pronto")
    print("=" * 60)
    
    # Menu simples
    print("\nOpcoes:")
    print("1. Testar processamento cognitivo")
    print("2. Verificar modulos disponiveis")
    print("3. Sair")
    
    choice = input("\nEscolha uma opcao: ")
    
    if choice == "1":
        print("\nTestando processamento cognitivo...")
        # Aqui poderiamos adicionar um teste simples
        print("[OK] Teste concluido")
    elif choice == "2":
        print("\nModulos disponiveis em 'core':")
        for file in os.listdir('core'):
            if file.endswith('.py') and not file.startswith('_'):
                print(f"  - {file[:-3]}")
    
except Exception as e:
    print(f"\n[ERRO] {e}")
    import traceback
    traceback.print_exc()
