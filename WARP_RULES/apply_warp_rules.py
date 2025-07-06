"""
Script para aplicar e servir regras personalizadas ao agente Warp.
Inclui exportação, leitura reversa e API local opcional com FastAPI.
"""

import os
import json
import sys
from datetime import datetime

# Regras a serem aplicadas
RULES = {
    "version": "1.0.0",
    "created_at": str(datetime.now()),
    "rules": [
        {
            "name": "Tecnologias e Frameworks Preferidos",
            "content": """O usuário prefere as seguintes tecnologias e frameworks:
  - Framework Web Principal: FastAPI
  - Framework Frontend: Streamlit
  - Banco de Dados: PostgreSQL
  - Linguagem de Programação: Python
  - Containerização: Docker e docker-compose"""
        },
        {
            "name": "Estruturação de Projetos",
            "content": """O usuário segue estas convenções para estruturação de projetos:
  - Arquitetura modular (como em SAGE_HUB e AIDEN_PROJECT)
  - Separação frontend/backend (seguindo padrão ARKITECT)
  - Convenções de nomenclatura: snake_case para arquivos Python, PascalCase para classes, UPPERCASE para constantes
  - Estrutura de diretórios padrão: app, tests, docs, utils, modules, database"""
        },
        {
            "name": "Fluxos de Trabalho e Automação",
            "content": """O usuário utiliza os seguintes fluxos de trabalho:
  - Gestão de ambiente: sempre incluir ambientes virtuais Python (venv) e arquivos .env
  - Scripts de automação: .bat para Windows e .ps1 para PowerShell
  - Integração entre projetos: SAGE_HUB, AIDEN_PROJECT, ARKITECT
  - Versionamento: Git com .gitignore padronizado"""
        },
        {
            "name": "Projetos Ativos",
            "content": """Os projetos ativos do usuário são:
  - SAGE_HUB
  - AIDEN_PROJECT
  - ARKITECT
  - FYNDRAL
  Terminologia específica importante: "Mente Coletiva", "SAGE", "EON"
  Práticas de segurança: JWT, bcrypt"""
        },
        {
            "name": "Documentação e Comunicação",
            "content": """Preferências de documentação do usuário:
  - Formato: Markdown (.md)
  - Estrutura de respostas preferida: 
    1. Explicação conceitual
    2. Código de exemplo
    3. Considerações de implementação
  - Fazer referências cruzadas entre projetos relacionados quando relevante"""
        },
        {
            "name": "Bibliotecas Recomendadas",
            "content": """Bibliotecas preferidas do usuário por área:
  - Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, python-jose, passlib, psycopg2-binary, python-dotenv
  - Frontend: Streamlit, plotly, pandas, pyvis, streamlit-extras
  - Dados: pandas, numpy, scikit-learn, matplotlib, seaborn
  - Testes: pytest, pytest-cov, httpx, pytest-asyncio"""
        },
        {
            "name": "Templates de Projeto",
            "content": """O usuário tem preferência por estruturas de projetos específicas:
  - Projetos backend com FastAPI: estrutura modular com endpoints versionados
  - Projetos frontend com Streamlit: organização com pages/, components/ e utils/
  - Docker com configuração de desenvolvimento padronizada
  - Preferência por arquivos .env para configuração"""
        }
    ]
}

RULES_FILE = os.path.join(os.path.dirname(__file__), "warp_rules.json")

def save_rules_to_file():
    """
    Salva as regras definidas em um arquivo JSON para referência futura.
    """
    try:
        with open(RULES_FILE, "w", encoding="utf-8") as f:
            json.dump(RULES, f, ensure_ascii=False, indent=2)
        print(f"✅ Regras salvas com sucesso em: {RULES_FILE}")
        return RULES_FILE
    except Exception as e:
        print(f"❌ Erro ao salvar regras: {e}")
        return None

def load_rules_from_file():
    """
    Carrega regras salvas previamente do arquivo JSON.
    """
    if not os.path.exists(RULES_FILE):
        print("⚠️ Arquivo de regras não encontrado.")
        return None
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def display_rules_formatted(rules=None):
    """
    Exibe as regras formatadas no terminal.
    """
    rules = rules or RULES
    print("\n" + "=" * 80)
    print("📜 REGRAS FORMATADAS PARA O AGENTE WARP")
    print("=" * 80 + "\n")

    for i, rule in enumerate(rules["rules"], 1):
        print(f"🔹 REGRA {i}: {rule['name']}")
        print("-" * 50)
        print(rule['content'])
        print("\n" + "=" * 80 + "\n")

def main():
    """
    Executa o processo de gravação e exibição.
    """
    print("🚀 Iniciando configuração simbiótica do agente Warp...\n")
    save_rules_to_file()
    display_rules_formatted()
    print("👉 Para aplicar no Warp:")
    print("1. Acesse as configurações do seu agente Warp")
    print("2. Vá até a aba 'Rules' ou use um Notebook")
    print("3. Importe ou copie o conteúdo de warp_rules.json\n")

if __name__ == "__main__":
    sys.exit(main())

