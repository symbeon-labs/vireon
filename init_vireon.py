#!/usr/bin/env python
"""Inicialização do VIREON"""

import sys
sys.path.append('.')

print("🚀 VIREON - Sistema de Consciência Evolutiva")
print("=" * 50)

try:
    # Importar módulos principais
    from core import consciousness, cognitive_engine, neural
    print("✅ Módulos core carregados")
    
    # Tentar inicializar o sistema de consciência
    print("\n📊 Inicializando Sistema de Consciência...")
    
    # Verificar se há uma classe principal
    if hasattr(consciousness, 'ConsciousnessSystem'):
        cs = consciousness.ConsciousnessSystem()
        print("✅ Sistema de Consciência inicializado")
    
    # Verificar cognitive engine
    if hasattr(cognitive_engine, 'CognitiveEngine'):
        print("✅ Motor Cognitivo disponível")
    
    # Listar funcionalidades disponíveis
    print("\n📋 Funcionalidades disponíveis:")
    
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
            
    print("\n✨ VIREON está pronto!")
    print("\nPara uma interface interativa, tente:")
    print("  python -m core")
    print("  python vireon_ui.py (se disponível)")
    
except Exception as e:
    print(f"❌ Erro ao inicializar: {e}")
    import traceback
    traceback.print_exc()
