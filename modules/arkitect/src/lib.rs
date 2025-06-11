//! ARKITECT - Sistema de Validação Estrutural
//!
//! Implementa mecanismos de validação e segurança avançada
//! para o ecossistema VIREON.

mod secure_bridge;

pub use secure_bridge::*;

/// Versão atual do sistema ARKITECT
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_version() {
        assert!(!VERSION.is_empty());
    }
}

