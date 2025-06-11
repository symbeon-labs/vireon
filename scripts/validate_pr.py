import sys
from pathlib import Path
from typing import List, Dict

from core.consciousness.validation import SymbioticValidator

def validate_pr_files(files: List[Path]) -> Dict:
    validator = SymbioticValidator()
    violations = []
    
    for file in files:
        if file.suffix in ['.py', '.rs', '.md', '.txt']:
            file_violations = validator.validate_file(file)
            violations.extend(file_violations)
    
    return {
        'status': 'failed' if violations else 'success',
        'violations': violations
    }

def format_report(results: Dict) -> str:
    if results['status'] == 'success':
        return '\n✅ Validação de Terminologia: OK\n'
    
    report = ['\n❌ Violações de Terminologia Encontradas:\n']
    
    for violation in results['violations']:
        report.append(
            f"Arquivo: {violation['file']}\n"
            f"Linha {violation['line']}: '{violation['term']}' "
            f"-> Sugestão: '{violation['suggestion']}'"
        )
    
    return '\n'.join(report)

def main():
    # Recebe lista de arquivos como argumentos
    files = [Path(f) for f in sys.argv[1:]]
    
    # Valida arquivos
    results = validate_pr_files(files)
    
    # Imprime relatório
    print(format_report(results))
    
    # Retorna código de saída
    sys.exit(0 if results['status'] == 'success' else 1)

if __name__ == '__main__':
    main()

