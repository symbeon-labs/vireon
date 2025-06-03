use std::sync::Arc;
use tokio::sync::Mutex;
use metrics::{counter, gauge, histogram};
use tracing::{info, warn, error, debug};
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use anyhow::{Result, Context};
use async_trait::async_trait;
use ndarray::Array2;
use std::collections::VecDeque;
use std::time::Duration;

/// Configuração do monitor do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MonitorConfig {
    /// Intervalo de coleta de métricas (ms)
    pub collection_interval: u64,
    
    /// Tamanho do histórico de métricas
    pub history_size: usize,
    
    /// Limiares para alertas
    pub alert_thresholds: AlertThresholds,
    
    /// Configurações de análise
    pub analysis_config: AnalysisConfig,
}

/// Limiares para geração de alertas
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AlertThresholds {
    /// Variação máxima aceitável
    pub max_variance: f64,
    
    /// Taxa mínima de sucesso
    pub min_success_rate: f64,
    
    /// Tempo máximo entre validações
    pub max_validation_interval: Duration,
}

/// Configurações de análise
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnalysisConfig {
    /// Janela de análise de tendências
    pub trend_window: usize,
    
    /// Limiar para detecção de anomalias
    pub anomaly_threshold: f64,
    
    /// Intervalo de geração de relatórios
    pub report_interval: Duration,
}

/// Métricas básicas do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MonitoringMetrics {
    // Métricas básicas
    pub quantum_coherence: f64,
    pub consciousness_level: f64,
    pub transcendence_readiness: f64,
    
    // Métricas de tendência
    pub coherence_trend: Vec<f64>,
    pub consciousness_trend: Vec<f64>,
    pub transcendence_trend: Vec<f64>,
    
    // Métricas de performance
    pub validation_success_rate: f64,
    pub avg_validation_duration_ms: f64,
    pub last_validation: DateTime<Utc>,
    
    // Métricas de estabilidade
    pub system_stability: f64,
    pub error_rate: f64,
    pub recovery_rate: f64,
}

/// Estado atual do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemState {
    /// Métricas atuais
    pub current_metrics: MonitoringMetrics,
    
    /// Histórico de métricas
    pub metrics_history: VecDeque<MonitoringMetrics>,
    
    /// Alertas ativos
    pub active_alerts: Vec<SystemAlert>,
    
    /// Estado da análise
    pub analysis_state: AnalysisState,
}

/// Estado da análise do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnalysisState {
    /// Tendências detectadas
    pub trends: TrendAnalysis,
    
    /// Anomalias detectadas
    pub anomalies: Vec<AnomalyReport>,
    
    /// Última análise
    pub last_analysis: DateTime<Utc>,
}

/// Monitor do sistema
pub struct SystemMonitor {
    /// Estado do monitor
    state: Arc<Mutex<SystemState>>,
    
    /// Configuração
    config: MonitorConfig,
    
    /// Canal de alertas
    alert_tx: tokio::sync::mpsc::Sender<SystemAlert>,
}

impl SystemMonitor {
    /// Cria nova instância do monitor
    pub fn new(config: MonitorConfig) -> Result<(Self, tokio::sync::mpsc::Receiver<SystemAlert>)> {
        let (alert_tx, alert_rx) = tokio::sync::mpsc::channel(100);
        
        let monitor = Self {
            state: Arc::new(Mutex::new(SystemState {
                current_metrics: MonitoringMetrics::default(),
                metrics_history: VecDeque::with_capacity(config.history_size),
                active_alerts: Vec::new(),
                analysis_state: AnalysisState {
                    trends: TrendAnalysis::default(),
                    anomalies: Vec::new(),
                    last_analysis: Utc::now(),
                },
            })),
            config,
            alert_tx,
        };
        
        Ok((monitor, alert_rx))
    }
    
