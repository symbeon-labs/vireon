use crate::error::{SageXError, Result};

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum RuleType {
    Language,
    Framework,
    Architecture,
    Workflow,
    Symbiotic,
    TextPattern,
    Regex,
    JavaScript,
    Python,
    JsonPath,
    Conditional,
}