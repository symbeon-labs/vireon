"""
Plugins para estender as funcionalidades do Research Packager.

Este módulo contém plugins que podem ser usados para personalizar o comportamento
do processador de pesquisas, incluindo:
- Processadores de formato personalizados
- Analisadores de dados customizados
- Geradores de relatório especializados
"""

from typing import Dict, Type, Any

registered_plugins: Dict[str, Type[Any]] = {}

def register_plugin(name: str, plugin_class: Type[Any]) -> None:
    """Registra um novo plugin no sistema."""
    registered_plugins[name] = plugin_class

def get_plugin(name: str) -> Type[Any]:
    """Recupera um plugin registrado pelo nome."""
    return registered_plugins.get(name)

