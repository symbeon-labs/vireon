#!/usr/bin/env python
"""Script de teste para VIREON"""

try:
    print("🚀 Testando VIREON...")
    print("=" * 40)
    
    # Tentar importar módulos principais
    try:
        import core
        print("✅ Módulo 'core' importado")
    except:
        print("❌ Erro ao importar 'core'")
    
    try:
        from src import adaptive_supervisor
        print("✅ Módulo 'adaptive_supervisor' importado")
    except:
        print("❌ Erro ao importar 'adaptive_supervisor'")
        
    print("\n📋 Módulos Python disponíveis:")
    import os
    for item in os.listdir('.'):
        if os.path.isdir(item) and os.path.exists(os.path.join(item, '__init__.py')):
            print(f"  - {item}")
            
except Exception as e:
    print(f"❌ Erro: {e}")
