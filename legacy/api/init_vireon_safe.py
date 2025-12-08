#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Inicialização do VIREON"""

import sys
import os
sys.path.append('.')

# Configurar encoding para UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("VIREON - Sistema de Consciencia Evolutiva")
print("=" * 50)

try:
    # Importar módulos principais
    from core import consciousness, cognitive_engine, neural
    print("[OK] Modulos core carregados")
    
    # Tentar inicializar o sistema de consciência
    print("\nInicializando Sistema de Consciencia...")
    
    # Verificar se há uma classe principal
    if hasattr(consciousness, 'ConsciousnessSystem'):
        cs = consciousness.ConsciousnessSystem()
        print("[OK] Sistema de Consciencia inicializado")
    
    # Verificar cognitive engine
    if hasattr(cognitive_engine, 'CognitiveEngine'):
        print("[OK] Motor Cognitivo disponivel")
    
    # Listar funcionalidades disponíveis
    print("\nFuncionalidades disponiveis:")
    
    modules = {
        'consciousness': consciousness,
        'cognitive_engine': cognitive_engine,
        'neural': neural
    }
    
    for name, module in modules.items():
        print(f"\n  {name}:")
        attrs = [attr for attr in dir(module) if not attr.startswith('_')]
        for attr in attrs[:5]:  # Mostrar apenas os primeiros 5
            print(f"    - {attr}")
            
    print("\nVIREON esta pronto!")
    print("\nPara uma interface interativa, tente:")
    print("  python -m core")
    
except Exception as e:
    print(f"[ERRO] Erro ao inicializar: {e}")
    import traceback
    traceback.print_exc()
