//! # Sistema de Erros
//!
//! Este módulo define tipos de erro personalizados para a crate symbiotic_method,
//! fornecendo tratamento de erros robusto e informações detalhadas para debug.

use pyo3::prelude::*;
use std::fmt;
use thiserror::Error;

/// Tipos de erro principais do sistema simbiótico
#[derive(Error, Debug)]
pub enum SymbioticError {
    #[error("Erro de consciência: {message}")]
    ConsciousnessError { message: String },
    
    #[error("Erro quântico: {message}")]
    QuantumError { message: String },
    
    #[error("Erro de memória quântica: {message}")]
    QuantumMemoryError { message: String },
    
    #[error("Erro do IRIS: {message}")]
    IrisError { message: String },
    
    #[error("Erro de configuração: {message}")]
    ConfigurationError { message: String },
    
    #[error("Erro de serialização: {source}")]
    SerializationError {
        #[from]
        source: serde_json::Error,
    },
    
    #[error("Erro de Python: {message}")]
    PythonError { message: String },
    
    #[error("Erro de IO: {source}")]
    IoError {
        #[from]
        source: std::io::Error,
    },
    
    #[error("Erro de integração: {component} - {message}")]
    IntegrationError { component: String, message: String },
    
    #[error("Erro de validação: {field} - {message}")]
    ValidationError { field: String, message: String },
    
    #[error("Erro interno: {message}")]
    InternalError { message: String },
}

impl SymbioticError {
    /// Cria um novo erro de consciência
    pub fn consciousness_error(message: impl Into<String>) -> Self {
        Self::ConsciousnessError {
            message: message.into(),
        }
    }
    
    /// Cria um novo erro quântico
    pub fn quantum_error(message: impl Into<String>) -> Self {
        Self::QuantumError {
            message: message.into(),
        }
    }
    
    /// Cria um novo erro de memória quântica
    pub fn quantum_memory_error(message: impl Into<String>) -> Self {
        Self::QuantumMemoryError {
            message: message.into(),
        }
    }
    
    /// Cria um novo erro do IRIS
    pub fn iris_error(message: impl Into<String>) -> Self {
        Self::IrisError {
            message: message.into(),
        }
    }
    
    /// Cria um novo erro de configuração
    pub fn configuration_error(message: impl Into<String>) -> Self {
        Self::ConfigurationError {
            message: message.into(),
        }
    }
    
    /// Cria um novo erro de Python
    pub fn python_error(message: impl Into<String>) -> Self {
        Self::PythonError {
            message: message.into(),
        }
    }
    
    /// Cria um novo erro de integração
    pub fn integration_error(component: impl Into<String>, message: impl Into<String>) -> Self {
        Self::IntegrationError {
            component: component.into(),
            message: message.into(),
        }
    }
    
    /// Cria um novo erro de validação
    pub fn validation_error(field: impl Into<String>, message: impl Into<String>) -> Self {
        Self::ValidationError {
            field: field.into(),
            message: message.into(),
        }
    }
    
    /// Cria um novo erro interno
    pub fn internal_error(message: impl Into<String>) -> Self {
        Self::InternalError {
            message: message.into(),
        }
    }
    
