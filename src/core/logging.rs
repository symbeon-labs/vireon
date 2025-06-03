use std::{
    collections::VecDeque,
    sync::{Arc, Mutex},
    time::{SystemTime, UNIX_EPOCH},
};

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use tokio::sync::broadcast;
use tracing::{Event, Level, Subscriber};
use tracing_subscriber::{layer::Context, Layer};

/// Níveis de log suportados pelo sistema
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum LogLevel {
    Debug,
    Info,
    Warn,
    Error,
}

/// Estado quântico no momento do log
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumContext {
    pub coherence: f64,
    pub entanglement_level: f64,
    pub stability_index: f64,
    pub evolution_stage: String,
}

/// Estrutura principal de log com contexto quântico
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumLogEntry {
    pub timestamp: DateTime<Utc>,
    pub level: LogLevel,
    pub message: String,
    pub quantum_context: QuantumContext,
    pub module_path: String,
    pub file_line: Option<String>,
    pub correlation_id: Option<String>,
    pub metrics: Option<serde_json::Value>,
}

/// Configuração do sistema de logging
#[derive(Debug, Clone)]
pub struct LogConfig {
    pub buffer_size: usize,
    pub min_level: LogLevel,
    pub enable_file_output: bool,
    pub enable_console_output: bool,
    pub enable_metrics_integration: bool,
}

/// Buffer circular thread-safe para armazenamento de logs
#[derive(Clone)]
pub struct CircularLogBuffer {
    entries: Arc<Mutex<VecDeque<QuantumLogEntry>>>,
    max_size: usize,
}

impl CircularLogBuffer {
    pub fn new(max_size: usize) -> Self {
        Self {
            entries: Arc::new(Mutex::new(VecDeque::with_capacity(max_size))),
            max_size,
        }
    }

    pub fn push(&self, entry: QuantumLogEntry) {
        let mut buffer = self.entries.lock().unwrap();
        if buffer.len() >= self.max_size {
            buffer.pop_front();
        }
        buffer.push_back(entry);
    }

    pub fn get_recent(&self, count: usize) -> Vec<QuantumLogEntry> {
        let buffer = self.entries.lock().unwrap();
        buffer.iter().rev().take(count).cloned().collect()
    }

    pub fn filter_by_level(&self, level: LogLevel) -> Vec<QuantumLogEntry> {
        let buffer = self.entries.lock().unwrap();
        buffer
            .iter()
            .filter(|entry| entry.level == level)
            .cloned()
            .collect()
    }
}

/// Gerenciador principal de logging
pub struct QuantumLogger {
    buffer: CircularLogBuffer,
    config: LogConfig,
    metrics_tx: Option<broadcast::Sender<serde_json::Value>>,
}

impl QuantumLogger {
    pub fn new(config: LogConfig) -> Self {
        Self {
            buffer: CircularLogBuffer::new(config.buffer_size),
            config,
            metrics_tx: None,
        }
    }

    pub fn set_metrics_channel(&mut self, tx: broadcast::Sender<serde_json::Value>) {
        self.metrics_tx = Some(tx);
    }

    pub async fn log(&self, 
        level: LogLevel, 
        message: String, 
        quantum_context: QuantumContext,
        correlation_id: Option<String>,
        metrics: Option<serde_json::Value>
    ) {
        let entry = QuantumLogEntry {
            timestamp: Utc::now(),
            level,
            message,
            quantum_context,
            module_path: module_path!().to_string(),
            file_line: Some(format!("{}:{}", file!(), line!())),
            correlation_id,
            metrics: metrics.clone(),
        };

        // Armazena no buffer circular
        self.buffer.push(entry.clone());

        // Integração com métricas se habilitado
        if self.config.enable_metrics_integration {
            if let Some(metrics) = metrics {
                if let Some(tx) = &self.metrics_tx {
                    let _ = tx.send(metrics);
                }
            }
        }

        // Output para console se habilitado
        if self.config.enable_console_output {
            println!("[{}] {}: {}", 
                entry.level, 
                entry.timestamp, 
                entry.message
            );
        }
    }

