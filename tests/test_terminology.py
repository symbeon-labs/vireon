import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from core.terminology_governance import (
    TerminologyViolation,
    TerminologyViolationLevel,
)
from core.terminology_governance.rules import RuleManager
from core.terminology_governance.analyzer import TerminologyAnalyzer
from core.terminology_governance.corrector import TerminologyCorrector
from core.terminology_governance.integration import IntegrationManager

@pytest.fixture
def rule_manager():
    return RuleManager()

@pytest.fixture
def analyzer(rule_manager):
    return TerminologyAnalyzer(rule_manager.rules)

@pytest.fixture
def corrector(rule_manager):
    return TerminologyCorrector(rule_manager)

@pytest.fixture
def integration_manager(rule_manager, analyzer, corrector):
    return IntegrationManager(rule_manager, analyzer, corrector)

def test_rule_loading(rule_manager):
    """Testa carregamento de regras"""
    rules = rule_manager.rules
    assert 'terminology_rules' in rules
    assert 'neural_symbiotic' in rules['terminology_rules']
    assert 'consciousness' in rules['terminology_rules']

def test_term_detection(analyzer):
    """Testa detecção de termos proibidos"""
    test_content = """
    def quantum_process():
        return quantum_enhancement()
    """
    
    violations = analyzer.analyze_file(Mock(spec=Path, read_text=lambda encoding: test_content))
    assert len(violations) == 2
    assert any(v.term == 'quantum_process' for v in violations)
    assert any(v.term == 'quantum_enhancement' for v in violations)

def test_correction_suggestion(corrector):
    """Testa sugestões de correção"""
    violation = TerminologyViolation(
        term='quantum_process',
        context='implementation',
        suggestion='neural_process',
        level=TerminologyViolationLevel.ERROR,
        file_path=Path('test.py'),
        line_number=1
    )
    
    suggestions = corrector.suggest_corrections([violation])
    assert 'test.py' in suggestions
    assert len(suggestions['test.py']) == 1
    assert 'neural_process' in suggestions['test.py'][0]

@pytest.mark.asyncio
async def test_project_integration(integration_manager):
    """Testa integração de projeto"""
    test_files = [
        Mock(spec=Path, suffix='.py', parts=['test.py'],
             read_text=lambda encoding: 'def quantum_process(): pass')
    ]
    
    with patch('pathlib.Path.rglob') as mock_rglob:
        mock_rglob.return_value = test_files
        report = await integration_manager.integrate_project(Path('test_project'))
        
    assert report.status == 'needs_correction'
    assert len(report.violations) == 1
    assert len(report.corrections) > 0

def test_context_detection(analyzer):
    """Testa detecção de contexto"""
    test_content = """
    # Documentation
    This is a quantum process implementation.
    """
    
    violations = analyzer.analyze_file(Mock(spec=Path, read_text=lambda encoding: test_content))
    assert len(violations) == 1
    assert violations[0].context == 'documentation'

def test_violation_levels(analyzer):
    """Testa níveis de violação"""
    test_content = """
    quantum_process()
    quantum_consciousness()
    """
    
    violations = analyzer.analyze_file(Mock(spec=Path, read_text=lambda encoding: test_content))
    assert all(v.level == TerminologyViolationLevel.ERROR for v in violations)

@pytest.mark.asyncio
async def test_pr_validation(integration_manager):
    """Testa validação de PR"""
    test_files = [
        Mock(spec=Path, suffix='.py',
             read_text=lambda encoding: 'def quantum_process(): pass')
    ]
    
    report = await integration_manager.validate_pr(test_files)
    assert report.status == 'needs_correction'
    assert len(report.violations) == 1

