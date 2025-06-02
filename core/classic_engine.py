import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
import sqlite3
from contextlib import contextmanager

@dataclass
class ProcessingMetrics:
    """Métricas de processamento clássico"""
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    avg_processing_time: float = 0.0
    pattern_matches: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    
    def update_processing_time(self, processing_time: float):
        self.avg_processing_time = (
            (self.avg_processing_time * self.total_operations + processing_time)
            / (self.total_operations + 1)
        )
        self.total_operations += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_operations": self.total_operations,
            "success_rate": self.successful_operations / max(self.total_operations, 1),
            "avg_processing_time": self.avg_processing_time,
            "pattern_recognition_rate": self.pattern_matches / max(self.total_operations, 1),
            "cache_hit_rate": self.cache_hits / max(self.cache_hits + self.cache_misses, 1)
        }

class SimpleCache:
    """Cache básico com expiração"""
    
    def __init__(self, max_size: int = 1000):
        self.data: Dict[str, Any] = {}
        self.expiry: Dict[str, datetime] = {}
        self.max_size = max_size

    def get(self, key: str) -> Optional[Any]:
        """Recupera item do cache"""
        if key in self.data:
            if datetime.now() > self.expiry[key]:
                del self.data[key]
                del self.expiry[key]
                return None
            return self.data[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Armazena item no cache"""
        if len(self.data) >= self.max_size:
            # Remove item mais antigo
            oldest = min(self.expiry.items(), key=lambda x: x[1])[0]
            del self.data[oldest]
            del self.expiry[oldest]
        
        self.data[key] = value
        self.expiry[key] = datetime.now() + timedelta(seconds=ttl_seconds)

class PatternAnalyzer:
    """Analisador de padrões clássico"""
    
    def __init__(self):
        self.patterns: Dict[str, int] = {}
        self.threshold = 0.8

    def analyze(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Analisa padrões nos dados"""
        results = {}
        
        # Análise básica de frequência
        for key, value in data.items():
            pattern_key = f"{key}:{str(value)}"
            self.patterns[pattern_key] = self.patterns.get(pattern_key, 0) + 1
            
            # Calcula confiança do padrão
            total = sum(self.patterns.values())
            confidence = self.patterns[pattern_key] / total
            if confidence > self.threshold:
                results[pattern_key] = confidence
                
        return results

class ClassicCognitiveEngine:
    """Motor cognitivo clássico com processamento síncrono"""
    
    def __init__(
        self,
        cache_size: int = 1000,
        db_path: str = "cognitive_data.db"
    ):
        self.cache = SimpleCache(max_size=cache_size)
        self.pattern_analyzer = PatternAnalyzer()
        self.metrics = ProcessingMetrics()
        self.db_path = db_path
        self.logger = logging.getLogger("ClassicCognitiveEngine")
        self.logger.setLevel(logging.INFO)
        
        # Inicializa banco de dados
        self._init_db()

    def _init_db(self):
        """Inicializa banco de dados SQLite"""
        with self._get_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cognitive_data (
                    id TEXT PRIMARY KEY,
                    data JSON,
                    patterns JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    @contextmanager
    def _get_db(self):
        """Gerencia conexão com banco de dados"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Processa dados de entrada"""
        start_time = time.time()
        
        try:
            # Verifica cache
            cache_key = self._generate_cache_key(input_data)
            cached_result = self.cache.get(cache_key)
            
            if cached_result:
                self.metrics.cache_hits += 1
                self.logger.info("Cache hit")
                return cached_result
            
            self.metrics.cache_misses += 1
            
            # Análise de padrões
            patterns = self.pattern_analyzer.analyze(input_data)
            if patterns:
                self.metrics.pattern_matches += 1
                
            # Processamento principal
            processed_data = {
                "input": input_data,
                "patterns": patterns,
                "processing_info": {
                    "timestamp": datetime.now().isoformat(),
                    "confidence": sum(patterns.values()) / len(patterns) if patterns else 0
                }
            }
            
            # Armazena resultado
            self._store_result(processed_data)
            
            # Atualiza cache
            self.cache.set(cache_key, processed_data)
            
            self.metrics.successful_operations += 1
            return processed_data
            
        except Exception as e:
            self.logger.error(f"Erro no processamento: {e}")
            self.metrics.failed_operations += 1
            return {"error": str(e)}
            
        finally:
            processing_time = time.time() - start_time
            self.metrics.update_processing_time(processing_time)

    def _generate_cache_key(self, data: Dict[str, Any]) -> str:
        """Gera chave única para cache"""
        return json.dumps(data, sort_keys=True)

    def _store_result(self, data: Dict[str, Any]):
        """Armazena resultado no banco de dados"""
        with self._get_db() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cognitive_data (id, data, patterns) VALUES (?, ?, ?)",
                (
                    data["processing_info"]["timestamp"],
                    json.dumps(data["input"]),
                    json.dumps(data["patterns"])
                )
            )
            conn.commit()

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de performance"""
        return self.metrics.to_dict()

    def generate_report(self, output_dir: str = "reports"):
        """Gera relatório de performance"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        metrics = self.get_metrics()
        patterns = self.pattern_analyzer.patterns
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "patterns": {
                "total_patterns": len(patterns),
                "top_patterns": dict(sorted(
                    patterns.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10])
            }
        }
        
        with open(output_path / "cognitive_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        self.logger.info(f"Relatório gerado em {output_path}")

