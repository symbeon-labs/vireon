//! # Utilitários
//!
//! Este módulo fornece funções utilitárias e helpers para a crate symbiotic_method,
//! incluindo validação, serialização, logging e outras funcionalidades auxiliares.

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use chrono::{DateTime, Utc};
use uuid::Uuid;
use tracing::{debug, info, warn};

/// Versão da crate
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Nome da crate
pub const CRATE_NAME: &str = env!("CARGO_PKG_NAME");

/// Descrição da crate
pub const DESCRIPTION: &str = env!("CARGO_PKG_DESCRIPTION");

/// Configuração de logging
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LoggingConfig {
    pub level: String,
    pub format: String,
    pub enable_colors: bool,
    pub enable_timestamps: bool,
    pub output_file: Option<String>,
}

impl Default for LoggingConfig {
    fn default() -> Self {
        Self {
            level: "info".to_string(),
            format: "full".to_string(),
            enable_colors: true,
            enable_timestamps: true,
            output_file: None,
        }
    }
}

/// Informações do sistema
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct SystemInfo {
    #[pyo3(get)]
    pub crate_name: String,
    #[pyo3(get)]
    pub version: String,
    #[pyo3(get)]
    pub description: String,
    #[pyo3(get)]
    pub build_timestamp: String,
    #[pyo3(get)]
    pub rust_version: String,
    #[pyo3(get)]
    pub features: Vec<String>,
}

#[pymethods]
impl SystemInfo {
    #[new]
    fn new() -> Self {
        Self {
            crate_name: CRATE_NAME.to_string(),
            version: VERSION.to_string(),
            description: DESCRIPTION.to_string(),
            build_timestamp: Utc::now().to_rfc3339(),
            rust_version: env!("RUSTC_VERSION").to_string(),
            features: vec![
                "quantum".to_string(),
                "consciousness".to_string(),
                "evolution".to_string(),
            ],
        }
    }
    
    fn to_dict(&self) -> HashMap<String, PyObject> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        
        let mut result = HashMap::new();
        result.insert("crate_name".to_string(), self.crate_name.to_object(py));
        result.insert("version".to_string(), self.version.to_object(py));
        result.insert("description".to_string(), self.description.to_object(py));
        result.insert("build_timestamp".to_string(), self.build_timestamp.to_object(py));
        result.insert("rust_version".to_string(), self.rust_version.to_object(py));
        result.insert("features".to_string(), self.features.to_object(py));
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "{} v{} - {}",
            self.crate_name,
            self.version,
            self.description
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "SystemInfo(name='{}', version='{}', features={:?})",
            self.crate_name,
            self.version,
            self.features
        )
    }
}

/// Gerador de IDs únicos
pub struct IdGenerator;

impl IdGenerator {
    /// Gera um UUID v4
    pub fn uuid() -> String {
        Uuid::new_v4().to_string()
    }
    
    /// Gera um ID curto (8 caracteres)
    pub fn short_id() -> String {
        Uuid::new_v4().to_string()[..8].to_string()
    }
    
    /// Gera um ID com prefixo
    pub fn prefixed_id(prefix: &str) -> String {
        format!("{}-{}", prefix, Self::short_id())
    }
    
    /// Gera um ID baseado em timestamp
    pub fn timestamp_id() -> String {
        format!("{}-{}", 
            Utc::now().timestamp_millis(),
            Self::short_id()
        )
    }
}

/// Validador de configurações
pub struct ConfigValidator;

impl ConfigValidator {
    /// Valida um valor float no intervalo [0, 1]
    pub fn validate_probability(value: f64, field_name: &str) -> Result<(), String> {
        if value < 0.0 || value > 1.0 {
            Err(format!("{} deve estar entre 0.0 e 1.0, recebido: {}", field_name, value))
        } else {
            Ok(())
        }
    }
    
    /// Valida um valor positivo
    pub fn validate_positive(value: f64, field_name: &str) -> Result<(), String> {
        if value <= 0.0 {
            Err(format!("{} deve ser positivo, recebido: {}", field_name, value))
        } else {
            Ok(())
        }
    }
    
    /// Valida que uma string não está vazia
    pub fn validate_non_empty_string(value: &str, field_name: &str) -> Result<(), String> {
        if value.trim().is_empty() {
            Err(format!("{} não pode estar vazio", field_name))
        } else {
            Ok(())
        }
    }
    
    /// Valida um ID UUID
    pub fn validate_uuid(value: &str, field_name: &str) -> Result<(), String> {
        Uuid::parse_str(value)
            .map(|_| ())
            .map_err(|_| format!("{} deve ser um UUID válido, recebido: {}", field_name, value))
    }
    
    /// Valida um timestamp RFC3339
    pub fn validate_timestamp(value: &str, field_name: &str) -> Result<(), String> {
        DateTime::parse_from_rfc3339(value)
            .map(|_| ())
            .map_err(|_| format!("{} deve ser um timestamp RFC3339 válido, recebido: {}", field_name, value))
    }
}

/// Serialização de dados
pub struct DataSerializer;

