# Script de Otimização do Warp
# Criado em: 2025-07-07
# Propósito: Reduzir consumo de recursos do Warp

Write-Host "=== Otimização do Warp ===" -ForegroundColor Cyan
Write-Host "Iniciando processo de otimização..." -ForegroundColor Yellow

# 1. Verificar estado atual
Write-Host "`n[1] Estado atual do Warp:" -ForegroundColor Green
$warpProcess = Get-Process -Name warp -ErrorAction SilentlyContinue
if ($warpProcess) {
    $warpProcess | ForEach-Object {
        Write-Host "  - PID: $($_.Id)"
        Write-Host "  - Memória: $([Math]::Round($_.PM/1MB,2)) MB"
        Write-Host "  - Handles: $($_.Handles)"
        Write-Host "  - CPU Time: $($_.CPU) segundos"
    }
} else {
    Write-Host "  Warp não está em execução." -ForegroundColor Yellow
}

# 2. Limpar cache do sistema
Write-Host "`n[2] Limpando caches do sistema..." -ForegroundColor Green
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  OK - Cache temporário limpo" -ForegroundColor Green

# 3. Configurar limites de memória para o Warp
Write-Host "`n[3] Aplicando configurações de otimização..." -ForegroundColor Green

# Criar arquivo de configuração de otimização
$configPath = "$env:USERPROFILE\.warp\optimization.json"
$optimizationConfig = @{
    "memory_limit" = "2GB"
    "cache_cleanup_interval" = "30min"
    "max_handles" = 10000
    "performance_mode" = "balanced"
} | ConvertTo-Json

# Criar diretório se não existir
if (!(Test-Path "$env:USERPROFILE\.warp")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\.warp" -Force | Out-Null
}

# Salvar configuração
$optimizationConfig | Set-Content -Path $configPath -Force
Write-Host "  OK - Configurações de otimização salvas" -ForegroundColor Green

# 4. Reiniciar o Warp com otimizações
$restart = Read-Host "`n[4] Deseja reiniciar o Warp agora? (S/N)"
if ($restart -eq 'S' -or $restart -eq 's') {
    Write-Host "  Encerrando processos do Warp..." -ForegroundColor Yellow
    Stop-Process -Name warp -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 3
    
    Write-Host "  Reiniciando Warp com otimizações..." -ForegroundColor Yellow
    Start-Process "warp" -WindowStyle Minimized
    Write-Host "  OK - Warp reiniciado" -ForegroundColor Green
}

# 5. Verificar novo estado
Start-Sleep -Seconds 5
Write-Host "`n[5] Novo estado do Warp:" -ForegroundColor Green
$newWarpProcess = Get-Process -Name warp -ErrorAction SilentlyContinue
if ($newWarpProcess) {
    $newWarpProcess | ForEach-Object {
        Write-Host "  - PID: $($_.Id)"
        Write-Host "  - Memória: $([Math]::Round($_.PM/1MB,2)) MB"
        Write-Host "  - Handles: $($_.Handles)"
    }
}

Write-Host "`nOtimização concluída!" -ForegroundColor Green
Write-Host "Dica: Execute este script regularmente para manter o desempenho." -ForegroundColor Cyan
