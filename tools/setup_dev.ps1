# Script para configurar ambiente de desenvolvimento
$ErrorActionPreference = "Stop"

function Write-Log {
    param($Message)
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $Message"
}

# Verificar requisitos
Write-Log "Verificando requisitos..."

# Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python não encontrado. Por favor, instale Python 3.9 ou superior."
    exit 1
}

# Rust
if (-not (Get-Command rustc -ErrorAction SilentlyContinue)) {
    Write-Error "Rust não encontrado. Por favor, instale Rust usando rustup."
    exit 1
}

# Criar e ativar ambiente virtual
Write-Log "Configurando ambiente virtual Python..."
python -m venv venv
.\venv\Scripts\Activate

# Atualizar pip
Write-Log "Atualizando pip..."
python -m pip install --upgrade pip

# Instalar dependências Python
Write-Log "Instalando dependências Python..."
pip install maturin
pip install -e .

# Compilar componentes Rust
Write-Log "Compilando componentes Rust..."
foreach ($cargo_toml in @("VIREON-CORE/Cargo.toml", "VIREON-QUANTUM/Cargo.toml", "Shared/Cargo.toml")) {
    if (Test-Path $cargo_toml) {
        Write-Log "Compilando $cargo_toml..."
        Push-Location (Split-Path $cargo_toml)
        cargo build
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Falha ao compilar $cargo_toml"
            exit 1
        }
        Pop-Location
    }
}

# Executar testes
Write-Log "Executando testes..."
pytest

Write-Log "Setup completo!"
Write-Log @"
Ambiente configurado com sucesso!

Para começar a desenvolver:
1. Ative o ambiente virtual: .\venv\Scripts\Activate
2. Execute o servidor: uvicorn vireon.api:app --reload
3. Execute testes: pytest

Para mais informações, consulte o README.md
"@

