use std::{
    collections::HashMap,
    sync::Arc,
    time::Duration,
};
use tokio::sync::Mutex;
use chrono::{DateTime, Utc};
use serde::{Serialize, Deserialize};
use anyhow::Result;

use crate::{
    logging::{
        QuantumContext,
        LogLevel,
        LogEntry,
        CircularLogBuffer,
    },
    metrics::{
        MetricsCollector,
        MetricValue,
    },
    quantum::QuantumState,
    consciousness::ConsciousnessState,
};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EnhancedLogEntry {
    pub timestamp: DateTime<Utc>,
    pub level: LogLevel,
    pub message: String,
    pub quantum_context: Option<QuantumContext>,
    pub metrics: Option<HashMap<String, MetricValue>>,
    pub correlation_id: Option<String>,
}

pub struct LogViewer {
    log_buffer: Arc<CircularLogBuffer>,
    metrics_collector: Arc<MetricsCollector>,
    state: Arc<Mutex<LogViewerState>>,
    config: LogViewerConfig,
}

#[derive(Debug, Clone)]
pub struct LogViewerState {
    visible_levels: Vec<LogLevel>,
    search_text: Option<String>,
    auto_scroll: bool,
    visible_columns: Vec<LogColumn>,
    metric_correlations: HashMap<String, Vec<String>>,
    quantum_state_threshold: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LogViewerConfig {
    pub max_entries: usize,
    pub refresh_interval: Duration,
    pub retention_period: Duration,
    pub correlation_window: Duration,
    pub metrics_threshold: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum LogColumn {
    Timestamp,
    Level,
    Message,
    QuantumContext,
    Metrics,
    CorrelationId,
}

impl LogViewer {
    pub async fn new(
        log_buffer: Arc<CircularLogBuffer>,
        metrics_collector: Arc<MetricsCollector>,
        config: LogViewerConfig,
    ) -> Result<Self> {
        let state = Arc::new(Mutex::new(LogViewerState {
            visible_levels: vec![
                LogLevel::Info,
                LogLevel::Warning,
                LogLevel::Error,
                LogLevel::Critical,
            ],
            search_text: None,
            auto_scroll: true,
            visible_columns: vec![
                LogColumn::Timestamp,
                LogColumn::Level,
                LogColumn::Message,
                LogColumn::QuantumContext,
            ],
            metric_correlations: HashMap::new(),
            quantum_state_threshold: 0.8,
        }));

        Ok(Self {
            log_buffer,
            metrics_collector,
            state,
            config,
        })
    }

    pub async fn get_logs(&self, filter: Option<LogFilter>) -> Result<Vec<EnhancedLogEntry>> {
        let state = self.state.lock().await;
        let mut entries = Vec::new();

        let raw_logs = self.log_buffer.get_recent(self.config.max_entries).await?;

        for log in raw_logs {
            if !self.should_display_log(&log, &state, &filter).await? {
                continue;
            }

            let enhanced_log = self.enhance_log_entry(log).await?;
            entries.push(enhanced_log);
        }

        Ok(entries)
    }

    async fn enhance_log_entry(&self, log: LogEntry) -> Result<EnhancedLogEntry> {
        let metrics = if let Some(context) = &log.quantum_context {
            self.metrics_collector
                .get_metrics_at_timestamp(log.timestamp)
                .await?
        } else {
            None
        };

        Ok(EnhancedLogEntry {
            timestamp: log.timestamp,
            level: log.level,
            message: log.message,
            quantum_context: log.quantum_context,
            metrics,
            correlation_id: log.correlation_id,
        })
    }

    async fn should_display_log(
        &self,
        log: &LogEntry,
        state: &LogViewerState,
        filter: &Option<LogFilter>,
    ) -> Result<bool> {
        if !state.visible_levels.contains(&log.level) {
            return Ok(false);
        }

        if let Some(search) = &state.search_text {
            if !log.message.to_lowercase().contains(&search.to_lowercase()) {
                return Ok(false);
            }
        }

        if let Some(filter) = filter {
            if !filter.matches(log) {
                return Ok(false);
            }
        }

        Ok(true)
    }

    pub async fn set_filter(&self, filter: LogFilter) -> Result<()> {
        let mut state = self.state.lock().await;
        state.search_text = filter.text_search;
        state.visible_levels = filter.levels;
        Ok(())
    }

    pub async fn correlate_metrics(&self, log_id: String) -> Result<HashMap<String, MetricValue>> {
        let metrics = self.metrics_collector
            .get_correlated_metrics(log_id, self.config.correlation_window)
            .await?;
        Ok(metrics)
    }

    pub async fn export_logs(&self, format: ExportFormat) -> Result<Vec<u8>> {
        let logs = self.get_logs(None).await?;
        match format {
            ExportFormat::Json => {
                serde_json::to_vec(&logs).map_err(|e| anyhow::anyhow!("JSON serialization failed: {}", e))
            }
            ExportFormat::Csv => {
                let mut wtr = csv::Writer::from_writer(vec![]);
                for log in logs {
                    wtr.serialize(log)?;
                }
                Ok(wtr.into_inner()?)
            }
        }
    }

    pub async fn analyze_trends(&self) -> Result<LogTrends> {
        let logs = self.get_logs(None).await?;
        let mut trends = LogTrends::default();

        for log in logs {
            if let Some(metrics) = log.metrics {
                trends.update(&metrics);
            }
        }

        Ok(trends)
    }
}

#[derive(Debug, Clone, Default)]
pub struct LogTrends {
    pub error_frequency: HashMap<String, usize>,
    pub quantum_state_changes: Vec<(DateTime<Utc>, QuantumState)>,
    pub consciousness_evolution: Vec<(DateTime<Utc>, ConsciousnessState)>,
    pub metric_patterns: HashMap<String, Vec<MetricValue>>,
}

impl LogTrends {
    fn update(&mut self, metrics: &HashMap<String, MetricValue>) {
        for (key, value) in metrics {
            self.metric_patterns
                .entry(key.clone())
                .or_default()
                .push(value.clone());
        }
    }
}

#[derive(Debug, Clone)]
pub struct LogFilter {
    pub text_search: Option<String>,
    pub levels: Vec<LogLevel>,
    pub time_range: Option<(DateTime<Utc>, DateTime<Utc>)>,
    pub quantum_state_filter: Option<QuantumState>,
    pub metric_threshold: Option<HashMap<String, f64>>,
}

impl LogFilter {
    fn matches(&self, log: &LogEntry) -> bool {
        if let Some(text) = &self.text_search {
            if !log.message.to_lowercase().contains(&text.to_lowercase()) {
                return false;
            }
        }

        if !self.levels.contains(&log.level) {
            return false;
        }

        if let Some((start, end)) = self.time_range {
            if log.timestamp < start || log.timestamp > end {
                return false;
            }
        }

        true
    }
}

#[derive(Debug, Clone, Copy)]
pub enum ExportFormat {
    Json,
    Csv,
}