    /// Obtém o tipo do erro como string
    pub fn error_type(&self) -> &'static str {
        match self {
            Self::ConsciousnessError { .. } => "ConsciousnessError",
            Self::QuantumError { .. } => "QuantumError",
            Self::QuantumMemoryError { .. } => "QuantumMemoryError",
            Self::IrisError { .. } => "IrisError",
            Self::ConfigurationError { .. } => "ConfigurationError",
            Self::SerializationError { .. } => "SerializationError",
            Self::PythonError { .. } => "PythonError",
            Self::IoError { .. } => "IoError",
            Self::IntegrationError { .. } => "IntegrationError",
            Self::ValidationError { .. } => "ValidationError",
            Self::InternalError { .. } => "InternalError",
        }
    }
    
    /// Verifica se o erro é recuperável
    pub fn is_recoverable(&self) -> bool {
        match self {
            Self::ConsciousnessError { .. } => true,
            Self::QuantumError { .. } => true,
            Self::QuantumMemoryError { .. } => true,
            Self::IrisError { .. } => true,
            Self::ConfigurationError { .. } => false,
            Self::SerializationError { .. } => false,
            Self::PythonError { .. } => true,
            Self::IoError { .. } => true,
            Self::IntegrationError { .. } => true,
            Self::ValidationError { .. } => false,
            Self::InternalError { .. } => false,
        }
    }
    
    /// Obtém a severidade do erro
    pub fn severity(&self) -> ErrorSeverity {
        match self {
            Self::ConsciousnessError { .. } => ErrorSeverity::Medium,
            Self::QuantumError { .. } => ErrorSeverity::High,
            Self::QuantumMemoryError { .. } => ErrorSeverity::High,
            Self::IrisError { .. } => ErrorSeverity::Medium,
            Self::ConfigurationError { .. } => ErrorSeverity::Low,
            Self::SerializationError { .. } => ErrorSeverity::Low,
            Self::PythonError { .. } => ErrorSeverity::Medium,
            Self::IoError { .. } => ErrorSeverity::Medium,
            Self::IntegrationError { .. } => ErrorSeverity::High,
            Self::ValidationError { .. } => ErrorSeverity::Low,
            Self::InternalError { .. } => ErrorSeverity::Critical,
        }
    }
}

/// Níveis de severidade de erro
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ErrorSeverity {
    Low,
    Medium,
    High,
    Critical,
}

impl fmt::Display for ErrorSeverity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Low => write!(f, "LOW"),
            Self::Medium => write!(f, "MEDIUM"),
            Self::High => write!(f, "HIGH"),
            Self::Critical => write!(f, "CRITICAL"),
        }
    }
}

/// Converte SymbioticError para PyErr
impl From<SymbioticError> for PyErr {
    fn from(err: SymbioticError) -> Self {
        match err {
            SymbioticError::ConsciousnessError { message } => {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Consciousness Error: {}", message))
            }
            SymbioticError::QuantumError { message } => {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Quantum Error: {}", message))
            }
            SymbioticError::QuantumMemoryError { message } => {
                PyErr::new::<pyo3::exceptions::PyMemoryError, _>(format!("Quantum Memory Error: {}", message))
            }
            SymbioticError::IrisError { message } => {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("IRIS Error: {}", message))
            }
            SymbioticError::ConfigurationError { message } => {
                PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Configuration Error: {}", message))
            }
            SymbioticError::SerializationError { source } => {
                PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Serialization Error: {}", source))
            }
            SymbioticError::PythonError { message } => {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Python Error: {}", message))
            }
            SymbioticError::IoError { source } => {
                PyErr::new::<pyo3::exceptions::PyIOError, _>(format!("IO Error: {}", source))
            }
            SymbioticError::IntegrationError { component, message } => {
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Integration Error [{}]: {}", component, message))
            }
            SymbioticError::ValidationError { field, message } => {
                PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Validation Error [{}]: {}", field, message))
            }
            SymbioticError::InternalError { message } => {
                PyErr::new::<pyo3::exceptions::PySystemError, _>(format!("Internal Error: {}", message))
            }
        }
    }
}

/// Resultado customizado para operações simbióticas
pub type SymbioticResult<T> = Result<T, SymbioticError>;

/// Contexto de erro para rastreamento detalhado
#[derive(Debug, Clone)]
pub struct ErrorContext {
    pub operation: String,
    pub component: String,
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub details: std::collections::HashMap<String, String>,
}

impl ErrorContext {
    /// Cria um novo contexto de erro
    pub fn new(operation: impl Into<String>, component: impl Into<String>) -> Self {
        Self {
            operation: operation.into(),
            component: component.into(),
            timestamp: chrono::Utc::now(),
            details: std::collections::HashMap::new(),
        }
    }
    
    /// Adiciona um detalhe ao contexto
    pub fn with_detail(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.details.insert(key.into(), value.into());
        self
    }
    
    /// Adiciona múltiplos detalhes ao contexto
    pub fn with_details(mut self, details: std::collections::HashMap<String, String>) -> Self {
        self.details.extend(details);
        self
    }
}

/// Trait para adição de contexto a erros
pub trait WithContext<T> {
    fn with_context(self, context: ErrorContext) -> SymbioticResult<T>;
    fn with_simple_context(self, operation: &str, component: &str) -> SymbioticResult<T>;
}

