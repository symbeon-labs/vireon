
# Regras WARP — Versão 2025‑07

> **Propósito**: Padronizar práticas de desenvolvimento, segurança, integração e governança para agentes, assistentes IDE e serviços do ecossistema WARP / VIREON.  
> **Formato**: Markdown para leitura • YAML para automação.  
> **Princípios‑chave**: tecnicidade, pragmatismo, auditabilidade.

---

## 1. symbolic_framework_heuristic
- **FastAPI** → APIs assíncronas leves  
- **Django** → Auth, ORM, Admin nativo  
- **Axum / Actix (Rust)** → desempenho crítico  
- **NestJS** → front‑ends modernos  
- **SQLite ⇢ dev / protótipo**, **PostgreSQL ⇢ produção**

Arquitetura (modular / separada / híbrida) deve alinhar‑se aos projetos **EON_LAB, SAGE_X, AIDEN_PROJECT, ARKITECT, …** (decisões auditáveis + refináveis em tempo real).

## 2. Environment Setup (referência)
Python 3.11 • Rust 1.87 • WSL • Git • VS Code • Node 18 • Docker 24 • PowerShell

## 3. Framework Choice – critérios adaptativos
… (idem versão anterior) …

## 4. Idioma & Linguagem Técnica
Português‑BR por padrão; alternância dinâmica p/ Inglês técnico quando necessário.

## 5‒23. (Regras de APIs, Segurança, Implementação, Extensibilidade, Monitoramento…)
*(conteúdo idêntico ao entregue na versão anterior, já sanitizado)*

---

## 24. SESSION RULES — Finalização de Sessão

### 24.1 Verificação de Ferramentas
| Ferramenta | Comando              | Versão mín. |
|------------|---------------------|-------------|
| Git        | `git --version`     | ≥ 2.40 |
| Node.js    | `node --version`    | ≥ 18  |
| Python     | `python --version`  | ≥ 3.10 |
| Winget     | `winget --version`  | n/a |
| Docker\*   | `docker --version`  | ≥ 24 |

> Se qualquer comando falhar, consulte seção **4 – Solução Rápida**.

### 24.2 Salvamento de Trabalho
1. `git add -A && git commit -m "WIP: …"`  
2. `git push origin <branch>`  
3. Atualizar **TASKS.md** e **CHANGELOG.md** (seção *Unreleased*).

### 24.3 Limpeza de Ambiente
- Encerrar VS Code, terminais ociosos.  
- `npm run clean` / `make clean` / `dotnet clean` se aplicável.  
- Remover `node_modules/.cache`, `__pycache__`, `.pytest_cache`, `bin/Debug`.

### 24.4 Atualizar PowerShell Profile
```powershell
. $PROFILE      # recarregar
```
Confirme ausência de erros.

### 24.5 Solução Rápida
| Sintoma                                    | Ação                           |
|-------------------------------------------|--------------------------------|
| Caixa “Selecionar aplicação” ao usar Git  | `C:\Users\laiss\fix-git-admin.ps1` (admin) |
| `node` não encontrado                     | Revisar `$env:Path`; reinstalar Node LTS |
| VS Code não encerra tarefas               | `taskkill /IM code.exe /F` (admin) |

### 24.6 Checklist Final
- [ ] Ferramentas OK  
- [ ] Código commitado / push  
- [ ] Tarefas documentadas  
- [ ] Ambiente limpo  
- [ ] Problemas resolvidos/documentados  

---

## 25. BRANCHING RULES
… (detalhes) …

## 26. CODE STYLE RULES
… (detalhes) …

## 27. TEST PLAN RULES
… (detalhes) …

## 28. RELEASE RULES
… (detalhes) …

## 29. Admin Privilege Policy
*(Invoke‑AdminCommand script + condições, notificação, revogação)*

---

## 30. Terminology Governance
Uso restrito de “neural”, “neural”, “consciência” — ver YAML anexo.

---

© 2025 EON_LAB / SAGE_X Alliance
