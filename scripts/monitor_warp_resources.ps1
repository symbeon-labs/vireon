# Monitor de Recursos do Warp
# Executa monitoramento contínuo e alerta sobre uso excessivo

param(
    [int]$IntervalSeconds = 60,
    [int]$MaxMemoryMB = 2048,
    [int]$MaxCPUPercent = 50
)

Write-Host "🔍 Monitor de Recursos do Warp" -ForegroundColor Cyan
Write-Host "Limites: Memória=$MaxMemoryMB MB, CPU=$MaxCPUPercent%" -ForegroundColor Yellow
Write-Host "Pressione Ctrl+C para parar`n" -ForegroundColor Gray

$logFile = ".\logs\warp_resource_monitor.log"

# Criar diretório de logs se não existir
if (!(Test-Path ".\logs")) {
    New-Item -ItemType Directory -Path ".\logs" -Force | Out-Null
}

# Função para adicionar ao log
function Add-Log {
    param($Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp - $Message" | Add-Content -Path $logFile
}

# Loop de monitoramento
while ($true) {
    $processes = Get-Process -Name warp -ErrorAction SilentlyContinue
    
    if ($processes) {
        foreach ($proc in $processes) {
            $memoryMB = [Math]::Round($proc.PM/1MB, 2)
            $cpuPercent = [Math]::Round($proc.CPU / (Get-WmiObject Win32_Processor).NumberOfLogicalProcessors, 2)
            
            $status = "OK"
            $color = "Green"
            
            # Verificar limites
            if ($memoryMB -gt $MaxMemoryMB -or $cpuPercent -gt $MaxCPUPercent) {
                $status = "ALERTA"
                $color = "Red"
                
                # Log do alerta
                Add-Log "ALERTA: PID=$($proc.Id) Memória=$memoryMB MB CPU=$cpuPercent%"
                
                # Notificação visual
                Write-Host "`n⚠️  ALERTA DE RECURSOS!" -ForegroundColor Red
            }
            
            # Exibir status
            $timestamp = Get-Date -Format "HH:mm:ss"
            Write-Host "[$timestamp] PID: $($proc.Id) | Mem: $memoryMB MB | CPU: $cpuPercent% | Handles: $($proc.Handles) | Status: $status" -ForegroundColor $color
            
            # Log regular
            if ($status -eq "OK") {
                Add-Log "INFO: PID=$($proc.Id) Memória=$memoryMB MB CPU=$cpuPercent% Handles=$($proc.Handles)"
            }
        }
    } else {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Warp não está em execução" -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}
