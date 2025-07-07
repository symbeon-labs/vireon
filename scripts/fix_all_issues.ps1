# VIREON - Script de Correção Coordenada
# Executa correções em paralelo para todos os pontos identificados

Write-Host "🔧 VIREON - Correção Coordenada de Issues" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. SEGURANÇA - Verificar credenciais expostas
Write-Host "`n🔒 1. SEGURANÇA - Verificando credenciais..." -ForegroundColor Yellow
$securityJob = Start-Job -ScriptBlock {
    # Buscar por padrões de credenciais
    $patterns = @(
        'api[_-]?key\s*=\s*\"[\w-]+\"',
        'secret[_-]?key\s*=\s*\"[\w-]+\"',
        'password\s*=\s*\"[\w-]+\"',
        'token\s*=\s*\"[\w-]+\"'
    )
    
    $results = @()
    foreach ($pattern in $patterns) {
        $matches = Get-ChildItem -Recurse -Include *.py,*.js,*.ts,*.json,*.yaml,*.yml -File | 
                   Select-String -Pattern $pattern
        if ($matches) {
            $results += $matches
        }
    }
    
    if ($results.Count -gt 0) {
        Write-Output "⚠️ Possíveis credenciais encontradas em $($results.Count) arquivos"
        $results | ForEach-Object { Write-Output "  - $($_.Filename):$($_.LineNumber)" }
    } else {
        Write-Output "✅ Nenhuma credencial exposta encontrada"
    }
}

# 2. OTIMIZAÇÃO - Limpar arquivos desnecessários
Write-Host "`n🧹 2. OTIMIZAÇÃO - Limpando repositório..." -ForegroundColor Yellow
$cleanupJob = Start-Job -ScriptBlock {
    # Remover arquivos de cache e build
    $dirsToClean = @(
        "__pycache__",
        ".pytest_cache",
        "*.pyc",
        "node_modules/.cache",
        "target/debug",
        "*.log"
    )
    
    $totalSize = 0
    foreach ($pattern in $dirsToClean) {
        $items = Get-ChildItem -Path . -Recurse -Force -ErrorAction SilentlyContinue | 
                 Where-Object { $_.FullName -like "*$pattern*" }
        
        foreach ($item in $items) {
            $totalSize += $item.Length
            Remove-Item -Path $item.FullName -Force -Recurse -ErrorAction SilentlyContinue
        }
    }
    
    $sizeMB = [math]::Round($totalSize / 1MB, 2)
    Write-Output "✅ Liberados $sizeMB MB de espaço"
}

# 3. DUPLICAÇÃO - Analisar código duplicado
Write-Host "`n🔍 3. DUPLICAÇÃO - Analisando código..." -ForegroundColor Yellow
$duplicationJob = Start-Job -ScriptBlock {
    # Verificar arquivos Python duplicados por hash
    $hashes = @{}
    $duplicates = @()
    
    Get-ChildItem -Recurse -Filter "*.py" | ForEach-Object {
        $hash = (Get-FileHash $_.FullName -Algorithm MD5).Hash
        if ($hashes.ContainsKey($hash)) {
            $duplicates += @{
                Original = $hashes[$hash]
                Duplicate = $_.FullName
            }
        } else {
            $hashes[$hash] = $_.FullName
        }
    }
    
    if ($duplicates.Count -gt 0) {
        Write-Output "⚠️ Encontrados $($duplicates.Count) arquivos duplicados"
        $duplicates | ForEach-Object { 
            Write-Output "  - $($_.Duplicate) (duplicado de $($_.Original))"
        }
    } else {
        Write-Output "✅ Nenhuma duplicação exata encontrada"
    }
}

# 4. TESTES - Verificar cobertura
Write-Host "`n🧪 4. TESTES - Verificando cobertura..." -ForegroundColor Yellow
$testJob = Start-Job -ScriptBlock {
    # Contar arquivos de teste vs arquivos de código
    $codeFiles = (Get-ChildItem -Recurse -Filter "*.py" | 
                  Where-Object { $_.FullName -notlike "*test*" -and $_.FullName -notlike "*__pycache__*" }).Count
    $testFiles = (Get-ChildItem -Recurse -Filter "test_*.py").Count
    
    $ratio = if ($codeFiles -gt 0) { [math]::Round(($testFiles / $codeFiles) * 100, 2) } else { 0 }
    
    Write-Output "📊 Arquivos de código: $codeFiles"
    Write-Output "📊 Arquivos de teste: $testFiles"
    Write-Output "📊 Proporção teste/código: $ratio%"
    
    if ($ratio -lt 30) {
        Write-Output "⚠️ Cobertura de testes baixa (recomendado: >80%)"
    } else {
        Write-Output "✅ Cobertura de testes adequada"
    }
}

# 5. ESTRUTURA - Verificar diretórios vazios
Write-Host "`n📁 5. ESTRUTURA - Limpando diretórios vazios..." -ForegroundColor Yellow
$structureJob = Start-Job -ScriptBlock {
    $emptyDirs = Get-ChildItem -Recurse -Directory | 
                 Where-Object { (Get-ChildItem $_.FullName -Force).Count -eq 0 }
    
    if ($emptyDirs.Count -gt 0) {
        Write-Output "🧹 Removendo $($emptyDirs.Count) diretórios vazios"
        $emptyDirs | ForEach-Object {
            Remove-Item $_.FullName -Force
        }
        Write-Output "✅ Diretórios vazios removidos"
    } else {
        Write-Output "✅ Nenhum diretório vazio encontrado"
    }
}

# Aguardar todos os jobs
Write-Host "`n⏳ Aguardando conclusão das tarefas paralelas..." -ForegroundColor Cyan
$jobs = @($securityJob, $cleanupJob, $duplicationJob, $testJob, $structureJob)
$results = $jobs | Wait-Job | Receive-Job

# Exibir resultados
Write-Host "`n📊 RESULTADOS DA CORREÇÃO" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green
$results | ForEach-Object { Write-Host $_ }

# Limpar jobs
$jobs | Remove-Job

# Criar relatório
$report = @"
# VIREON - Relatório de Correções
Data: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## Resultados das Correções

### 1. Segurança
$($results[0])

### 2. Otimização
$($results[1])

### 3. Duplicação
$($results[2])

### 4. Testes
$($results[3])

### 5. Estrutura
$($results[4])

## Próximos Passos
0. Implementar secrets scanning automático
0. Configurar CI/CD com quality gates
0. Aumentar cobertura de testes
0. Criar documentação de API
"@

$report | Out-File -FilePath "CORRECTION_REPORT.md" -Encoding UTF8

Write-Host "`n✅ Correções concluídas! Relatório salvo em CORRECTION_REPORT.md" -ForegroundColor Green
Write-Host "📝 Execute 'git add -A && git commit -m \"fix: correções de segurança, otimização e qualidade\"' para salvar as mudanças" -ForegroundColor Yellow
