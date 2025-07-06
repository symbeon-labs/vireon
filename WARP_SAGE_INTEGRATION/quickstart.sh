#!/bin/bash

# WARP_SAGE_INTEGRATION - Script de inicialização rápida (Linux/macOS)
# ==================================================================

echo "WARP_SAGE_INTEGRATION - Script de inicialização rápida (Linux/macOS)"
echo "=================================================================="
echo

# Verifica se o arquivo .env existe
if [ ! -f .env ]; then
    echo "Criando arquivo .env a partir do exemplo..."
    cp .env.example .env
    echo "Arquivo .env criado com sucesso!"
    echo "IMPORTANTE: Edite o arquivo .env com suas configurações antes de continuar."
    echo
    read -p "Pressione Enter para continuar..."
fi

# Prepara a estrutura de diretórios
echo "Criando estrutura de diretórios..."
mkdir -p python/warp_rules
mkdir -p rust/sage_x_rust_module
mkdir -p mock/eon_framework

# Copia arquivos entre diretórios, se necessário
echo
echo "Para prosseguir, você deve ter os arquivos de código em:"
echo "- python/warp_rules (código Python do WARP_RULES)"
echo "- rust/sage_x_rust_module (código Rust do SAGE-X Module)"
echo
read -p "Continuar? (S/N) " CONTINUE

if [[ ! "" =~ ^[Ss]$ ]]; then
    echo "Operação cancelada pelo usuário."
    exit 1
fi

# Verifica se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "[ERRO] Docker não encontrado! Certifique-se de que está instalado e em execução."
    exit 1
fi

# Verifica se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "[ERRO] Docker Compose não encontrado! Certifique-se de que está instalado corretamente."
    exit 1
fi

# Cria um mock simples para o EON Framework se não existir
if [ ! -f mock/eon_framework/db.json ]; then
    echo "Criando mock para o EON Framework..."
    cat > mock/eon_framework/db.json << EOF
{
  "tasks": [],
  "health": { "status": "ok" }
}
EOF
    
    cat > mock/eon_framework/routes.json << EOF
{
  "/api/task": "/tasks",
  "/api/health": "/health"
}
EOF
fi

# Dá permissão de execução aos scripts
find python rust -name "*.sh" -exec chmod +x {} \;

# Constrói e inicia os contêineres
echo
echo "Construindo e iniciando os contêineres..."
docker-compose up --build -d

# Verifica o status dos contêineres
echo
echo "Verificando o status dos contêineres..."
sleep 5
docker-compose ps

echo
echo "Inicialização concluída!"
echo
echo "Para visualizar os logs: docker-compose logs -f"
echo "Para parar os serviços: docker-compose down"
echo
