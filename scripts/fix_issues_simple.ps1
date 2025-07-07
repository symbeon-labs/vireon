# VIREON - Script de Correção Simplificado
Write-Host "🔧 VIREON - Executando Correções" -ForegroundColor Cyan

# 1. Limpeza de Cache
Write-Host "`n🧹 Limpando caches e arquivos temporários..." -ForegroundColor Yellow
$cachePatterns = @("__pycache__", ".pytest_cache", "*.pyc", "*.log")
$totalRemoved = 0

foreach ($pattern in $cachePatterns) {
    $items = Get-ChildItem -Path . -Recurse -Force -ErrorAction SilentlyContinue | Where-Object { $_.Name -like $pattern }
    foreach ($item in $items) {
        Remove-Item -Path $item.FullName -Force -Recurse -ErrorAction SilentlyContinue
        $totalRemoved++
    }
}
Write-Host "✅ Removidos $totalRemoved arquivos/diretórios de cache" -ForegroundColor Green

# 2. Remover diretórios vazios
Write-Host "`n📁 Removendo diretórios vazios..." -ForegroundColor Yellow
$emptyDirs = Get-ChildItem -Recurse -Directory | Where-Object { (Get-ChildItem $_.FullName -Force).Count -eq 0 }
$emptyCount = $emptyDirs.Count

if ($emptyCount -gt 0) {
    $emptyDirs | ForEach-Object { Remove-Item $_.FullName -Force }
    Write-Host "✅ Removidos $emptyCount diretórios vazios" -ForegroundColor Green
} else {
    Write-Host "✅ Nenhum diretório vazio encontrado" -ForegroundColor Green
}

# 3. Criar .gitignore atualizado
Write-Host "`n📝 Atualizando .gitignore..." -ForegroundColor Yellow
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# Rust
target/
Cargo.lock
*.rs.bk

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Environment
.env
.env.local
.env.*.local

# Build
dist/
build/
*.exe
*.dll
*.so
*.dylib

# Temporary
*.tmp
*.temp
*.cache
"@

$gitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8
Write-Host "✅ .gitignore atualizado" -ForegroundColor Green

# 4. Criar script de verificação de segurança
Write-Host "`n🔒 Criando script de verificação de segurança..." -ForegroundColor Yellow
$securityScript = @'
import os
import re
import json

def scan_for_secrets(directory="."):
    """Scan for potential exposed secrets in the codebase"""
    patterns = {
        'api_key': r'api[_-]?key\s*=\s*["\'][\w-]+["\']',
        'secret': r'secret[_-]?key\s*=\s*["\'][\w-]+["\']',
        'password': r'password\s*=\s*["\'][\w-]+["\']',
        'token': r'token\s*=\s*["\'][\w-]+["\']'
    }
    
    results = []
    extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env']
    
    for root, dirs, files in os.walk(directory):
        # Skip venv and node_modules
        dirs[:] = [d for d in dirs if d not in ['venv', '.venv', 'node_modules', '__pycache__']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for key, pattern in patterns.items():
                            matches = re.finditer(pattern, content)
                            for match in matches:
                                line_num = content[:match.start()].count('\n') + 1
                                results.append({
                                    'file': filepath,
                                    'line': line_num,
                                    'type': key,
                                    'match': match.group()
                                })
                except:
                    pass
    
    return results

if __name__ == "__main__":
    print("🔍 Scanning for potential secrets...")
    secrets = scan_for_secrets()
    
    if secrets:
        print(f"\n⚠️  Found {len(secrets)} potential secrets:")
        for secret in secrets:
            print(f"  - {secret['file']}:{secret['line']} ({secret['type']})")
        
        # Save report
        with open('security_scan_report.json', 'w') as f:
            json.dump(secrets, f, indent=2)
        print("\n📄 Detailed report saved to security_scan_report.json")
    else:
        print("✅ No potential secrets found!")
'@

$securityScript | Out-File -FilePath "scripts/security_scan.py" -Encoding UTF8
Write-Host "✅ Script de segurança criado" -ForegroundColor Green

# 5. Criar template de teste
Write-Host "`n🧪 Criando template de teste..." -ForegroundColor Yellow
$testTemplate = @'
"""
Template for VIREON unit tests
"""
import pytest
from unittest.mock import Mock, patch


class TestTemplate:
    """Template test class"""
    
    def setup_method(self):
        """Setup test environment"""
        pass
    
    def teardown_method(self):
        """Cleanup after test"""
        pass
    
    def test_example(self):
        """Example test case"""
        # Arrange
        expected = True
        
        # Act
        result = True
        
        # Assert
        assert result == expected
    
    @pytest.mark.parametrize("input,expected", [
        (1, 1),
        (2, 2),
        (3, 3),
    ])
    def test_parametrized(self, input, expected):
        """Example parametrized test"""
        assert input == expected
'@

$testTemplate | Out-File -FilePath "templates/test_template.py" -Encoding UTF8
Write-Host "✅ Template de teste criado" -ForegroundColor Green

Write-Host "`n✅ Correções concluídas!" -ForegroundColor Green
Write-Host "📊 Resumo das ações:" -ForegroundColor Yellow
Write-Host "  - Cache limpo: $totalRemoved itens removidos"
Write-Host "  - Diretórios vazios: $emptyCount removidos"
Write-Host "  - .gitignore atualizado"
Write-Host "  - Script de segurança criado em scripts/security_scan.py"
Write-Host "  - Template de teste criado em templates/test_template.py"
Write-Host "`n💡 Execute 'python scripts/security_scan.py' para verificar segurança" -ForegroundColor Cyan
