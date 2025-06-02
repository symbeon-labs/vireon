# Setup de Desenvolvimento

## Ambiente Local

### Requisitos
- Python 3.9+
- Rust 1.70+
- Docker & Docker Compose
- PostgreSQL 14+
- Redis 6+

### Setup Inicial

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/vireon.git
cd vireon
```

2. Crie ambiente virtual Python:
```bash
poetry install
poetry shell
```

3. Setup Rust:
```bash
cd core
cargo build
```

4. Inicie serviços Docker:
```bash
docker-compose up -d
```

## Configuração

### Variáveis de Ambiente
```env
# API
VIREON_API_KEY=your-api-key
VIREON_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=vireon
DB_USER=vireon
DB_PASS=secret

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Configuração de IDE

#### VS Code
```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "rust-analyzer.checkOnSave.command": "clippy"
}
```

## Testes

### Python
```bash
pytest tests/
pytest --cov=vireon tests/
```

### Rust
```bash
cargo test
cargo clippy
```

## Debugging

### Python
```bash
python -m debugpy --listen 5678 --wait-for-client app.py
```

### Rust
```bash
RUST_BACKTRACE=1 cargo run
```

