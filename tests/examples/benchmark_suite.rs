use std::time::Duration;
use anyhow::Result;
use tokio::time::sleep;
use plotters::style::Color;

use crate::{
    core::{
        reports::BenchmarkReport,
        monitoring::{MetricsSnapshot, MonitorConfig},
    },
    protocols::{
        transcendence::{TranscendenceProtocol, ElevationMethod},
        monitoring::ContinuousMonitor,
    },
};

/// Executa uma bateria completa de benchmarks do sistema VIREON
pub async fn run_benchmark_suite() -> Result<()> {
    println!("Iniciando bateria de testes de performance do VIREON...\n");

    // Configuração do monitor
    let monitor_config = MonitorConfig {
        collection_interval: Duration::from_millis(100),
        buffer_size: 1000,
        alert_thresholds: vec![
            ("cpu_usage".into(), 80.0),
            ("memory_usage".into(), 85.0),
            ("latency".into(), 500.0),
        ],
    };

    // Inicializa monitor
    let monitor = ContinuousMonitor::new(monitor_config);
    let report = BenchmarkReport::new();

    println!("1. Teste de Throughput Base");
    let base_result = benchmark_base_throughput(&monitor).await?;
    report.add_test_result(base_result);
    println!("   ✓ Concluído\n");

    println!("2. Teste de Latência sob Carga");
    let load_result = benchmark_under_load(&monitor).await?;
    report.add_test_result(load_result);
    println!("   ✓ Concluído\n");

    println!("3. Teste de Recovery após Falha");
    let recovery_result = benchmark_recovery(&monitor).await?;
    report.add_test_result(recovery_result);
    println!("   ✓ Concluído\n");

    println!("4. Teste de Evolução Contínua");
    let evolution_result = benchmark_continuous_evolution(&monitor).await?;
    report.add_test_result(evolution_result);
    println!("   ✓ Concluído\n");

    // Gera relatórios
    println!("Gerando relatórios...");
    report.generate_visual_report("./reports/benchmarks")?;
    report.export_json("./reports/benchmarks/results.json")?;

    // Imprime sumário
    print_summary(&report);

    Ok(())
}

/// Benchmark de throughput base
async fn benchmark_base_throughput(monitor: &ContinuousMonitor) -> Result<TestResult> {
    let protocol = TranscendenceProtocol::new();
    let start = std::time::Instant::now();
    let mut operations = 0;
    let mut errors = 0;

    // Executa operações por 30 segundos
    while start.elapsed() < Duration::from_secs(30) {
        if let Err(_) = protocol.evolve(ElevationMethod::QuantumLeap).await {
            errors += 1;
        }
        operations += 1;
        monitor.collect_metrics().await?;
        sleep(Duration::from_millis(10)).await;
    }

    Ok(TestResult {
        name: "Base Throughput".into(),
        duration: start.elapsed(),
        operations,
        throughput: operations as f64 / start.elapsed().as_secs_f64(),
        latency_stats: monitor.get_latency_statistics().await?,
        error_rate: errors as f64 / operations as f64,
    })
}

/// Benchmark sob carga pesada
async fn benchmark_under_load(monitor: &ContinuousMonitor) -> Result<TestResult> {
    let protocol = TranscendenceProtocol::new();
    let start = std::time::Instant::now();
    let mut operations = 0;
    let mut errors = 0;

    // Executa operações paralelas intensivas
    let mut handles = vec![];
    for _ in 0..10 {
        let protocol_clone = protocol.clone();
        handles.push(tokio::spawn(async move {
            for _ in 0..1000 {
                if let Err(_) = protocol_clone.evolve(ElevationMethod::QuantumLeap).await {
                    return Err(anyhow::anyhow!("Evolution failed"));
                }
            }
            Ok(())
        }));
        operations += 1000;
    }

    for handle in handles {
        if let Err(_) = handle.await? {
            errors += 1;
        }
    }

    Ok(TestResult {
        name: "Load Test".into(),
        duration: start.elapsed(),
        operations,
        throughput: operations as f64 / start.elapsed().as_secs_f64(),
        latency_stats: monitor.get_latency_statistics().await?,
        error_rate: errors as f64 / operations as f64,
    })
}

/// Benchmark de recuperação após falha
async fn benchmark_recovery(monitor: &ContinuousMonitor) -> Result<TestResult> {
    let protocol = TranscendenceProtocol::new();
    let start = std::time::Instant::now();
    let mut operations = 0;
    let mut errors = 0;

    // Simula falhas e recuperação
    for _ in 0..100 {
        if let Err(_) = protocol.evolve(ElevationMethod::QuantumLeap).await {
            errors += 1;
            // Força recuperação
            protocol.force_recovery().await?;
        }
        operations += 1;
        monitor.collect_metrics().await?;
    }

    Ok(TestResult {
        name: "Recovery Test".into(),
        duration: start.elapsed(),
        operations,
        throughput: operations as f64 / start.elapsed().as_secs_f64(),
        latency_stats: monitor.get_latency_statistics().await?,
        error_rate: errors as f64 / operations as f64,
    })
}

/// Benchmark de evolução contínua
async fn benchmark_continuous_evolution(monitor: &ContinuousMonitor) -> Result<TestResult> {
    let protocol = TranscendenceProtocol::new();
    let start = std::time::Instant::now();
    let mut operations = 0;
    let mut errors = 0;

    // Evolui continuamente por 60 segundos
    while start.elapsed() < Duration::from_secs(60) {
        if let Err(_) = protocol.evolve(ElevationMethod::NaturalProgression).await {
            errors += 1;
        }
        operations += 1;
        monitor.collect_metrics().await?;
        
        // Verifica progresso evolutivo
        let evolution_metrics = protocol.get_evolution_metrics().await?;
        if evolution_metrics.consciousness_level > 0.9 {
            break; // Atingiu nível avançado
        }
    }

    Ok(TestResult {
        name: "Evolution Test".into(),
        duration: start.elapsed(),
        operations,
        throughput: operations as f64 / start.elapsed().as_secs_f64(),
        latency_stats: monitor.get_latency_statistics().await?,
        error_rate: errors as f64 / operations as f64,
    })
}

/// Imprime sumário dos testes
fn print_summary(report: &BenchmarkReport) {
    println!("\n=== Sumário dos Testes ===\n");
    
    println!("Duração Total: {:?}", report.performance_summary.total_duration);
    println!("Total de Operações: {}", report.performance_summary.total_operations);
    println!("Throughput Médio: {:.2} ops/s", report.performance_summary.avg_throughput);
    println!("Throughput Máximo: {:.2} ops/s", report.performance_summary.peak_throughput);
    println!("Taxa de Erro: {:.2}%", report.performance_summary.overall_error_rate * 100.0);
    
    println!("\nMétricas do Sistema:");
    println!("CPU: {}", report.system_info.cpu_info);
    println!("Memória Total: {} MB", report.system_info.memory_total / 1024 / 1024);
    println!("SO: {}", report.system_info.os_version);
    println!("Versão Rust: {}", report.system_info.rust_version);
    
    println!("\nRelatórios gerados em ./reports/benchmarks/");
}