impl DataSerializer {
    /// Serializa para JSON
    pub fn to_json<T: Serialize>(data: &T) -> Result<String, serde_json::Error> {
        serde_json::to_string_pretty(data)
    }
    
    /// Deserializa de JSON
    pub fn from_json<'a, T: Deserialize<'a>>(json: &'a str) -> Result<T, serde_json::Error> {
        serde_json::from_str(json)
    }
    
    /// Serializa para bytes
    pub fn to_bytes<T: Serialize>(data: &T) -> Result<Vec<u8>, serde_json::Error> {
        serde_json::to_vec(data)
    }
    
    /// Deserializa de bytes
    pub fn from_bytes<T: for<'a> Deserialize<'a>>(bytes: &[u8]) -> Result<T, serde_json::Error> {
        serde_json::from_slice(bytes)
    }
}

/// Medidor de performance
#[derive(Debug, Clone)]
pub struct PerformanceTimer {
    start_time: std::time::Instant,
    operation_name: String,
}

impl PerformanceTimer {
    /// Inicia um novo timer
    pub fn start(operation_name: impl Into<String>) -> Self {
        let operation_name = operation_name.into();
        debug!("Iniciando timer para operação: {}", operation_name);
        
        Self {
            start_time: std::time::Instant::now(),
            operation_name,
        }
    }
    
    /// Finaliza o timer e retorna a duração em milissegundos
    pub fn finish(self) -> u128 {
        let duration = self.start_time.elapsed();
        let duration_ms = duration.as_millis();
        
        if duration_ms > 1000 {
            warn!(
                "Operação '{}' demorou {}ms (lenta)",
                self.operation_name,
                duration_ms
            );
        } else {
            debug!(
                "Operação '{}' concluída em {}ms",
                self.operation_name,
                duration_ms
            );
        }
        
        duration_ms
    }
    
    /// Obtém a duração atual sem finalizar o timer
    pub fn elapsed(&self) -> u128 {
        self.start_time.elapsed().as_millis()
    }
}

/// Formatador de tamanhos de arquivo
pub struct SizeFormatter;

impl SizeFormatter {
    /// Formata bytes em unidades legíveis
    pub fn format_bytes(bytes: u64) -> String {
        const UNITS: &[&str] = &["B", "KB", "MB", "GB", "TB", "PB"];
        
        if bytes == 0 {
            return "0 B".to_string();
        }
        
        let mut size = bytes as f64;
        let mut unit_index = 0;
        
        while size >= 1024.0 && unit_index < UNITS.len() - 1 {
            size /= 1024.0;
            unit_index += 1;
        }
        
        if unit_index == 0 {
            format!("{} {}", bytes, UNITS[unit_index])
        } else {
            format!("{:.2} {}", size, UNITS[unit_index])
        }
    }
    
    /// Formata tempo em unidades legíveis
    pub fn format_duration(milliseconds: u128) -> String {
        if milliseconds < 1000 {
            format!("{}ms", milliseconds)
        } else if milliseconds < 60_000 {
            format!("{:.2}s", milliseconds as f64 / 1000.0)
        } else if milliseconds < 3_600_000 {
            format!("{:.2}m", milliseconds as f64 / 60_000.0)
        } else {
            format!("{:.2}h", milliseconds as f64 / 3_600_000.0)
        }
    }
}

/// Funções Python utilitárias
#[pyfunction]
pub fn get_system_info() -> SystemInfo {
    SystemInfo::new()
}

#[pyfunction]
pub fn generate_uuid() -> String {
    IdGenerator::uuid()
}

#[pyfunction]
pub fn generate_short_id() -> String {
    IdGenerator::short_id()
}

#[pyfunction]
pub fn generate_prefixed_id(prefix: String) -> String {
    IdGenerator::prefixed_id(&prefix)
}

#[pyfunction]
pub fn validate_probability_value(value: f64, field_name: String) -> PyResult<bool> {
    match ConfigValidator::validate_probability(value, &field_name) {
        Ok(()) => Ok(true),
        Err(msg) => Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(msg)),
    }
}

#[pyfunction]
pub fn format_bytes(bytes: u64) -> String {
    SizeFormatter::format_bytes(bytes)
}

#[pyfunction]
pub fn format_duration_ms(milliseconds: u128) -> String {
    SizeFormatter::format_duration(milliseconds)
}

#[pyfunction]
pub fn serialize_to_json(data: HashMap<String, PyObject>) -> PyResult<String> {
    // Converter PyObject para serde_json::Value seria complexo
    // Por simplicidade, vamos usar uma implementação básica
    let gil = Python::acquire_gil();
    let py = gil.python();
    
    let json_str = py.import("json")?.
        getattr("dumps")?.call1((data,))?.
        extract::<String>()?;
    
    Ok(json_str)
}

#[pyfunction]
pub fn current_timestamp() -> String {
    Utc::now().to_rfc3339()
}

#[pyfunction]
pub fn timestamp_to_epoch(timestamp: String) -> PyResult<i64> {
    DateTime::parse_from_rfc3339(&timestamp)
        .map(|dt| dt.timestamp())
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(
            format!("Timestamp inválido: {}", e)
        ))
}