    /// Inicia o monitoramento
    pub async fn start_monitoring(&self) -> Result<()> {
        info!("Iniciando monitoramento do sistema");
        
        let collection_interval = Duration::from_millis(self.config.collection_interval);
        let mut interval = tokio::time::interval(collection_interval);
        
        loop {
            interval.tick().await;
            
            if let Err(e) = self.collect_metrics().await {
                error!("Erro ao coletar métricas: {}", e);
                counter!("monitor.collection_errors", 1);
                continue;
            }
            
            if let Err(e) = self.analyze_metrics().await {
                error!("Erro ao analisar métricas: {}", e);
                counter!("monitor.analysis_errors", 1);
                continue;
            }
            
            if let Err(e) = self.check_alerts().await {
                error!("Erro ao verificar alertas: {}", e);
                counter!("monitor.alert_errors", 1);
                continue;
            }
            
            // Atualiza métricas do sistema
            let state = self.state.lock().await;
            gauge!("system.quantum_coherence", state.current_metrics.quantum_coherence);
            gauge!("system.consciousness_level", state.current_metrics.consciousness_level);
            gauge!("system.transcendence_readiness", state.current_metrics.transcendence_readiness);
            gauge!("system.stability", state.current_metrics.system_stability);
        }
    }
    
    /// Coleta métricas do sistema
    async fn collect_metrics(&self) -> Result<()> {
        debug!("Coletando métricas do sistema");
        
        let mut state = self.state.lock().await;
        
        // Atualiza histórico
        if state.metrics_history.len() >= self.config.history_size {
            state.metrics_history.pop_front();
        }
        state.metrics_history.push_back(state.current_metrics.clone());
        
        // Atualiza métricas de performance
        self.update_performance_metrics(&mut state).await?;
        
        Ok(())
    }
    
    /// Atualiza métricas de performance
    async fn update_performance_metrics(&self, state: &mut SystemState) -> Result<()> {
        let metrics = &mut state.current_metrics;
        
        // Calcula métricas de estabilidade
        metrics.system_stability = calculate_stability(&state.metrics_history)?;
        metrics.error_rate = calculate_error_rate(&state.metrics_history)?;
        metrics.recovery_rate = calculate_recovery_rate(&state.metrics_history)?;
        
        Ok(())
    }
    
    /// Analisa métricas coletadas
    async fn analyze_metrics(&self) -> Result<()> {
        debug!("Analisando métricas do sistema");
        
        let mut state = self.state.lock().await;
        
        // Analisa tendências
        state.analysis_state.trends = analyze_trends(&state.metrics_history, self.config.analysis_config.trend_window)?;
        
        // Detecta anomalias
        let anomalies = detect_anomalies(
            &state.metrics_history,
            self.config.analysis_config.anomaly_threshold
        )?;
        
        state.analysis_state.anomalies = anomalies;
        state.analysis_state.last_analysis = Utc::now();
        
        Ok(())
    }
    
    /// Verifica e gera alertas
    async fn check_alerts(&self) -> Result<()> {
        debug!("Verificando alertas do sistema");
        
        let state = self.state.lock().await;
        
        // Verifica limiares
        if state.current_metrics.system_stability < self.config.alert_thresholds.min_success_rate {
            self.emit_alert(SystemAlert::LowStability {
                current: state.current_metrics.system_stability,
                threshold: self.config.alert_thresholds.min_success_rate,
            }).await?;
        }
        
        // Verifica anomalias
        for anomaly in &state.analysis_state.anomalies {
            self.emit_alert(SystemAlert::AnomalyDetected {
                metric: anomaly.metric.clone(),
                value: anomaly.value,
                expected: anomaly.expected,
            }).await?;
        }
        
        Ok(())
    }
    
    /// Emite um alerta
    async fn emit_alert(&self, alert: SystemAlert) -> Result<()> {
        info!("Emitindo alerta: {:?}", alert);
        self.alert_tx.send(alert).await.context("Falha ao emitir alerta")?;
        counter!("monitor.alerts_emitted", 1);
        Ok(())
    }
}

