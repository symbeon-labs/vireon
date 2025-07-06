"""
Sistema de Exportação de Métricas e Monitoramento do VIREON

Implementa:
- Formatadores de métricas (JSON, Prometheus)
- Endpoints de monitoramento
- Sistema de alertas
- Healthchecks
- Integração com CustomMetricsCollector
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
import aiohttp
from aiohttp import web
import prometheus_client as prom
from prometheus_client import Counter, Gauge, Histogram

from .superscope import CustomMetricsCollector, ContextualDimension

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Níveis de severidade de alertas"""
    INFO = auto()
    WARNING = auto()
    CRITICAL = auto()
    EMERGENCY = auto()

class MetricFormat(Enum):
    """Formatos suportados de exportação"""
    JSON = auto()
    PROMETHEUS = auto()
    OPENMETRICS = auto()

@dataclass
class AlertRule:
    """Regra de alerta para métricas"""
    name: str
    metric_key: str
    threshold: float
    severity: AlertSeverity
    condition: str  # '>', '<', '>=', '<=', '=='
    duration: timedelta = field(default_factory=lambda: timedelta(minutes=5))
    callback: Optional[Callable] = None
    last_triggered: Optional[datetime] = None
    is_active: bool = True

@dataclass
class Alert:
    """Alerta gerado pelo sistema"""
    rule_name: str
    severity: AlertSeverity
    metric_key: str
    current_value: float
    threshold: float
    timestamp: datetime = field(default_factory=datetime.now)
    dimensions: Set[str] = field(default_factory=set)

