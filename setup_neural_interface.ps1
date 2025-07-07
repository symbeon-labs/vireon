# Script de configuração para a Interface Neural VIREON

Write-Host "Configurando a Interface Neural VIREON..." -ForegroundColor Cyan

# Renomear arquivos .new para substituir os corrompidos
Write-Host "Corrigindo arquivos corrompidos..." -ForegroundColor Yellow

if (Test-Path ".\frontend\package.json.new") {
    Move-Item -Path ".\frontend\package.json.new" -Destination ".\frontend\package.json" -Force
    Write-Host "✓ package.json restaurado" -ForegroundColor Green
}

if (Test-Path ".\frontend\tailwind.config.js.new") {
    Move-Item -Path ".\frontend\tailwind.config.js.new" -Destination ".\frontend\tailwind.config.js" -Force
    Write-Host "✓ tailwind.config.js restaurado" -ForegroundColor Green
}

if (Test-Path ".\frontend\src\index.css.new") {
    Move-Item -Path ".\frontend\src\index.css.new" -Destination ".\frontend\src\index.css" -Force
    Write-Host "✓ index.css restaurado" -ForegroundColor Green
}

# Verificar se node_modules existe, se não, instalar dependências
Write-Host "Verificando dependências..." -ForegroundColor Yellow
if (-not (Test-Path ".\frontend\node_modules")) {
    Write-Host "Instalando dependências (isso pode levar algum tempo)..." -ForegroundColor Yellow
    Set-Location -Path ".\frontend"
    npm install
    npm install -D tailwindcss postcss autoprefixer tw-animate-css
    Set-Location -Path ".."
    Write-Host "✓ Dependências instaladas" -ForegroundColor Green
} else {
    Write-Host "✓ Dependências já instaladas" -ForegroundColor Green
}

Write-Host "`nInterface Neural VIREON configurada com sucesso!" -ForegroundColor Cyan
Write-Host "`nPara iniciar a aplicação:" -ForegroundColor White
Write-Host "1. Navegue até a pasta frontend: cd frontend" -ForegroundColor White
Write-Host "2. Execute o servidor de desenvolvimento: npm run dev" -ForegroundColor White
Write-Host "3. Abra o navegador no endereço indicado (geralmente http://localhost:5173)" -ForegroundColor White

Write-Host "`nPara mais informações, consulte o arquivo: ./frontend/README.NEURAL.md" -ForegroundColor White
