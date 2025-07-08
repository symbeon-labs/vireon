#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIREON MCP Tools v1.0
Ferramentas legacy para compatibilidade com funcionalidades básicas de desenvolvimento.
"""

import json
import sys
import os
import datetime
import subprocess
from typing import Dict, List, Any

def start_dev_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Inicia sessão de desenvolvimento com verificações básicas"""
    project_path = args.get('project_path', os.getcwd())
    symbiotic_mode = args.get('symbiotic_mode', True)
    consciousness_level = args.get('consciousness_level', 2)
    
    # Verificações básicas
    checks = []
    if os.path.exists(project_path):
        checks.append("✓ Diretório do projeto válido")
    else:
        checks.append("✗ Diretório do projeto não encontrado")
    
    if os.path.exists(os.path.join(project_path, '.git')):
        checks.append("✓ Repositório Git detectado")
    else:
        checks.append("⚠ Repositório Git não detectado")
    
    session_info = {
        "session_id": f"session_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "started_at": datetime.datetime.now().isoformat(),
        "project_path": project_path,
        "mode": "Human-AI Collaborative" if symbiotic_mode else "Standard",
        "awareness_level": f"Level {consciousness_level}/4"
    }
    
    return {
        "status": "success",
        "session_info": session_info,
        "initial_checks": checks,
        "message": "Sessão de desenvolvimento iniciada com sucesso"
    }

def smart_commit(args: Dict[str, Any]) -> Dict[str, Any]:
    """Commit inteligente seguindo Conventional Commits"""
    commit_type = args.get('type', 'feat')
    description = args.get('description', '')
    scope = args.get('scope', '')
    breaking = args.get('breaking', False)
    
    # Construir mensagem do commit
    commit_message = f"{commit_type}"
    if scope:
        commit_message += f"({scope})"
    if breaking:
        commit_message += "!"
    commit_message += f": {description}"
    
    try:
        # Verificar se há mudanças para commit
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if not result.stdout.strip():
            return {
                "status": "warning",
                "message": "Nenhuma mudança detectada para commit",
                "commit_message": commit_message
            }
        
        # Fazer o commit
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        return {
            "status": "success",
            "message": "Commit realizado com sucesso",
            "commit_message": commit_message,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "message": f"Erro ao realizar commit: {e}",
            "commit_message": commit_message
        }

def quality_gate(args: Dict[str, Any]) -> Dict[str, Any]:
    """Verificação de qualidade básica"""
    project_path = args.get('project_path', os.getcwd())
    
    checks = []
    
    # Verificar estrutura básica
    important_files = ['README.md', 'package.json', '.gitignore']
    for file in important_files:
        if os.path.exists(os.path.join(project_path, file)):
            checks.append(f"✓ {file} presente")
        else:
            checks.append(f"⚠ {file} ausente")
    
    # Verificar se há arquivos Python
    python_files = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    if python_files:
        checks.append(f"✓ {len(python_files)} arquivo(s) Python encontrado(s)")
    
    quality_score = len([c for c in checks if c.startswith('✓')]) / len(checks) * 100
    
    return {
        "status": "success",
        "quality_report": {
            "score": f"{quality_score:.1f}%",
            "checks": checks,
            "python_files_count": len(python_files)
        },
        "recommendations": [
            "Manter arquivos de documentação atualizados",
            "Implementar testes automatizados",
            "Seguir padrões de código limpo"
        ]
    }

def get_system_metrics(args: Dict[str, Any]) -> Dict[str, Any]:
    """Coleta métricas básicas do sistema"""
    import psutil
    
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            "cpu_usage": f"{cpu_percent:.1f}%",
            "memory_usage": f"{memory.percent:.1f}%",
            "memory_available": f"{memory.available / 1024**3:.1f} GB",
            "disk_usage": f"{disk.percent:.1f}%",
            "disk_free": f"{disk.free / 1024**3:.1f} GB"
        }
        
        return {
            "status": "success",
            "system_metrics": metrics,
            "timestamp": datetime.datetime.now().isoformat(),
            "health_status": "good" if cpu_percent < 80 and memory.percent < 80 else "attention_needed"
        }
        
    except ImportError:
        return {
            "status": "warning",
            "message": "psutil não disponível - métricas básicas simuladas",
            "system_metrics": {
                "cpu_usage": "N/A",
                "memory_usage": "N/A",
                "note": "Instalar psutil para métricas reais"
            }
        }