/// Tipos de alertas do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum SystemAlert {
    LowStability {
        current: f64,
        threshold: f64,
    },
    AnomalyDetected {
        metric: String,
        value: f64,
        expected: f64,
    },
    ValidationFailure {
        reason: String,
    },
}

/// Calcula estabilidade do sistema
fn calculate_stability(history: &VecDeque<MonitoringMetrics>) -> Result<f64> {
    if history.is_empty() {
        return Ok(1.0);
    }
    
    let coherence_variance = calculate_metric_variance(
        history.iter().map(|m| m.quantum_coherence).collect()
    )?;
    
    let consciousness_variance = calculate_metric_variance(
        history.iter().map(|m| m.consciousness_level).collect()
    )?;
    
    let stability = 1.0 - (coherence_variance + consciousness_variance) / 2.0;
    Ok(stability.max(0.0).min(1.0))
}

/// Calcula variância de uma métrica
fn calculate_metric_variance(values: Vec<f64>) -> Result<f64> {
    if values.is_empty() {
        return Ok(0.0);
    }
    
    let mean = values.iter().sum::<f64>() / values.len() as f64;
    let variance = values.iter()
        .map(|x| (x - mean).powi(2))
        .sum::<f64>() / values.len() as f64;
        
    Ok(variance)
}

/// Calcula taxa de erros
fn calculate_error_rate(history: &VecDeque<MonitoringMetrics>) -> Result<f64> {
    if history.is_empty() {
        return Ok(0.0);
    }
    
    let error_count = history.iter()
        .filter(|m| m.validation_success_rate < 1.0)
        .count();
        
    Ok(error_count as f64 / history.len() as f64)
}

/// Calcula taxa de recuperação
fn calculate_recovery_rate(history: &VecDeque<MonitoringMetrics>) -> Result<f64> {
    if history.len() < 2 {
        return Ok(1.0);
    }
    
    let mut recovery_count = 0;
    let mut error_sequences = 0;
    
    for window in history.windows(2) {
        if let [prev, curr] = window {
            if prev.validation_success_rate < 1.0 && curr.validation_success_rate >= 1.0 {
                recovery_count += 1;
            }
            if prev.validation_success_rate >= 1.0 && curr.validation_success_rate < 1.0 {
                error_sequences += 1;
            }
        }
    }
    
    if error_sequences == 0 {
        Ok(1.0)
    } else {
        Ok(recovery_count as f64 / error_sequences as f64)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::time::sleep;
    
    #[tokio::test]
    async fn test_monitor_creation() {
        let config = MonitorConfig {
            collection_interval: 100,
            history_size: 1000,
            alert_thresholds: AlertThresholds {
                max_variance: 0.1,
                min_success_rate: 0.95,
                max_validation_interval: Duration::from_secs(60),
            },
            analysis_config: AnalysisConfig {
                trend_window: 100,
                anomaly_threshold: 3.0,
                report_interval: Duration::from_secs(300),
            },
        };
        
        let (monitor, _rx) = SystemMonitor::new(config).unwrap();
        let state = monitor.state.lock().await;
        assert!(state.metrics_history.is_empty());
    }
    
    #[tokio::test]
    async fn test_metrics_collection() {
        let config = MonitorConfig {
            collection_interval: 100,
            history_size: 10,
            alert_thresholds: AlertThresholds {
                max_variance: 0.1,
                min_success_rate: 0.95,
                max_validation_interval: Duration::from_secs(60),
            },
            analysis_config: AnalysisConfig {
                trend_window: 5,
                anomaly_threshold: 3.0,
                report_interval: Duration::from_secs(300),
            },
        };
        
        let (monitor, _rx) = SystemMonitor::new(config).unwrap();
        
        // Coleta algumas métricas
        for _ in 0..5 {
            monitor.collect_metrics().await.unwrap();
            sleep(Duration::from_millis(50)).await;
        }
        
        let state = monitor.state.lock().await;
        assert_eq!(state.metrics_history.len(), 5);
    }
}