class MetricsExporter:
    """
    Exportador de métricas do VIREON.
    
    Implementa endpoints de monitoramento, formatação de métricas,
    sistema de alertas e healthchecks.
    
    Attributes:
        collector: Coletor de métricas customizado
        alert_rules: Regras de alerta configuradas
        active_alerts: Alertas atualmente ativos
        prometheus_metrics: Métricas registradas no Prometheus
    """
    
    def __init__(self, collector: CustomMetricsCollector):
        self.collector = collector
        self.alert_rules: List[AlertRule] = []
        self.active_alerts: List[Alert] = []
        
        # Métricas Prometheus
        self.prometheus_metrics = {
            "consciousness_depth": Gauge(
                "vireon_consciousness_depth",
                "Nível de profundidade de consciência"
            ),
            "symbiotic_coherence": Gauge(
                "vireon_symbiotic_coherence",
                "Nível de coerência simbiótica"
            ),
            "evolution_rate": Gauge(
                "vireon_evolution_rate",
                "Taxa de evolução do sistema"
            ),
            "transcendence_potential": Gauge(
                "vireon_transcendence_potential",
                "Potencial de transcendência"
            ),
            "quantum_operations": Counter(
                "vireon_quantum_operations_total",
                "Total de operações quânticas"
            ),
            "alert_count": Counter(
                "vireon_alerts_total",
                "Total de alertas gerados",
                ["severity"]
            ),
            "metrics_latency": Histogram(
                "vireon_metrics_latency_seconds",
                "Latência na coleta de métricas"
            )
        }
        
    async def setup_endpoints(self, app: web.Application):
        """Configura endpoints de monitoramento"""
        app.router.add_get("/metrics", self.handle_metrics)
        app.router.add_get("/health", self.handle_health)
        app.router.add_get("/status", self.handle_status)
        app.router.add_get("/alerts", self.handle_alerts)
        
    async def handle_metrics(self, request: web.Request) -> web.Response:
        """Handler para endpoint /metrics"""
        format_type = request.query.get("format", "prometheus")
        
        try:
            if format_type.lower() == "json":
                return web.json_response(await self.format_metrics_json())
            else:
                return web.Response(
                    text=await self.format_metrics_prometheus(),
                    content_type="text/plain"
                )
        except Exception as e:
            logger.error(f"Erro ao gerar métricas: {e}")
            return web.Response(status=500)
            
    async def handle_health(self, request: web.Request) -> web.Response:
        """Handler para healthcheck"""
        try:
            health_status = await self.check_health()
            return web.json_response(health_status)
        except Exception as e:
            logger.error(f"Erro no healthcheck: {e}")
            return web.Response(status=503)
            
    async def handle_status(self, request: web.Request) -> web.Response:
        """Handler para status detalhado"""
        try:
            status = await self.get_detailed_status()
            return web.json_response(status)
        except Exception as e:
            logger.error(f"Erro ao gerar status: {e}")
            return web.Response(status=500)
            
    async def handle_alerts(self, request: web.Request) -> web.Response:
        """Handler para listagem de alertas"""
        try:
            alerts = [
                {
                    "rule_name": alert.rule_name,
                    "severity": alert.severity.name,
                    "metric_key": alert.metric_key,
                    "current_value": alert.current_value,
                    "threshold": alert.threshold,
                    "timestamp": alert.timestamp.isoformat(),
                    "dimensions": list(alert.dimensions)
                }
                for alert in self.active_alerts
            ]
            return web.json_response(alerts)
        except Exception as e:
            logger.error(f"Erro ao listar alertas: {e}")
            return web.Response(status=500)
            
    async def format_metrics_json(self) -> Dict[str, Any]:
        """Formata métricas em JSON"""
        metrics = {}
        
        for metric_name, metric in self.prometheus_metrics.items():
            if isinstance(metric, Gauge):
                metrics[metric_name] = metric._value.get()
            elif isinstance(metric, Counter):
                metrics[metric_name] = metric._value.get()
                
        # Adicionar métricas agregadas
        aggregated = await self.collector.get_aggregated_metrics(
            window=timedelta(minutes=5)
        )
        metrics.update(aggregated)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "active_alerts": len(self.active_alerts)
        }
        
    async def format_metrics_prometheus(self) -> str:
        """Formata métricas no formato Prometheus"""
        return prom.generate_latest().decode()
        
    async def check_health(self) -> Dict[str, Any]:
        """Realiza verificação de saúde do sistema"""
        try:
            # Verificar componentes críticos
            collector_healthy = len(self.collector.metrics_buffer) > 0
            quantum_healthy = self.collector.neural_engine is not None
            
            status = "healthy" if (collector_healthy and quantum_healthy) else "degraded"
            
            return {
                "status": status,
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "metrics_collector": "healthy" if collector_healthy else "failing",
                    "neural_engine": "healthy" if quantum_healthy else "failing"
                }
            }
        except Exception as e:
            logger.error(f"Erro no healthcheck: {e}")
            return {
                "status": "failing",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
    async def get_detailed_status(self) -> Dict[str, Any]:
        """Retorna status detalhado do sistema"""
        try:
            # Coletar métricas recentes
            recent_metrics = await self.collector.get_aggregated_metrics(
                window=timedelta(minutes=15)
            )
            
            # Detectar anomalias
            anomalies = await self.collector.detect_anomalies()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "system_status": await self.check_health(),
                "recent_metrics": recent_metrics,
                "active_alerts": len(self.active_alerts),
                "detected_anomalies": len(anomalies),
                "metrics_collection_rate": len(self.collector.metrics_buffer) / self.collector.buffer_size
            }
        except Exception as e:
            logger.error(f"Erro ao gerar status detalhado: {e}")
            return {"status": "error", "message": str(e)}
            
    async def add_alert_rule(self, rule: AlertRule):
        """Adiciona nova regra de alerta"""
        self.alert_rules.append(rule)
        logger.info(f"Regra de alerta adicionada: {rule.name}")
        
    async def check_alert_rules(self, dimension: ContextualDimension):
        """Verifica regras de alerta para uma dimensão"""
        metrics = await self.collector.collect_metrics(dimension)
        
        for rule in self.alert_rules:
            if not rule.is_active:
                continue
                
            current_value = metrics.get(rule.metric_key)
            if current_value is None:
                continue
                
            condition_met = False
            if rule.condition == ">":
                condition_met = current_value > rule.threshold
            elif rule.condition == "<":
                condition_met = current_value < rule.threshold
            elif rule.condition == ">=":
                condition_met = current_value >= rule.threshold
            elif rule.condition == "<=":
                condition_met = current_value <= rule.threshold
            elif rule.condition == "==":
                condition_met = abs(current_value - rule.threshold) < 1e-6
                
            if condition_met:
                if not rule.last_triggered or \
                   (datetime.now() - rule.last_triggered) >= rule.duration:
                    await self._trigger_alert(rule, current_value, dimension)
                    
    async def _trigger_alert(
        self,
        rule: AlertRule,
        current_value: float,
        dimension: ContextualDimension
    ):
        """Dispara um alerta"""
        alert = Alert(
            rule_name=rule.name,
            severity=rule.severity,
            metric_key=rule.metric_key,
            current_value=current_value,
            threshold=rule.threshold,
            dimensions={str(dimension.id)}
        )
        
        self.active_alerts.append(alert)
        rule.last_triggered = datetime.now()
        
        # Incrementar contador Prometheus
        self.prometheus_metrics["alert_count"].labels(
            severity=rule.severity.name.lower()
        ).inc()
        
        # Executar callback se existir
        if rule.callback:
            try:
                await rule.callback(alert)
            except Exception as e:
                logger.error(f"Erro no callback de alerta: {e}")
                
        logger.warning(
            f"Alerta disparado: {rule.name} "
            f"({rule.metric_key} = {current_value}, "
            f"threshold = {rule.threshold})"
        )
        
    async def cleanup_old_alerts(self, max_age: timedelta = timedelta(hours=24)):
        """Remove alertas antigos"""
        now = datetime.now()
        self.active_alerts = [
            alert for alert in self.active_alerts
            if now - alert.timestamp < max_age
        ]
        
# Exemplo de uso
async def setup_metrics_exporter(
    app: web.Application,
    collector: CustomMetricsCollector
):
    """Configura e inicializa o exportador de métricas"""
    exporter = MetricsExporter(collector)
    
    # Configurar regras de alerta padrão
    await exporter.add_alert_rule(
        AlertRule(
            name="high_consciousness",
            metric_key="consciousness_depth",
            threshold=0.9,
            severity=AlertSeverity.WARNING,
            condition=">=",
            duration=timedelta(minutes=10)
        )
    )
    
    await exporter.add_alert_rule(
        AlertRule(
            name="low_coherence",
            metric_key="symbiotic_coherence",
            threshold=0.3,
            severity=AlertSeverity.CRITICAL,
            condition="<",
            duration=timedelta(minutes=5)
        )
    )
    
    # Configurar endpoints
    await exporter.setup_endpoints(app)
    
    # Cleanup periódico de alertas
    asyncio.create_task(
        periodic_alert_cleanup(exporter)
    )
    
    return exporter

async def periodic_alert_cleanup(exporter: MetricsExporter):
    """Task para limpeza periódica de alertas antigos"""
    while True:
        await asyncio.sleep(3600)  # 1 hora
        await exporter.cleanup_old_alerts()

