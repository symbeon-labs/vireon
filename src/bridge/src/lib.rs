//! VIREON BRIDGE Module
use anyhow::Result;
use tracing::info;

pub fn init() -> Result<()> {
    info!("Initializing VIREON BRIDGE");
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_init() {
        assert!(init().is_ok());
    }
}