/// Inicializa logging para a crate
pub fn init_logging(config: Option<LoggingConfig>) -> Result<(), Box<dyn std::error::Error>> {
    let config = config.unwrap_or_default();
    
    let filter = match config.level.as_str() {
        "error" => tracing::Level::ERROR,
        "warn" => tracing::Level::WARN,
        "info" => tracing::Level::INFO,
        "debug" => tracing::Level::DEBUG,
        "trace" => tracing::Level::TRACE,
        _ => tracing::Level::INFO,
    };
    
    let subscriber = tracing_subscriber::fmt()
        .with_max_level(filter);
    
    let subscriber = if config.enable_colors {
        subscriber.with_ansi(true)
    } else {
        subscriber.with_ansi(false)
    };
    
    let subscriber = if config.enable_timestamps {
        subscriber.with_timer(tracing_subscriber::fmt::time::ChronoUtc::rfc3339())
    } else {
        subscriber.without_time()
    };
    
    if let Some(file_path) = config.output_file {
        let file = std::fs::OpenOptions::new()
            .create(true)
            .append(true)
            .open(file_path)?;
        
        subscriber.with_writer(file).init();
    } else {
        subscriber.init();
    }
    
    info!("Logging inicializado com nível: {}", config.level);
    Ok(())
}

/// Macro para medir tempo de execução
#[macro_export]
macro_rules! time_operation {
    ($operation_name:expr, $block:block) => {
        {
            let timer = $crate::utils::PerformanceTimer::start($operation_name);
            let result = $block;
            timer.finish();
            result
        }
    };
}

/// Macro para logging estruturado
#[macro_export]
macro_rules! log_operation {
    ($level:ident, $operation:expr, $component:expr, $($key:expr => $value:expr),*) => {
        tracing::$level!(
            operation = $operation,
            component = $component,
            $($key = $value),*
        );
    };
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_id_generation() {
        let uuid = IdGenerator::uuid();
        assert_eq!(uuid.len(), 36);
        
        let short_id = IdGenerator::short_id();
        assert_eq!(short_id.len(), 8);
        
        let prefixed_id = IdGenerator::prefixed_id("test");
        assert!(prefixed_id.starts_with("test-"));
        assert_eq!(prefixed_id.len(), 13); // "test-" + 8 chars
    }
    
    #[test]
    fn test_config_validation() {
        assert!(ConfigValidator::validate_probability(0.5, "test").is_ok());
        assert!(ConfigValidator::validate_probability(-0.1, "test").is_err());
        assert!(ConfigValidator::validate_probability(1.1, "test").is_err());
        
        assert!(ConfigValidator::validate_positive(1.0, "test").is_ok());
        assert!(ConfigValidator::validate_positive(-1.0, "test").is_err());
        assert!(ConfigValidator::validate_positive(0.0, "test").is_err());
        
        assert!(ConfigValidator::validate_non_empty_string("test", "field").is_ok());
        assert!(ConfigValidator::validate_non_empty_string("", "field").is_err());
        assert!(ConfigValidator::validate_non_empty_string("   ", "field").is_err());
    }
    
    #[test]
    fn test_size_formatting() {
        assert_eq!(SizeFormatter::format_bytes(0), "0 B");
        assert_eq!(SizeFormatter::format_bytes(1024), "1.00 KB");
        assert_eq!(SizeFormatter::format_bytes(1024 * 1024), "1.00 MB");
        assert_eq!(SizeFormatter::format_bytes(1536), "1.50 KB");
        
        assert_eq!(SizeFormatter::format_duration(500), "500ms");
        assert_eq!(SizeFormatter::format_duration(1500), "1.50s");
        assert_eq!(SizeFormatter::format_duration(90000), "1.50m");
    }
    
    #[test]
    fn test_performance_timer() {
        let timer = PerformanceTimer::start("test_operation");
        std::thread::sleep(std::time::Duration::from_millis(10));
        let elapsed = timer.elapsed();
        assert!(elapsed >= 10);
        
        let duration = timer.finish();
        assert!(duration >= 10);
    }
    
    #[test]
    fn test_system_info() {
        let info = SystemInfo::new();
        assert_eq!(info.crate_name, CRATE_NAME);
        assert_eq!(info.version, VERSION);
        assert!(!info.features.is_empty());
    }
    
    #[test]
    fn test_data_serialization() {
        #[derive(Serialize, Deserialize, PartialEq, Debug)]
        struct TestData {
            name: String,
            value: i32,
        }
        
        let data = TestData {
            name: "test".to_string(),
            value: 42,
        };
        
        let json = DataSerializer::to_json(&data).unwrap();
        let deserialized: TestData = DataSerializer::from_json(&json).unwrap();
        assert_eq!(data, deserialized);
        
        let bytes = DataSerializer::to_bytes(&data).unwrap();
        let from_bytes: TestData = DataSerializer::from_bytes(&bytes).unwrap();
        assert_eq!(data, from_bytes);
    }
}

