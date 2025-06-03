use std::{sync::Arc, time::Duration};
use tokio::{sync::Mutex, time};
use tracing::{info, warn};

use vireon::{
    core::{
        metrics::{MetricsSnapshot, SystemMetrics},
        monitoring::{MonitorConfig, ContinuousMonitor},
    },
    protocols::{
        transcendence::{TranscendenceProtocol, ElevationMethod},
        validation::{ValidationSystem, ValidationConfig},
        quantum::{QuantumState, QuantumConfig},
    },
    dashboard::BenchmarkDashboard,
};

const BENCHMARK_DURATION: Duration = Duration::from_secs(300); // 5 minutos
const REPORT_INTERVAL: Duration = Duration::from_secs(1);
const METRICS_BUFFER_SIZE: usize = 1000;

/// Configuração do benchmark
struct BenchmarkConfig {
    concurrent_operations: usize,
    elevation_methods: Vec<ElevationMethod>,
    quantum_states: Vec<QuantumState>,
    validation_config: ValidationConfig,
    monitor_config: MonitorConfig,
}

impl Default for BenchmarkConfig {
    fn default() -> Self {
        Self {
            concurrent_operations: 100,
            elevation_methods: vec![
                ElevationMethod::QuantumLeap,
                ElevationMethod::NaturalProgression,
                ElevationMethod::GuidedTranscendence,
            ],
            quantum_states: vec![
                QuantumState::Superposition,
                QuantumState::Entangled,
                QuantumState::Coherent,
            ],
            validation_config: ValidationConfig::default(),
            monitor_config: MonitorConfig::new(METRICS_BUFFER_SIZE),
        }
    }
}

/// Executor do benchmark
struct BenchmarkExecutor {
    config: BenchmarkConfig,
    protocol: Arc<TranscendenceProtocol>,
    monitor: Arc<ContinuousMonitor>,
    validation: Arc<ValidationSystem>,
    metrics: Arc<Mutex<Vec<MetricsSnapshot>>>,
}

impl BenchmarkExecutor {
    pub fn new(config: BenchmarkConfig) -> Self {
        let protocol = Arc::new(TranscendenceProtocol::new(
            QuantumConfig::default(),
            config.validation_config.clone(),
        ));
        
        let monitor = Arc::new(ContinuousMonitor::new(config.monitor_config.clone()));
        let validation = Arc::new(ValidationSystem::new(config.validation_config.clone()));
        let metrics = Arc::new(Mutex::new(Vec::with_capacity(METRICS_BUFFER_SIZE)));

        Self {
            config,
            protocol,
            monitor,
            validation,
            metrics,
        }
    }

    /// Executa uma única operação de elevação
    async fn execute_single_operation(&self, method: ElevationMethod, state: QuantumState) -> anyhow::Result<()> {
        let start = time::Instant::now();
        
        // Tenta elevar o estado
        match self.protocol.elevate(method, state).await {
            Ok(new_state) => {
                // Valida o novo estado
                self.validation.validate_state(&new_state).await?;
                
                // Coleta métricas
                let duration = start.elapsed();
                self.monitor.record_operation_success(duration).await;
                
                info!("Elevação bem sucedida: {:?} -> {:?}", state, new_state);
                Ok(())
            }
            Err(e) => {
                self.monitor.record_operation_failure().await;
                warn!("Falha na elevação: {}", e);
                Err(e.into())
            }
        }
    }

    /// Executa o benchmark completo
    pub async fn run(&self) -> anyhow::Result<()> {
        info!("Iniciando benchmark com {} operações concorrentes", self.config.concurrent_operations);

        // Inicia dashboard
        let dashboard = BenchmarkDashboard::new(self.monitor.clone());
        tokio::spawn(async move {
            dashboard.launch().await;
        });

        // Timer para duração total
        let end_time = time::Instant::now() + BENCHMARK_DURATION;

        while time::Instant::now() < end_time {
            let mut tasks = Vec::new();

            // Cria operações concorrentes
            for _ in 0..self.config.concurrent_operations {
                let method = self.config.elevation_methods.choose(&mut rand::thread_rng()).unwrap().clone();
                let state = self.config.quantum_states.choose(&mut rand::thread_rng()).unwrap().clone();
                
                let protocol = self.protocol.clone();
                let monitor = self.monitor.clone();
                
                tasks.push(tokio::spawn(async move {
                    match self.execute_single_operation(method, state).await {
                        Ok(_) => (),
                        Err(e) => warn!("Operação falhou: {}", e),
                    }
                }));
            }

            // Aguarda conclusão do batch
            futures::future::join_all(tasks).await;

            // Coleta métricas
            let snapshot = self.monitor.take_snapshot().await;
            self.metrics.lock().await.push(snapshot);

            // Relatório de progresso
            info!(
                "Progresso: {:.1}%, Throughput: {:.1} ops/s, Latência: {:.2}ms, Erros: {:.2}%",
                (time::Instant::now() - end_time).as_secs_f64() / BENCHMARK_DURATION.as_secs_f64() * 100.0,
                snapshot.throughput,
                snapshot.avg_latency,
                snapshot.error_rate * 100.0,
            );

            time::sleep(REPORT_INTERVAL).await;
        }

        // Gera relatório final
        self.generate_report().await?;

        Ok(())
    }

    /// Gera relatório detalhado do benchmark
    async fn generate_report(&self) -> anyhow::Result<()> {
        let metrics = self.metrics.lock().await;
        let total_ops = metrics.iter().map(|m| m.total_operations).sum::<u64>();
        let avg_throughput = metrics.iter().map(|m| m.throughput).sum::<f64>() / metrics.len() as f64;
        let avg_latency = metrics.iter().map(|m| m.avg_latency).sum::<f64>() / metrics.len() as f64;
        let error_rate = metrics.iter().map(|m| m.error_rate).sum::<f64>() / metrics.len() as f64;

        info!("=== Relatório Final do Benchmark ===");
        info!("Duração Total: {:?}", BENCHMARK_DURATION);
        info!("Total de Operações: {}", total_ops);
        info!("Throughput Médio: {:.1} ops/s", avg_throughput);
        info!("Latência Média: {:.2}ms", avg_latency);
        info!("Taxa de Erro: {:.2}%", error_rate * 100.0);

        // Exporta métricas detalhadas
        let report_path = "benchmark_report.json";
        let report = serde_json::to_string_pretty(&*metrics)?;
        std::fs::write(report_path, report)?;
        info!("Relatório detalhado salvo em: {}", report_path);

        Ok(())
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Configura logging
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .init();

    // Configura e executa benchmark
    let config = BenchmarkConfig::default();
    let executor = BenchmarkExecutor::new(config);
    
    info!("Iniciando suite de benchmark VIREON");
    executor.run().await?;
    info!("Benchmark concluído com sucesso");

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_single_operation() {
        let config = BenchmarkConfig::default();
        let executor = BenchmarkExecutor::new(config);

        let result = executor
            .execute_single_operation(
                ElevationMethod::QuantumLeap,
                QuantumState::Superposition,
            )
            .await;

        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_metrics_collection() {
        let config = BenchmarkConfig {
            concurrent_operations: 10,
            ..Default::default()
        };
        let executor = BenchmarkExecutor::new(config);

        // Executa algumas operações
        for _ in 0..5 {
            executor
                .execute_single_operation(
                    ElevationMethod::QuantumLeap,
                    QuantumState::Superposition,
                )
                .await
                .unwrap();
        }

        let metrics = executor.metrics.lock().await;
        assert!(!metrics.is_empty());
    }
}