impl<T, E> WithContext<T> for Result<T, E>
where
    E: Into<SymbioticError>,
{
    fn with_context(self, _context: ErrorContext) -> SymbioticResult<T> {
        self.map_err(|e| e.into())
    }
    
    fn with_simple_context(self, _operation: &str, _component: &str) -> SymbioticResult<T> {
        self.map_err(|e| e.into())
    }
}

/// Macro para criação rápida de erros
#[macro_export]
macro_rules! symbiotic_error {
    (consciousness, $msg:expr) => {
        $crate::error::SymbioticError::consciousness_error($msg)
    };
    (quantum, $msg:expr) => {
        $crate::error::SymbioticError::quantum_error($msg)
    };
    (quantum_memory, $msg:expr) => {
        $crate::error::SymbioticError::quantum_memory_error($msg)
    };
    (iris, $msg:expr) => {
        $crate::error::SymbioticError::iris_error($msg)
    };
    (config, $msg:expr) => {
        $crate::error::SymbioticError::configuration_error($msg)
    };
    (python, $msg:expr) => {
        $crate::error::SymbioticError::python_error($msg)
    };
    (integration, $component:expr, $msg:expr) => {
        $crate::error::SymbioticError::integration_error($component, $msg)
    };
    (validation, $field:expr, $msg:expr) => {
        $crate::error::SymbioticError::validation_error($field, $msg)
    };
    (internal, $msg:expr) => {
        $crate::error::SymbioticError::internal_error($msg)
    };
}

/// Função utilitária para criar PyResult
pub fn py_result<T>(result: SymbioticResult<T>) -> PyResult<T> {
    result.map_err(|e| e.into())
}

/// Função utilitária para capturar panics e converter em erros
pub fn catch_panic<F, T>(f: F) -> SymbioticResult<T>
where
    F: FnOnce() -> T + std::panic::UnwindSafe,
{
    std::panic::catch_unwind(f)
        .map_err(|panic_info| {
            let message = if let Some(s) = panic_info.downcast_ref::<&str>() {
                s.to_string()
            } else if let Some(s) = panic_info.downcast_ref::<String>() {
                s.clone()
            } else {
                "Unknown panic occurred".to_string()
            };
            SymbioticError::internal_error(format!("Panic caught: {}", message))
        })
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_error_creation() {
        let err = SymbioticError::consciousness_error("Test error");
        assert_eq!(err.error_type(), "ConsciousnessError");
        assert!(err.is_recoverable());
        assert_eq!(err.severity(), ErrorSeverity::Medium);
    }
    
    #[test]
    fn test_error_context() {
        let context = ErrorContext::new("test_operation", "test_component")
            .with_detail("key1", "value1")
            .with_detail("key2", "value2");
        
        assert_eq!(context.operation, "test_operation");
        assert_eq!(context.component, "test_component");
        assert_eq!(context.details.len(), 2);
        assert_eq!(context.details.get("key1"), Some(&"value1".to_string()));
    }
    
    #[test]
    fn test_symbiotic_error_macro() {
        let err = symbiotic_error!(consciousness, "Test consciousness error");
        assert!(matches!(err, SymbioticError::ConsciousnessError { .. }));
        
        let err = symbiotic_error!(integration, "TestComponent", "Integration failed");
        assert!(matches!(err, SymbioticError::IntegrationError { .. }));
    }
    
    #[test]
    fn test_error_severity_ordering() {
        assert!(ErrorSeverity::Low < ErrorSeverity::Medium);
        assert!(ErrorSeverity::Medium < ErrorSeverity::High);
        assert!(ErrorSeverity::High < ErrorSeverity::Critical);
    }
    
    #[test]
    fn test_catch_panic() {
        let result = catch_panic(|| {
            panic!("Test panic");
        });
        
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(matches!(err, SymbioticError::InternalError { .. }));
        assert!(err.to_string().contains("Panic caught"));
    }
    
    #[test]
    fn test_pyerr_conversion() {
        let err = SymbioticError::consciousness_error("Test error");
        let py_err: PyErr = err.into();
        let py_err_string = format!("{:?}", py_err);
        assert!(py_err_string.contains("Consciousness Error"));
    }
}

