@echo off
echo WARP_SAGE_INTEGRATION - Script de inicialização rápida (Windows)
echo ================================================================

REM Verifica se o arquivo .env existe
if not exist .env (
    echo Criando arquivo .env a partir do exemplo...
    copy .env.example .env
    echo Arquivo .env criado com sucesso!
    echo IMPORTANTE: Edite o arquivo .env com suas configurações antes de continuar.
    echo.
    pause
)

REM Prepara a estrutura de diretórios
echo Criando estrutura de diretórios...
if not exist python\warp_rules mkdir python\warp_rules
if not exist rust\sage_x_rust_module mkdir rust\sage_x_rust_module
if not exist mock\eon_framework mkdir mock\eon_framework

REM Copia arquivos entre diretórios, se necessário
echo.
echo Para prosseguir, você deve ter os arquivos de código em:
echo - python\warp_rules (código Python do WARP_RULES)
echo - rust\sage_x_rust_module (código Rust do SAGE-X Module)
echo.
echo Continuar? (S/N)
set /p CONTINUE=

if /i "%CONTINUE%" NEQ "S" (
    echo Operação cancelada pelo usuário.
    exit /b
)

REM Verifica se o Docker está instalado
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Docker não encontrado! Certifique-se de que o Docker Desktop está instalado e em execução.
    exit /b
)

REM Verifica se o Docker Compose está instalado
docker-compose --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Docker Compose não encontrado! Certifique-se de que está instalado corretamente.
    exit /b
)

REM Cria um mock simples para o EON Framework se não existir
if not exist mock\eon_framework\db.json (
    echo Criando mock para o EON Framework...
    echo { > mock\eon_framework\db.json
    echo   "tasks": [], >> mock\eon_framework\db.json
    echo   "health": { "status": "ok" } >> mock\eon_framework\db.json
    echo } >> mock\eon_framework\db.json
    
    echo { > mock\eon_framework\routes.json
    echo   "/api/task": "/tasks", >> mock\eon_framework\routes.json
    echo   "/api/health": "/health" >> mock\eon_framework\routes.json
    echo } >> mock\eon_framework\routes.json
)

REM Constrói e inicia os contêineres
echo.
echo Construindo e iniciando os contêineres...
docker-compose up --build -d

REM Verifica o status dos contêineres
echo.
echo Verificando o status dos contêineres...
timeout /t 5 /nobreak > nul
docker-compose ps

echo.
echo Inicialização concluída!
echo.
echo Para visualizar os logs: docker-compose logs -f
echo Para parar os serviços: docker-compose down
echo.
