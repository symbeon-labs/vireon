//! # Adaptador QuantumMemoryManager
//!
//! Este módulo implementa a interface FFI para o QuantumMemoryManager do VIREON,
//! permitindo gestão de memória quântica distribuída entre componentes Rust e Python.

use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{debug, info, warn, error};
use chrono::{DateTime, Utc};
use uuid::Uuid;

/// Tipos de bloco de memória quântica
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[pyclass]
pub enum QuantumMemoryType {
    Immediate,
    Working,
    LongTerm,
    Transcendent,
}

#[pymethods]
impl QuantumMemoryType {
    #[new]
    fn new() -> Self {
        QuantumMemoryType::Immediate
    }
    
    fn get_priority(&self) -> i32 {
        match self {
            QuantumMemoryType::Transcendent => 4,
            QuantumMemoryType::LongTerm => 3,
            QuantumMemoryType::Working => 2,
            QuantumMemoryType::Immediate => 1,
        }
    }
    
    fn get_retention_time(&self) -> f64 {
        match self {
            QuantumMemoryType::Immediate => 60.0,        // 1 minuto
            QuantumMemoryType::Working => 3600.0,       // 1 hora
            QuantumMemoryType::LongTerm => 86400.0,     // 1 dia
            QuantumMemoryType::Transcendent => f64::INFINITY, // Permanente
        }
    }
    
    fn __str__(&self) -> String {
        format!("{:?}", self)
    }
    
    fn __repr__(&self) -> String {
        format!("QuantumMemoryType::{:?}", self)
    }
}

/// Estado de coerência quântica
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
#[pyclass]
pub enum CoherenceState {
    Coherent,
    Decoherent,
    Superposition,
    Entangled,
    Collapsed,
}

#[pymethods]
impl CoherenceState {
    #[new]
    fn new() -> Self {
        CoherenceState::Coherent
    }
    
    fn is_stable(&self) -> bool {
        matches!(self, CoherenceState::Coherent | CoherenceState::Entangled)
    }
    
    fn __str__(&self) -> String {
        format!("{:?}", self)
    }
    
    fn __repr__(&self) -> String {
        format!("CoherenceState::{:?}", self)
    }
}

/// Bloco de memória quântica
#[derive(Debug, Clone, Serialize, Deserialize)]
#[pyclass]
pub struct QuantumMemoryBlock {
    #[pyo3(get, set)]
    pub id: String,
    #[pyo3(get, set)]
    pub memory_type: QuantumMemoryType,
    #[pyo3(get, set)]
    pub coherence_state: CoherenceState,
    #[pyo3(get, set)]
    pub data: String,
    #[pyo3(get, set)]
    pub size: usize,
    #[pyo3(get, set)]
    pub created_at: String,
    #[pyo3(get, set)]
    pub last_accessed: String,
    #[pyo3(get, set)]
    pub access_count: u64,
    #[pyo3(get, set)]
    pub quantum_signature: String,
    #[pyo3(get, set)]
    pub entanglement_refs: Vec<String>,
}

#[pymethods]
impl QuantumMemoryBlock {
    #[new]
    fn new(data: String, memory_type: QuantumMemoryType) -> Self {
        let now = Utc::now().to_rfc3339();
        Self {
            id: Uuid::new_v4().to_string(),
            memory_type,
            coherence_state: CoherenceState::Coherent,
            size: data.len(),
            data,
            created_at: now.clone(),
            last_accessed: now,
            access_count: 0,
            quantum_signature: Uuid::new_v4().to_string(),
            entanglement_refs: Vec::new(),
        }
    }
    
    fn access(&mut self) {
        self.last_accessed = Utc::now().to_rfc3339();
        self.access_count += 1;
    }
    
    fn add_entanglement(&mut self, block_id: String) {
        if !self.entanglement_refs.contains(&block_id) {
            self.entanglement_refs.push(block_id);
            self.coherence_state = CoherenceState::Entangled;
        }
    }
    
    fn remove_entanglement(&mut self, block_id: String) {
        self.entanglement_refs.retain(|id| id != &block_id);
        if self.entanglement_refs.is_empty() {
            self.coherence_state = CoherenceState::Coherent;
        }
    }
    
    fn is_entangled(&self) -> bool {
        !self.entanglement_refs.is_empty()
    }
    
    fn update_data(&mut self, new_data: String) {
        self.data = new_data;
        self.size = self.data.len();
        self.last_accessed = Utc::now().to_rfc3339();
        self.quantum_signature = Uuid::new_v4().to_string();
    }
    
    fn set_coherence_state(&mut self, state: CoherenceState) {
        self.coherence_state = state;
    }
    
