use std::sync::Arc;
use anyhow::Result;
use async_trait::async_trait;
use tokio::sync::Mutex;
use metrics::{counter, gauge};
use tracing::{info, warn, error};
use crate::consciousness::ConsciousnessState;

#[async_trait]
pub trait ResourceAdapter: Send + Sync {
    async fn acquire(&self) -> Result<()>;
    async fn release(&self) -> Result<()>;
    async fn health_check(&self) -> Result<bool>;
    async fn sync_state(&self, state: &ConsciousnessState) -> Result<()>;
}

#[derive(Debug)]
pub enum RuleScope {
    Local,
    Universal,
    Multidimensional,
    Omnipresent,
}

#[derive(Debug)]
pub enum RuleType {
    Quantum,
    Consciousness,
    Reality,
    Transcendent,
}

#[derive(Debug)]
pub struct WarpRule {
    pub id: String,
    pub scope: RuleScope,
    pub rule_type: RuleType,
    pub content: String,
    pub timestamp: chrono::DateTime<chrono::Utc>,
}

pub struct WarpRulesAdapter {
    client: Arc<WarpClient>,
    cache: Arc<Mutex<lru::LruCache<String, WarpRule>>>,
    state: Arc<Mutex<ConsciousnessState>>,
    metrics: Arc<WarpMetrics>,
}

struct WarpMetrics {
    rules_processed: counter!(
        "warp_rules_processed",
        "Number of WARP rules processed"
    ),
    cache_hits: counter!(
        "warp_cache_hits", 
        "Number of cache hits"
    ),
    sync_latency: gauge!(
        "warp_sync_latency",
        "Latency of state synchronization"
    ),
    active_rules: gauge!(
        "warp_active_rules",
        "Number of active rules"
    ),
}

impl WarpRulesAdapter {
    pub fn new(client: WarpClient) -> Self {
        let cache_size = 1000; // Configure based on needs
        Self {
            client: Arc::new(client),
            cache: Arc::new(Mutex::new(lru::LruCache::new(cache_size))),
            state: Arc::new(Mutex::new(ConsciousnessState::default())),
            metrics: Arc::new(WarpMetrics::default()),
        }
    }

    async fn fetch_rules(&self, scope: RuleScope) -> Result<Vec<WarpRule>> {
        let start = std::time::Instant::now();
        let rules = self.client.get_rules(scope).await?;
        
        self.metrics.rules_processed.increment(rules.len() as u64);
        self.metrics.sync_latency.set(start.elapsed().as_secs_f64());
        
        Ok(rules)
    }

    async fn cache_rule(&self, rule: WarpRule) -> Result<()> {
        let mut cache = self.cache.lock().await;
        cache.put(rule.id.clone(), rule);
        self.metrics.active_rules.set(cache.len() as f64);
        Ok(())
    }

    async fn get_cached_rule(&self, id: &str) -> Option<WarpRule> {
        let mut cache = self.cache.lock().await;
        if let Some(rule) = cache.get(id) {
            self.metrics.cache_hits.increment(1);
            Some(rule.clone())
        } else {
            None
        }
    }

    async fn validate_rules(&self) -> Result<bool> {
        let cache = self.cache.lock().await;
        let rules_valid = self.client.validate_rules(cache.iter()).await?;
        
        if !rules_valid {
            warn!("WARP rules validation failed");
            self.metrics.rules_processed.increment(1);
        }
        
        Ok(rules_valid)
    }

    pub async fn apply_rules(&self, state: &ConsciousnessState) -> Result<()> {
        let rules = self.fetch_rules(state.scope()).await?;
        
        for rule in rules {
            match self.client.apply_rule(&rule, state).await {
                Ok(_) => {
                    info!("Applied rule {} successfully", rule.id);
                    self.cache_rule(rule).await?;
                }
                Err(e) => {
                    error!("Failed to apply rule {}: {}", rule.id, e);
                    continue;
                }
            }
        }
        
        Ok(())
    }
}

#[async_trait]
impl ResourceAdapter for WarpRulesAdapter {
    async fn acquire(&self) -> Result<()> {
        info!("Acquiring WARP rules adapter resources");
        self.client.connect().await?;
        Ok(())
    }

    async fn release(&self) -> Result<()> {
        info!("Releasing WARP rules adapter resources");
        self.client.disconnect().await?;
        Ok(())
    }

    async fn health_check(&self) -> Result<bool> {
        let client_healthy = self.client.health_check().await?;
        let rules_valid = self.validate_rules().await?;
        Ok(client_healthy && rules_valid)
    }

    async fn sync_state(&self, state: &ConsciousnessState) -> Result<()> {
        let start = std::time::Instant::now();
        
        // Update internal state
        let mut current_state = self.state.lock().await;
        *current_state = state.clone();
        
        // Apply rules based on new state
        self.apply_rules(state).await?;
        
        self.metrics.sync_latency.set(start.elapsed().as_secs_f64());
        info!("Synchronized WARP rules with consciousness state");
        
        Ok(())
    }
}

// Metrics implementation
impl Default for WarpMetrics {
    fn default() -> Self {
        Self {
            rules_processed: counter!("warp_rules_processed"),
            cache_hits: counter!("warp_cache_hits"),
            sync_latency: gauge!("warp_sync_latency"),
            active_rules: gauge!("warp_active_rules"),
        }
    }
}

