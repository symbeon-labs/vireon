from datetime import datetime
from core.meta_governance import MetaGovernance, Rule, RuleType, Context

def main():
    # Inicializa o sistema de meta-governança
    governance = MetaGovernance("config/governance_config.yaml")
    
    # Cria uma regra de exemplo
    rule = Rule(
        id="RULE001",
        type=RuleType.COGNITIVE,
        description="Regra de adaptação linguística",
        parameters={
            "language_detection": True,
            "cultural_adaptation": True,
            "formality_level": "adaptive"
        },
        version="1.0.0",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    # Adiciona a regra ao sistema
    governance.add_rule(rule)
    
    # Define o contexto
    context = Context(
        environment={"platform": "warp", "mode": "interactive"},
        language="pt-BR",
        culture="BR",
        preferences={"formality": "casual", "technical_level": "intermediate"},
        constraints={"response_time": "real-time", "memory_usage": "efficient"}
    )
    
    # Ativa o contexto
    governance.set_context(context)
    
    # Exemplo de aplicação de regras
    input_data = {
        "user_message": "Como posso ajudar?",
        "user_profile": {"experience": "intermediate", "role": "developer"}
    }
    
    result = governance.apply_rules(input_data)
    print(f"Resultado da aplicação de regras: {result}")
    
    # Exemplo de feedback
    feedback = {
        "source": "user",
        "type": "explicit",
        "content": {
            "effectiveness": 0.9,
            "appropriateness": 0.85,
            "response_time": 0.95
        }
    }
    
    governance.adapt_rules(feedback)
    
    # Exibe métricas
    metrics = governance.get_metrics()
    print(f"Métricas do sistema: {metrics}")

if __name__ == "__main__":
    main()