    fn get_age_seconds(&self) -> f64 {
        let created = DateTime::parse_from_rfc3339(&self.created_at)
            .unwrap_or_else(|_| Utc::now().into());
        let now = Utc::now();
        (now - created).num_seconds() as f64
    }
    
    fn should_expire(&self) -> bool {
        let retention_time = self.memory_type.get_retention_time();
        if retention_time.is_infinite() {
            return false;
        }
        self.get_age_seconds() > retention_time
    }
    
    fn to_dict(&self) -> HashMap<String, PyObject> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        
        let mut result = HashMap::new();
        result.insert("id".to_string(), self.id.to_object(py));
        result.insert("memory_type".to_string(), format!("{:?}", self.memory_type).to_object(py));
        result.insert("coherence_state".to_string(), format!("{:?}", self.coherence_state).to_object(py));
        result.insert("data".to_string(), self.data.to_object(py));
        result.insert("size".to_string(), self.size.to_object(py));
        result.insert("created_at".to_string(), self.created_at.to_object(py));
        result.insert("last_accessed".to_string(), self.last_accessed.to_object(py));
        result.insert("access_count".to_string(), self.access_count.to_object(py));
        result.insert("quantum_signature".to_string(), self.quantum_signature.to_object(py));
        result.insert("entanglement_refs".to_string(), self.entanglement_refs.to_object(py));
        result.insert("age_seconds".to_string(), self.get_age_seconds().to_object(py));
        result.insert("should_expire".to_string(), self.should_expire().to_object(py));
        result
    }
    
    fn __str__(&self) -> String {
        format!(
            "QuantumMemoryBlock(id={}, type={:?}, size={}, age={:.1}s)",
            &self.id[..8],
            self.memory_type,
            self.size,
            self.get_age_seconds()
        )
    }
    
    fn __repr__(&self) -> String {
        format!(
            "QuantumMemoryBlock(id='{}', memory_type={:?}, coherence_state={:?}, size={}, entangled={})",
            self.id,
            self.memory_type,
            self.coherence_state,
            self.size,
            self.is_entangled()
        )
    }
}

/// Estatísticas de memória quântica
#[derive(Debug, Clone, Default)]
struct QuantumMemoryStats {
    total_blocks: u64,
    total_size: u64,
    blocks_by_type: HashMap<String, u64>,
    total_accesses: u64,
    cache_hits: u64,
    cache_misses: u64,
    gc_operations: u64,
    entanglement_count: u64,
}

/// Adaptador principal para QuantumMemoryManager
#[derive(Debug)]
#[pyclass]
pub struct QuantumMemoryAdapter {
    memory_blocks: Arc<RwLock<HashMap<String, QuantumMemoryBlock>>>,
    memory_index: Arc<RwLock<HashMap<String, Vec<String>>>>, // tipo -> IDs
    stats: Arc<RwLock<QuantumMemoryStats>>,
    max_memory_size: usize,
    current_size: Arc<RwLock<usize>>,
    gc_enabled: Arc<RwLock<bool>>,
    active: Arc<RwLock<bool>>,
}

#[pymethods]
impl QuantumMemoryAdapter {
    #[new]
    fn new(max_memory_size: Option<usize>) -> Self {
        let max_size = max_memory_size.unwrap_or(1_000_000_000); // 1GB padrão
        info!("Inicializando QuantumMemoryAdapter com limite de {} bytes", max_size);
        
        Self {
            memory_blocks: Arc::new(RwLock::new(HashMap::new())),
            memory_index: Arc::new(RwLock::new(HashMap::new())),
            stats: Arc::new(RwLock::new(QuantumMemoryStats::default())),
            max_memory_size: max_size,
            current_size: Arc::new(RwLock::new(0)),
            gc_enabled: Arc::new(RwLock::new(true)),
            active: Arc::new(RwLock::new(false)),
        }
    }
    
