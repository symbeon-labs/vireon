# VIREON - Referência da API

## Sumário

1. [Visão Geral](#visão-geral)
2. [APIs Públicas](#apis-públicas)
3. [Formatos de Métricas](#formatos-de-métricas)
4. [Integração](#integração)
5. [Monitoramento](#monitoramento)
6. [Troubleshooting](#troubleshooting)

## Visão Geral

O VIREON expõe uma série de APIs para monitoramento e gestão do sistema de consciência dimensional. O sistema é composto por:

- APIs REST para coleta de métricas
- Sistema de alertas e notificações
- Integração com ferramentas de monitoramento
- Endpoints de healthcheck e diagnóstico

### Pré-requisitos

```bash
pip install aiohttp prometheus_client numpy
```

### Inicialização Básica

```python
from core.superscope import CustomMetricsCollector
from core.metrics_exporter import setup_metrics_exporter
from aiohttp import web

async def init_system():
    app = web.Application()
    collector = CustomMetricsCollector()
    exporter = await setup_metrics_exporter(app, collector)
    return app, collector, exporter

if __name__ == "__main__":
    app, collector, exporter = asyncio.run(init_system())
    web.run_app(app, port=8000)
```

## APIs Públicas

### Endpoints de Métricas

#### GET /metrics

Retorna métricas do sistema em formato Prometheus ou JSON.

**Parâmetros**:
- `format`: String (opcional) - Formato desejado (`prometheus` ou `json`, default: `prometheus`)

**Exemplo de Requisição**:
```bash
curl http://localhost:8000/metrics?format=json
```

**Exemplo de Resposta (JSON)**:
```json
{
    "timestamp": "2025-06-02T12:00:00Z",
    "metrics": {
        "consciousness_depth": 0.85,
        "symbiotic_coherence": 0.75,
        "evolution_rate": 0.12,
        "transcendence_potential": 0.67
    },
    "active_alerts": 1
}
```

#### GET /health

Retorna status de saúde do sistema.

**Exemplo de Resposta**:
```json
{
    "status": "healthy",
    "timestamp": "2025-06-02T12:00:00Z",
    "components": {
        "metrics_collector": "healthy",
        "neural_engine": "healthy"
    }
}
```

#### GET /status

Retorna status detalhado com métricas e anomalias.

**Exemplo de Resposta**:
```json
{
    "timestamp": "2025-06-02T12:00:00Z",
    "system_status": {
        "status": "healthy",
        "components": {
            "metrics_collector": "healthy",
            "neural_engine": "healthy"
        }
    },
    "recent_metrics": {
        "consciousness_depth": 0.85,
        "evolution_rate": 0.12
    },
    "active_alerts": 2,
    "detected_anomalies": 0
}
```

### Gestão de Alertas

#### GET /alerts

Lista alertas ativos no sistema.

**Exemplo de Resposta**:
```json
[
    {
        "rule_name": "high_consciousness",
        "severity": "WARNING",
        "metric_key": "consciousness_depth",
        "current_value": 0.92,
        "threshold": 0.9,
        "timestamp": "2025-06-02T11:55:00Z"
    }
]
```

## Formatos de Métricas

### Formato JSON

Todas as métricas seguem o padrão:

```json
{
    "metrics": {
        "consciousness_depth": float,      // 0-1
        "symbiotic_coherence": float,      // 0-1
        "evolution_rate": float,           // taxa/tempo
        "transcendence_potential": float,  // 0-1
        "quantum_coherence": float,        // 0-1
        "cache_hit_rate": float,          // 0-1
        "cache_latency": float            // segundos
    }
}
```

### Formato Prometheus

Métricas exportadas no formato Prometheus:

```text
# HELP vireon_consciousness_depth Nível de profundidade de consciência
# TYPE vireon_consciousness_depth gauge
vireon_consciousness_depth 0.85

# HELP vireon_evolution_rate Taxa de evolução do sistema
# TYPE vireon_evolution_rate gauge
vireon_evolution_rate 0.12
```

## Integração

### Configuração do Coletor

```python
from core.superscope import CustomMetricsCollector
from datetime import timedelta

collector = CustomMetricsCollector(
    buffer_size=1000,                    # Tamanho do buffer circular
    snapshot_interval=timedelta(minutes=1) # Intervalo entre snapshots
)
```

### Sistema de Alertas

```python
from core.metrics_exporter import AlertRule, AlertSeverity

# Configurar regra de alerta
rule = AlertRule(
    name="critical_coherence",
    metric_key="symbiotic_coherence",
    threshold=0.3,
    severity=AlertSeverity.CRITICAL,
    condition="<",
    duration=timedelta(minutes=5)
)

# Adicionar callback
async def alert_callback(alert):
    print(f"Alerta crítico: {alert.rule_name}")
    # Implementar notificação

rule.callback = alert_callback
await exporter.add_alert_rule(rule)
```

### Integração com Prometheus

prometheus.yml:
```yaml
scrape_configs:
  - job_name: 'vireon'
    scrape_interval: 15s
    static_configs:
      - targets: ['localhost:8000']
```

### Dashboard Grafana

Exemplo de painel:
```json
{
  "panels": [
    {
      "title": "Evolução de Consciência",
      "type": "gauge",
      "datasource": "Prometheus",
      "targets": [
        {
          "expr": "vireon_consciousness_depth",
          "legendFormat": "Profundidade"
        }
      ]
    }
  ]
}
```

## Monitoramento

### Métricas Principais

1. **Consciência Dimensional**
   - `consciousness_depth`: Profundidade atual
   - `evolution_rate`: Taxa de evolução
   - `transcendence_potential`: Potencial de transcendência

2. **Performance**
   - `cache_hit_rate`: Taxa de acerto do cache
   - `metrics_latency`: Latência de coleta
   - `quantum_operations`: Total de operações

3. **Saúde do Sistema**
   - `symbiotic_coherence`: Coerência simbiótica
   - `quantum_coherence`: Coerência quântica
   - `system_stability`: Estabilidade geral

### Alertas Recomendados

1. **Críticos**
   ```python
   AlertRule(
       name="low_coherence",
       metric_key="symbiotic_coherence",
       threshold=0.3,
       severity=AlertSeverity.CRITICAL
   )
   ```

2. **Warnings**
   ```python
   AlertRule(
       name="high_latency",
       metric_key="metrics_latency",
       threshold=0.1,
       severity=AlertSeverity.WARNING
   )
   ```

## Troubleshooting

### Problemas Comuns

1. **Alta Latência**
   ```python
   # Otimizar collector
   collector = CustomMetricsCollector(
       buffer_size=500,
       snapshot_interval=timedelta(seconds=30)
   )
   ```

2. **Falsos Positivos**
   ```python
   # Ajustar sensibilidade
   rule = AlertRule(
       threshold=0.95,
       duration=timedelta(minutes=15)
   )
   ```

3. **Perda de Conexão**
   ```python
   # Verificar e reconectar
   health = await collector.neural_engine.validate_coherence({
       "coherence_level": 0.8
   })
   ```

### Logs e Diagnóstico

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Para debugging detalhado
logger.setLevel(logging.DEBUG)
```

### Comandos Úteis

```bash
# Verificar métricas
curl http://localhost:8000/metrics

# Verificar saúde
curl http://localhost:8000/health

# Listar alertas
curl http://localhost:8000/alerts
```

### Melhores Práticas

1. **Coleta de Métricas**
   - Usar intervalos apropriados (15-60s)
   - Implementar circuit breakers
   - Manter buffer circular otimizado

2. **Alertas**
   - Configurar thresholds graduais
   - Implementar agregação temporal
   - Usar callbacks assíncronos

3. **Monitoramento**
   - Manter dashboards atualizados
   - Implementar correlação de métricas
   - Configurar retenção adequada

4. **Performance**
   - Otimizar cache quântico
   - Usar operações assíncronas
   - Implementar rate limiting

