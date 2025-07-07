import os
import re
import json

def scan_for_secrets(directory="."):
    """Scan for potential exposed secrets in the codebase"""
    patterns = {
        'api_key': r'api[_-]?key\s*=\s*["\'][\w-]+["\']',
        'secret': r'secret[_-]?key\s*=\s*["\'][\w-]+["\']',
        'password': r'password\s*=\s*["\'][\w-]+["\']',
        'token': r'token\s*=\s*["\'][\w-]+["\']'
    }
    
    results = []
    extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env']
    
    for root, dirs, files in os.walk(directory):
        # Skip venv and node_modules
        dirs[:] = [d for d in dirs if d not in ['venv', '.venv', 'node_modules', '__pycache__']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for key, pattern in patterns.items():
                            matches = re.finditer(pattern, content)
                            for match in matches:
                                line_num = content[:match.start()].count('\n') + 1
                                results.append({
                                    'file': filepath,
                                    'line': line_num,
                                    'type': key,
                                    'match': match.group()
                                })
                except:
                    pass
    
    return results

if __name__ == "__main__":
    print("🔍 Scanning for potential secrets...")
    secrets = scan_for_secrets()
    
    if secrets:
        print(f"\n⚠️  Found {len(secrets)} potential secrets:")
        for secret in secrets:
            print(f"  - {secret['file']}:{secret['line']} ({secret['type']})")
        
        # Save report
        with open('security_scan_report.json', 'w') as f:
            json.dump(secrets, f, indent=2)
        print("\n📄 Detailed report saved to security_scan_report.json")
    else:
        print("✅ No potential secrets found!")
