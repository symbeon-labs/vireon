#!/usr/bin/env python
"""
Script para validar a nova estrutura do VIREON após reorganização.
Verifica integridade, dependências e configurações.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Set

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("validation.log")
    ]
)

logger = logging.getLogger("vireon.validator")

class StructureValidator:
    """Validador da estrutura do projeto VIREON."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.errors = []
        self.warnings = []
        
    def validate_directory_structure(self) -> bool:
        """Valida estrutura de diretórios."""
        required_dirs = {
            "VIREON-CORE": [
                "src/meta_governance",
                "src/api",
                "src/warp_bridge",
                "src/monitoring",
                "tests",
                "docs",
                "examples"
            ],
            "VIREON-NEURAL": [
                "research/quantum_protocols",
                "research/consciousness",
                "research/evolution",
                "prototypes",
                "docs/papers",
                "docs/experiments",
                "tests"
            ],
            "Shared": [
                "interfaces",
                "utils",
                "config"
            ]
        }
        
        success = True
        for project, dirs in required_dirs.items():
            project_path = self.base_path / project
            if not project_path.exists():
                self.errors.append(f"Projeto {project} não encontrado")
                success = False
                continue
                
            for dir_path in dirs:
                full_path = project_path / dir_path
                if not full_path.exists():
                    self.errors.append(f"Diretório {full_path} não encontrado")
                    success = False
        
        return success
    
    def validate_core_components(self) -> bool:
        """Valida componentes do VIREON-CORE."""
        required_files = [
            "src/meta_governance/rule_manager.py",
            "src/api/main.py",
            "src/warp_bridge/bridge.py",
            "src/monitoring/metrics.py",
            "README.md",
            "requirements.txt"
        ]
        
        success = True
        core_path = self.base_path / "VIREON-CORE"
        
        for file_path in required_files:
            full_path = core_path / file_path
            if not full_path.exists():
                self.errors.append(f"Arquivo core {file_path} não encontrado")
                success = False
        
        return success
    
    def validate_quantum_components(self) -> bool:
        """Valida componentes do VIREON-NEURAL."""
        required_files = [
            "research/quantum_protocols/bridge.rs",
            "research/consciousness/evolution.py",
            "research/evolution/models.py",
            "README.md",
            "requirements.txt"
        ]
        
        success = True
        quantum_path = self.base_path / "VIREON-NEURAL"
        
        for file_path in required_files:
            full_path = quantum_path / file_path
            if not full_path.exists():
                self.warnings.append(f"Arquivo neural {file_path} não encontrado")
                # Não falha para componentes experimentais
        
        return success
    
    def validate_shared_components(self) -> bool:
        """Valida componentes compartilhados."""
        required_files = [
            "interfaces/symbiotic_bridge.py",
            "utils/common.py",
            "config/settings.py"
        ]
        
        success = True
        shared_path = self.base_path / "Shared"
        
        for file_path in required_files:
            full_path = shared_path / file_path
            if not full_path.exists():
                self.errors.append(f"Arquivo compartilhado {file_path} não encontrado")
                success = False
        
        return success
    
    def validate_dependencies(self) -> bool:
        """Valida dependências entre componentes."""
        success = True
        
        # Verificar imports em arquivos Python
        python_files = list(self.base_path.rglob("*.py"))
        for file_path in python_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Verificar imports inválidos
            if "neural" in str(file_path):
                if "VIREON-CORE" in content:
                    self.warnings.append(f"Arquivo neural {file_path} importa componentes core")
                    
            if "core" in str(file_path):
                if "VIREON-NEURAL" in content:
                    self.errors.append(f"Arquivo core {file_path} importa componentes neural")
                    success = False
        
        return success
    
    def validate_configuration(self) -> bool:
        """Valida arquivos de configuração."""
        success = True
        
        config_files = {
            "VIREON-CORE/src/config.py": ["CORE_CONFIG"],
            "VIREON-NEURAL/research/config.py": ["QUANTUM_CONFIG"],
            "Shared/config/settings.py": ["SHARED_CONFIG"]
        }
        
        for file_path, required_vars in config_files.items():
            full_path = self.base_path / file_path
            if not full_path.exists():
                self.errors.append(f"Arquivo de configuração {file_path} não encontrado")
                success = False
                continue
                
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            for var in required_vars:
                if var not in content:
                    self.errors.append(f"Variável {var} não encontrada em {file_path}")
                    success = False
        
        return success
    
    def run_validation(self) -> bool:
        """Executa todas as validações."""
        logger.info("Iniciando validação da estrutura VIREON...")
        
        validations = [
            (self.validate_directory_structure, "Estrutura de diretórios"),
            (self.validate_core_components, "Componentes Core"),
            (self.validate_quantum_components, "Componentes Neural"),
            (self.validate_shared_components, "Componentes Compartilhados"),
            (self.validate_dependencies, "Dependências"),
            (self.validate_configuration, "Configuração")
        ]
        
        success = True
        for validation_func, description in validations:
            logger.info(f"Validando {description}...")
            if not validation_func():
                success = False
                logger.error(f"Falha na validação: {description}")
            else:
                logger.info(f"Validação bem-sucedida: {description}")
        
        # Exibir erros e avisos
        if self.errors:
            logger.error("ERROS encontrados:")
            for error in self.errors:
                logger.error(f"  - {error}")
                
        if self.warnings:
            logger.warning("AVISOS encontrados:")
            for warning in self.warnings:
                logger.warning(f"  - {warning}")
        
        return success

def main():
    """Função principal."""
    try:
        base_path = Path(__file__).parent.parent
        validator = StructureValidator(base_path)
        
        if validator.run_validation():
            logger.info("Validação concluída com sucesso!")
            return 0
        else:
            logger.error("Validação falhou!")
            return 1
            
    except Excep                                                                                                                                            