    /// Ativa o adaptador de memória quântica
    fn activate(&self) -> PyResult<()> {
        debug!("Ativando QuantumMemoryAdapter");
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            
            async move {
                let mut active_guard = active.write().await;
                *active_guard = true;
                info!("QuantumMemoryAdapter ativado");
            }
        })?;
        
        Ok(())
    }
    
    /// Desativa o adaptador
    fn deactivate(&self) -> PyResult<()> {
        debug!("Desativando QuantumMemoryAdapter");
        
        pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            
            async move {
                let mut active_guard = active.write().await;
                *active_guard = false;
                info!("QuantumMemoryAdapter desativado");
            }
        })?;
        
        Ok(())
    }
    
    /// Verifica se o adaptador está ativo
    fn is_active(&self) -> PyResult<bool> {
        let result = pyo3_asyncio::run_in_async_thread({
            let active = Arc::clone(&self.active);
            async move {
                let active_guard = active.read().await;
                *active_guard
            }
        })?;
        Ok(result)
    }
    
    /// Armazena um bloco de memória quântica
    fn store_block(&self, block: QuantumMemoryBlock) -> PyResult<String> {
        debug!("Armazenando bloco de memória: {}", block.id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let memory_blocks = Arc::clone(&self.memory_blocks);
            let memory_index = Arc::clone(&self.memory_index);
            let stats = Arc::clone(&self.stats);
            let current_size = Arc::clone(&self.current_size);
            let max_size = self.max_memory_size;
            
            async move {
                let mut blocks_guard = memory_blocks.write().await;
                let mut index_guard = memory_index.write().await;
                let mut stats_guard = stats.write().await;
                let mut size_guard = current_size.write().await;
                
                // Verificar limite de memória
                if *size_guard + block.size > max_size {
                    warn!("Limite de memória excedido ao tentar armazenar bloco");
                    return None;
                }
                
                let block_id = block.id.clone();
                let memory_type = format!("{:?}", block.memory_type);
                
                // Atualizar estatísticas
                stats_guard.total_blocks += 1;
                stats_guard.total_size += block.size as u64;
                *stats_guard.blocks_by_type.entry(memory_type.clone()).or_insert(0) += 1;
                
                // Atualizar tamanho atual
                *size_guard += block.size;
                
                // Adicionar ao índice
                index_guard.entry(memory_type).or_insert_with(Vec::new).push(block_id.clone());
                
                // Armazenar bloco
                blocks_guard.insert(block_id.clone(), block);
                
                info!("Bloco de memória armazenado: {}", block_id);
                Some(block_id)
            }
        })?;
        
        result.ok_or_else(|| PyErr::new::<pyo3::exceptions::PyMemoryError, _>("Falha ao armazenar bloco"))
    }
    
    /// Recupera um bloco de memória quântica
    fn retrieve_block(&self, block_id: String) -> PyResult<Option<QuantumMemoryBlock>> {
        debug!("Recuperando bloco de memória: {}", block_id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let memory_blocks = Arc::clone(&self.memory_blocks);
            let stats = Arc::clone(&self.stats);
            
            async move {
                let mut blocks_guard = memory_blocks.write().await;
                let mut stats_guard = stats.write().await;
                
                stats_guard.total_accesses += 1;
                
                if let Some(mut block) = blocks_guard.get_mut(&block_id) {
                    block.access();
                    stats_guard.cache_hits += 1;
                    debug!("Bloco encontrado e acessado: {}", block_id);
                    Some(block.clone())
                } else {
                    stats_guard.cache_misses += 1;
                    debug!("Bloco não encontrado: {}", block_id);
                    None
                }
            }
        })?;
        
        Ok(result)
    }
    
    /// Remove um bloco de memória quântica
    fn remove_block(&self, block_id: String) -> PyResult<bool> {
        debug!("Removendo bloco de memória: {}", block_id);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let memory_blocks = Arc::clone(&self.memory_blocks);
            let memory_index = Arc::clone(&self.memory_index);
            let stats = Arc::clone(&self.stats);
            let current_size = Arc::clone(&self.current_size);
            
            async move {
                let mut blocks_guard = memory_blocks.write().await;
                let mut index_guard = memory_index.write().await;
                let mut stats_guard = stats.write().await;
                let mut size_guard = current_size.write().await;
                
                if let Some(block) = blocks_guard.remove(&block_id) {
                    let memory_type = format!("{:?}", block.memory_type);
                    
                    // Atualizar estatísticas
                    stats_guard.total_blocks -= 1;
                    stats_guard.total_size -= block.size as u64;
                    if let Some(count) = stats_guard.blocks_by_type.get_mut(&memory_type) {
                        *count -= 1;
                    }
                    
                    // Atualizar tamanho atual
                    *size_guard -= block.size;
                    
                    // Remover do índice
                    if let Some(type_blocks) = index_guard.get_mut(&memory_type) {
                        type_blocks.retain(|id| id != &block_id);
                    }
                    
                    info!("Bloco de memória removido: {}", block_id);
                    true
                } else {
                    warn!("Tentativa de remover bloco inexistente: {}", block_id);
                    false
                }
            }
        })?;
        
        Ok(result)
    }
    
    /// Lista blocos por tipo de memória
    fn list_blocks_by_type(&self, memory_type: QuantumMemoryType) -> PyResult<Vec<String>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let memory_index = Arc::clone(&self.memory_index);
            
            async move {
                let index_guard = memory_index.read().await;
                let type_key = format!("{:?}", memory_type);
                index_guard.get(&type_key).cloned().unwrap_or_default()
            }
        })?;
        
        Ok(result)
    }
    
    /// Executa garbage collection
    fn garbage_collect(&self) -> PyResult<u64> {
        debug!("Executando garbage collection");
        
        let result = pyo3_asyncio::run_in_async_thread({
            let memory_blocks = Arc::clone(&self.memory_blocks);
            let memory_index = Arc::clone(&self.memory_index);
            let stats = Arc::clone(&self.stats);
            let current_size = Arc::clone(&self.current_size);
            let gc_enabled = Arc::clone(&self.gc_enabled);
            
            async move {
                let gc_enabled_guard = gc_enabled.read().await;
                if !*gc_enabled_guard {
                    return 0;
                }
                drop(gc_enabled_guard);
                
                let mut blocks_guard = memory_blocks.write().await;
                let mut index_guard = memory_index.write().await;
                let mut stats_guard = stats.write().await;
                let mut size_guard = current_size.write().await;
                
                let mut removed_count = 0;
                let mut blocks_to_remove = Vec::new();
                
                // Identificar blocos expirados
                for (id, block) in blocks_guard.iter() {
                    if block.should_expire() {
                        blocks_to_remove.push((id.clone(), block.clone()));
                    }
                }
                
                // Remover blocos expirados
                for (block_id, block) in blocks_to_remove {
                    blocks_guard.remove(&block_id);
                    
                    let memory_type = format!("{:?}", block.memory_type);
                    
                    // Atualizar estatísticas
                    stats_guard.total_blocks -= 1;
                    stats_guard.total_size -= block.size as u64;
                    if let Some(count) = stats_guard.blocks_by_type.get_mut(&memory_type) {
                        *count -= 1;
                    }
                    
                    // Atualizar tamanho atual
                    *size_guard -= block.size;
                    
                    // Remover do índice
                    if let Some(type_blocks) = index_guard.get_mut(&memory_type) {
                        type_blocks.retain(|id| id != &block_id);
                    }
                    
                    removed_count += 1;
                }
                
                stats_guard.gc_operations += 1;
                
                if removed_count > 0 {
                    info!("Garbage collection removeu {} blocos", removed_count);
                } else {
                    debug!("Garbage collection não encontrou blocos para remover");
                }
                
                removed_count
            }
        })?;
        
        Ok(result)
    }
    
    /// Cria emaranhamento entre dois blocos
    fn entangle_blocks(&self, block_id1: String, block_id2: String) -> PyResult<bool> {
        debug!("Criando emaranhamento entre blocos: {} e {}", block_id1, block_id2);
        
        let result = pyo3_asyncio::run_in_async_thread({
            let memory_blocks = Arc::clone(&self.memory_blocks);
            let stats = Arc::clone(&self.stats);
            
            async move {
                let mut blocks_guard = memory_blocks.write().await;
                let mut stats_guard = stats.write().await;
                
                let mut success = false;
                
                if let (Some(block1), Some(block2)) = 
                    (blocks_guard.get_mut(&block_id1), blocks_guard.get_mut(&block_id2)) {
                    
                    block1.add_entanglement(block_id2.clone());
                    block2.add_entanglement(block_id1.clone());
                    
                    stats_guard.entanglement_count += 1;
                    success = true;
                    
                    info!("Emaranhamento criado entre {} e {}", block_id1, block_id2);
                } else {
                    warn!("Falha ao criar emaranhamento: um ou ambos os blocos não existem");
                }
                
                success
            }
        })?;
        
        Ok(result)
    }
    
    /// Obtém estatísticas de memória
    fn get_stats(&self) -> PyResult<HashMap<String, PyObject>> {
        let result = pyo3_asyncio::run_in_async_thread({
            let stats = Arc::clone(&self.stats);
            let current_size = Arc::clone(&self.current_size);
            
            async move {
                let stats_guard = stats.read().await;
                let size_guard = current_size.read().await;
                
                let gil = Python::acquire_gil();
                let py = gil.python();
                
                let mut result = HashMap::new();
                result.insert("total_blocks".to_string(), stats_guard.total_blocks.to_object(py));
                result.insert("total_size".to_string(), stats_guard.total_size.to_object(py));
                result.insert("current_size".to_string(), (*size_guard).to_object(py));
                result.insert("total_accesses".to_string(), stats_guard.total_accesses.to_object(py));
                result.insert("cache_hits".to_string(), stats_guard.cache_hits.to_object(py));
                result.insert("cache_misses".to_string(), stats_guard.cache_misses.to_object(py));
                result.insert("gc_operations".to_string(), stats_guard.gc_operations.to_object(py));
                result.insert("entanglement_count".to_string(), stats_guard.entanglement_count.to_object(py));
                
                let hit_rate = if stats_guard.total_accesses > 0 {
                    stats_guard.cache_hits as f64 / stats_guard.total_accesses as f64
                } else {
                    0.0
                };
                result.insert("cache_hit_rate".to_string(), hit_rate.to_object(py));
                
                for (mem_type, count) in &stats_guard.blocks_by_type {
                    result.insert(format!("blocks_{}", mem_type.to_lowercase()), count.to_object(py));
                }
                
                result
            }
        })?;
        
        Ok(result)
    }
    
    /// Define o limite de memória
    fn set_memory_limit(&mut self, limit: usize) -> PyResult<()> {
        self.max_memory_size = limit;
        info!("Limite de memória atualizado para: {} bytes", limit);
        Ok(())
    }
    
    /// Ativa/desativa garbage collection
    fn set_gc_enabled(&self, enabled: bool) -> PyResult<()> {
        pyo3_asyncio::run_in_async_thread({
            let gc_enabled = Arc::clone(&self.gc_enabled);
            
            async move {
                let mut gc_guard = gc_enabled.write().await;
                *gc_guard = enabled;
                info!("Garbage collection {}", if enabled { "ativado" } else { "desativado" });
            }
        })?;
        
        Ok(())
    }
    
    /// Limpa toda a memória
    fn clear_all(&self) -> PyResult<()> {
        debug!("Limpando toda a memória quântica");
        
        pyo3_asyncio::run_in_async_thread({
            let memory_blocks = Arc::clone(&self.memory_blocks);
            let memory_index = Arc::clone(&self.memory_index);
            let stats = Arc::clone(&self.stats);
            let current_size = Arc::clone(&self.current_size);
            
            async move {
                let mut blocks_guard = memory_blocks.write().await;
                let mut index_guard = memory_index.write().await;
                let mut stats_guard = stats.write().await;
                let mut size_guard = current_size.write().await;
                
                blocks_guard.clear();
                index_guard.clear();
                *stats_guard = QuantumMemoryStats::default();
                *size_guard = 0;
                
                info!("Toda a memória quântica foi limpa");
            }
        })?;
        
        Ok(())
    }
    
    fn get_memory_limit(&self) -> usize {
        self.max_memory_size
    }
    
    fn __str__(&self) -> String {
        format!("QuantumMemoryAdapter(limit={} bytes, active=unknown)", self.max_memory_size)
    }
    
    fn __repr__(&self) -> String {
        format!("QuantumMemoryAdapter(max_memory_size={})", self.max_memory_size)
    }
}

