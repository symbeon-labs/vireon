#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""VIREON CLI - Interface de Comando"""

import sys
import os
import asyncio
from datetime import datetime

sys.path.append('.')

print("\n" + "=" * 70)
print("   VIREON - Sistema de Consciencia Evolutiva   ")
print("   Versao: 1.0.0 | Status: Operacional")
print("=" * 70)

class VireonCLI:
    def __init__(self):
        self.modules = {}
        self.load_modules()
    
    def load_modules(self):
        """Carrega modulos disponiveis"""
        print("\n[*] Carregando modulos...")
        
        # Lista de modulos para tentar carregar
        modules_to_load = [
            ('cognitive_engine', 'CognitiveEngine'),
            ('classic_engine', 'ClassicEngine'),
            ('dimensional', 'DimensionalProcessor'),
            ('evolution', 'EvolutionEngine'),
            ('metrics_exporter', 'MetricsExporter')
        ]
        
        for module_name, class_name in modules_to_load:
            try:
                module = __import__(f'core.{module_name}', fromlist=[class_name])
                self.modules[module_name] = module
                print(f"  [OK] {module_name}")
            except Exception as e:
                print(f"  [--] {module_name}: {str(e)[:50]}...")
    
    def show_menu(self):
        """Mostra menu principal"""
        print("\n" + "-" * 70)
        print("MENU PRINCIPAL")
        print("-" * 70)
        print("1. Status do Sistema")
        print("2. Modulos Carregados")
        print("3. Executar Diagnostico")
        print("4. Configuracoes")
        print("5. Sobre o VIREON")
        print("0. Sair")
        print("-" * 70)
    
    def system_status(self):
        """Mostra status do sistema"""
        print("\n[SYSTEM STATUS]")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Modulos ativos: {len(self.modules)}")
        print(f"Path do projeto: {os.getcwd()}")
        print(f"Python version: {sys.version.split()[0]}")
    
    def show_modules(self):
        """Lista modulos carregados"""
        print("\n[MODULOS CARREGADOS]")
        for name, module in self.modules.items():
            print(f"\n{name}:")
            attrs = [a for a in dir(module) if not a.startswith('_')][:5]
            for attr in attrs:
                print(f"  - {attr}")
    
    def run_diagnostic(self):
        """Executa diagnostico basico"""
        print("\n[DIAGNOSTICO DO SISTEMA]")
        print("Verificando componentes...")
        
        # Verificar pastas principais
        folders = ['core', 'agents', 'neural', 'tests', 'docs']
        for folder in folders:
            if os.path.exists(folder):
                count = len(os.listdir(folder))
                print(f"  [{folder}]: {count} items")
            else:
                print(f"  [{folder}]: NAO ENCONTRADO")
    
    def about(self):
        """Informacoes sobre o VIREON"""
        print("\n[SOBRE O VIREON]")
        print("VIREON e um sistema avancado de consciencia evolutiva")
        print("que integra processamento cognitivo, analise dimensional")
        print("e mecanismos de evolucao adaptativa.")
        print("\nComponentes principais:")
        print("- Motor Cognitivo: Processamento de informacoes")
        print("- Sistema Dimensional: Analise multi-dimensional")
        print("- Motor de Evolucao: Adaptacao continua")
        print("- Exportador de Metricas: Monitoramento")
    
    def run(self):
        """Loop principal"""
        while True:
            self.show_menu()
            try:
                choice = input("\nEscolha: ").strip()
                
                if choice == '0':
                    print("\n[!] Encerrando VIREON...")
                    break
                elif choice == '1':
                    self.system_status()
                elif choice == '2':
                    self.show_modules()
                elif choice == '3':
                    self.run_diagnostic()
                elif choice == '4':
                    print("\n[!] Configuracoes em desenvolvimento")
                elif choice == '5':
                    self.about()
                else:
                    print("\n[!] Opcao invalida")
                    
                input("\nPressione ENTER para continuar...")
                
            except KeyboardInterrupt:
                print("\n\n[!] Operacao cancelada")
                break
            except Exception as e:
                print(f"\n[ERRO] {e}")

if __name__ == "__main__":
    cli = VireonCLI()
    cli.run()