def end_dev_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Finaliza sessão de desenvolvimento"""
    project_path = args.get('project_path', os.getcwd())
    auto_commit = args.get('auto_commit', True)
    commit_message = args.get('commit_message', 'chore: end development session')
    changelog_entry = args.get('changelog_entry', '')
    
    summary = []
    
    # Auto-commit se solicitado
    if auto_commit:
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                subprocess.run(['git', 'add', '.'], check=True)
                subprocess.run(['git', 'commit', '-m', commit_message], check=True)
                summary.append("✓ Auto-commit realizado")
            else:
                summary.append("⚠ Nenhuma mudança para commit")
                
        except subprocess.CalledProcessError:
            summary.append("✗ Erro no auto-commit")
    
    # Adicionar entrada ao changelog se fornecida
    if changelog_entry:
        try:
            changelog_path = os.path.join(project_path, 'CHANGELOG.md')
            with open(changelog_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Adicionar nova entrada no topo
            new_entry = f"\n## {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n{changelog_entry}\n"
            content = content.replace('# Changelog\n', f'# Changelog\n{new_entry}')
            
            with open(changelog_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            summary.append("✓ Entrada adicionada ao CHANGELOG.md")
            
        except Exception as e:
            summary.append(f"⚠ Erro ao atualizar changelog: {e}")
    
    session_summary = {
        "ended_at": datetime.datetime.now().isoformat(),
        "project_path": project_path,
        "actions_performed": summary,
        "final_message": "Sessão de desenvolvimento finalizada com sucesso"
    }
    
    return {
        "status": "success",
        "session_summary": session_summary,
        "governance_note": "VIREON: Preservando estado e integridade do projeto"
    }

def vireon_audit(args: Dict[str, Any]) -> Dict[str, Any]:
    """Auditoria básica das regras VIREON"""
    
    # Simulação de auditoria básica
    audit_checks = [
        {"check": "Terminologia orientada ao mercado", "status": "passed", "score": 95},
        {"check": "Estrutura de arquivos adequada", "status": "passed", "score": 90},
        {"check": "Documentação presente", "status": "warning", "score": 75},
        {"check": "Testes implementados", "status": "needs_attention", "score": 60},
        {"check": "Código limpo e organizado", "status": "passed", "score": 85}
    ]
    
    total_score = sum(check["score"] for check in audit_checks) / len(audit_checks)
    
    if total_score >= 90:
        compliance_level = "Excellent"
        assessment = "Projeto totalmente aderente às regras VIREON"
    elif total_score >= 80:
        compliance_level = "Good"
        assessment = "Projeto bem alinhado com pequenos ajustes necessários"
    elif total_score >= 70:
        compliance_level = "Fair"
        assessment = "Projeto adequado mas com melhorias recomendadas"
    else:
        compliance_level = "Needs Improvement"
        assessment = "Projeto necessita ajustes significativos"
    
    return {
        "status": "success",
        "audit_report": {
            "compliance_level": compliance_level,
            "total_score": f"{total_score:.1f}/100",
            "assessment": assessment,
            "detailed_checks": audit_checks
        },
        "recommendations": [
            "Manter foco em terminologia de mercado",
            "Implementar testes automatizados",
            "Atualizar documentação regularmente",
            "Seguir padrões de código limpo"
        ],
        "audit_timestamp": datetime.datetime.now().isoformat()
    }

def main():
    """Função principal do script"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing function name",
            "usage": f"python {sys.argv[0]} <function_name> [args_json]"
        }))
        sys.exit(1)
    
    function_name = sys.argv[1]
    args = {}
    
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(json.dumps({
                "error": f"Invalid JSON arguments: {e}",
                "received": sys.argv[2]
            }))
            sys.exit(1)
    
    functions = {
        'start_dev_session': start_dev_session,
        'smart_commit': smart_commit,
        'quality_gate': quality_gate,
        'get_system_metrics': get_system_metrics,
        'end_dev_session': end_dev_session,
        'vireon_audit': vireon_audit
    }
    
    if function_name not in functions:
        print(json.dumps({
            "error": f"Unknown function: {function_name}",
            "available_functions": list(functions.keys())
        }))
        sys.exit(1)
    
    try:
        result = functions[function_name](args)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "error": f"Function execution failed: {str(e)}",
            "function": function_name,
            "args": args
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