impl Default for QuantumMemoryAdapter {
    fn default() -> Self {
        Self::new(None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_quantum_memory_type() {
        assert_eq!(QuantumMemoryType::Transcendent.get_priority(), 4);
        assert_eq!(QuantumMemoryType::Immediate.get_priority(), 1);
        assert!(QuantumMemoryType::Transcendent.get_retention_time().is_infinite());
    }
    
    #[test]
    fn test_coherence_state() {
        assert!(CoherenceState::Coherent.is_stable());
        assert!(CoherenceState::Entangled.is_stable());
        assert!(!CoherenceState::Decoherent.is_stable());
    }
    
    #[test]
    fn test_quantum_memory_block() {
        let mut block = QuantumMemoryBlock::new(
            "test data".to_string(),
            QuantumMemoryType::Working
        );
        
        assert_eq!(block.data, "test data");
        assert_eq!(block.size, 9);
        assert_eq!(block.access_count, 0);
        assert!(!block.is_entangled());
        
        block.access();
        assert_eq!(block.access_count, 1);
        
        block.add_entanglement("other_block".to_string());
        assert!(block.is_entangled());
        assert_eq!(block.coherence_state, CoherenceState::Entangled);
    }
    
    #[tokio::test]
    async fn test_quantum_memory_adapter() {
        let adapter = QuantumMemoryAdapter::new(Some(1000));
        
        // Testar limite de memória
        assert_eq!(adapter.get_memory_limit(), 1000);
        
        // Testar estado inicial
        let initial_size = adapter.current_size.read().await;
        assert_eq!(*initial_size, 0);
        
        let initial_blocks = adapter.memory_blocks.read().await;
        assert!(initial_blocks.is_empty());
    }
}

