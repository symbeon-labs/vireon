# Warp Optimus — Guia de Uso Eficiente do Warp

> **Estado:** Experimental · **Versão:** 0.1.0

## Objetivo

Maximizar o impacto de cada chamada Warp e evitar desperdício de tarefas por
meio de cache local, simulação *dry-run* e políticas de throttle adaptativas.

---

## Princípios-chave

| Princípio               | Ação prática                                   |
|-------------------------|-----------------------------------------------|
| **Evitar Redundância**  | Consultar fingerprint/local-cache antes de pedir ao Warp |
| **Simular Primeiro**    | `vireon dry-run` sempre que possível          |
| **Memorizar Resultados**| Persistir saídas frequentes como embeddings   |
| **Modularizar Pedidos** | Converter sequências recorrentes em novas regras |

---

## Comandos rápidos

```bash
# Ativar modo otimizado
warp agent --optimize

# Analisar últimas chamadas e sugerir merges
warp logs --analyze

# Limitar uso a 10 chamadas/hora para este agente
warp agent --throttle 10/h
```

## Fluxo recomendado

- Dry-run local:
  - Execute: python core/vireon.py dry-run --rule-id optimize_warp_usage
  - O texto da requisição é convertido em hash semântico
- Consulta ao cache: se existir → retorna; se não → segue para Warp
- Pós-execução: o resultado vai para o cache e as métricas são atualizadas

Warp Optimus é parte do VIREON e foi pensado para evoluir: contribua com
adapters para outros back-ends ou melhorias de hash semântico!

---