    pub fn get_recent_logs(&self, count: usize) -> Vec<QuantumLogEntry> {
        self.buffer.get_recent(count)
    }

    pub fn filter_logs(&self, level: LogLevel) -> Vec<QuantumLogEntry> {
        self.buffer.filter_by_level(level)
    }
}

/// Implementação da trait Layer do tracing para integração
pub struct QuantumLogLayer {
    logger: Arc<QuantumLogger>,
}

impl<S: Subscriber> Layer<S> for QuantumLogLayer {
    fn on_event(&self, event: &Event<'_>, _ctx: Context<'_, S>) {
        // Extrai informações do evento
        let level = match *event.metadata().level() {
            Level::TRACE | Level::DEBUG => LogLevel::Debug,
            Level::INFO => LogLevel::Info,
            Level::WARN => LogLevel::Warn,
            Level::ERROR => LogLevel::Error,
        };

        // Cria contexto quântico default
        let quantum_context = QuantumContext {
            coherence: 1.0,
            entanglement_level: 1.0,
            stability_index: 1.0,
            evolution_stage: "normal".to_string(),
        };

        // Processa o evento assincronamente
        let logger = self.logger.clone();
        tokio::spawn(async move {
            logger.log(
                level,
                event.metadata().name().to_string(),
                quantum_context,
                None,
                None
            ).await;
        });
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tokio::time::{sleep, Duration};

    #[tokio::test]
    async fn test_basic_logging() {
        let config = LogConfig {
            buffer_size: 1000,
            min_level: LogLevel::Debug,
            enable_file_output: false,
            enable_console_output: true,
            enable_metrics_integration: false,
        };

        let logger = QuantumLogger::new(config);

        let context = QuantumContext {
            coherence: 0.95,
            entanglement_level: 0.85,
            stability_index: 0.90,
            evolution_stage: "testing".to_string(),
        };

        logger.log(
            LogLevel::Info,
            "Test log message".to_string(),
            context,
            None,
            None
        ).await;

        let logs = logger.get_recent_logs(1);
        assert_eq!(logs.len(), 1);
        assert_eq!(logs[0].level, LogLevel::Info);
    }

    #[tokio::test]
    async fn test_circular_buffer() {
        let buffer = CircularLogBuffer::new(2);

        let context = QuantumContext {
            coherence: 1.0,
            entanglement_level: 1.0,
            stability_index: 1.0,
            evolution_stage: "test".to_string(),
        };

        for i in 1..=3 {
            let entry = QuantumLogEntry {
                timestamp: Utc::now(),
                level: LogLevel::Info,
                message: format!("Log {}", i),
                quantum_context: context.clone(),
                module_path: "test".to_string(),
                file_line: None,
                correlation_id: None,
                metrics: None,
            };
            buffer.push(entry);
            sleep(Duration::from_millis(1)).await;
        }

        let entries = buffer.get_recent(3);
        assert_eq!(entries.len(), 2);
        assert_eq!(entries[0].message, "Log 3");
    }

    #[tokio::test]
    async fn test_metrics_integration() {
        let (tx, mut rx) = broadcast::channel(100);
        
        let mut config = LogConfig {
            buffer_size: 1000,
            min_level: LogLevel::Debug,
            enable_file_output: false,
            enable_console_output: false,
            enable_metrics_integration: true,
        };

        let mut logger = QuantumLogger::new(config);
        logger.set_metrics_channel(tx);

        let context = QuantumContext {
            coherence: 0.95,
            entanglement_level: 0.85,
            stability_index: 0.90,
            evolution_stage: "testing".to_string(),
        };

        let metrics = serde_json::json!({
            "operation_time_ms": 100,
            "success_rate": 0.95
        });

        logger.log(
            LogLevel::Info,
            "Test with metrics".to_string(),
            context,
            None,
            Some(metrics.clone())
        ).await;

        if let Ok(received) = rx.try_recv() {
            assert_eq!(received, metrics);
        }
    }
}

