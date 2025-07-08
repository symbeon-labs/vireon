#!/usr/bin/env node

/**
 * VIREON System Audit Script
 * Auditoria completa do sistema VIREON seguindo as especificações técnicas
 * e regras de governança definidas
 */

import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

class VireonAuditor {
    constructor() {
        this.results = {
            timestamp: new Date().toISOString(),
            status: 'INICIANDO',
            modules: {},
            governance: {},
            integration: {},
            security: {},
            performance: {},
            recommendations: []
        };
        
        this.criticalModules = [
            'symbiotic_integration',
            'consciousness_framework', 
            'system_evolution',
            'communication_system',
            'validation_protocols',
            'preservation_system',
            'super_scope_integration',
            'execution_protocols',
            'metrics_monitoring',
            'adaptive_evolution'
        ];
    }

    async runAudit() {
        console.log('🔍 VIREON SYSTEM AUDIT');
        console.log('═══════════════════════');
        console.log(`📅 Iniciado em: ${this.results.timestamp}\n`);

        try {
            await this.auditSystemStructure();
            await this.auditGovernance();
            await this.auditIntegration();
            await this.auditSecurity();
            await this.auditPerformance();
            await this.auditTerminologyCompliance();
            await this.generateRecommendations();
            
            this.results.status = this.calculateOverallStatus();
            await this.generateReport();
            
        } catch (error) {
            this.results.status = 'ERRO';
            console.error('❌ Erro durante auditoria:', error.message);
        }
    }

    async auditSystemStructure() {
        console.log('📁 Auditando estrutura do sistema...');
        
        const moduleStatus = {};
        const requiredFiles = [
            'index.js',
            'package.json',
            'README.md',
            'DESENVOLVIMENTO.md',
            'TODO.md',
            'SESSION.md'
        ];

        // Verificar arquivos base
        for (const file of requiredFiles) {
            const exists = fs.existsSync(file);
            moduleStatus[file] = {
                exists,
                status: exists ? 'OK' : 'MISSING',
                size: exists ? fs.statSync(file).size : 0
            };
        }

        // Verificar módulos críticos no index.js
        try {
            const indexContent = fs.readFileSync('index.js', 'utf8');
            
            for (const module of this.criticalModules) {
                const moduleExists = indexContent.includes(module) || 
                                  indexContent.includes(module.replace(/_/g, '-')) ||
                                  indexContent.includes(module.replace(/_/g, ''));
                
                moduleStatus[module] = {
                    exists: moduleExists,
                    status: moduleExists ? 'IMPLEMENTED' : 'MISSING',
                    implementation: moduleExists ? 'DETECTED' : 'NOT_FOUND'
                };
            }
        } catch (error) {
            console.warn('⚠️ Erro ao analisar index.js:', error.message);
        }

        this.results.modules = moduleStatus;
        console.log('✅ Estrutura do sistema auditada');
    }

    async auditGovernance() {
        console.log('📋 Auditando governança e terminologia...');
        
        const governance = {
            terminology_compliance: 'CHECKING',
            restricted_terms: [],
            session_documentation: 'CHECKING',
            framework_alignment: 'CHECKING'
        };

        try {
            // Verificar compliance terminológica
            const files = this.getCodeFiles();
            const restrictedTerms = ['quantum', 'neural', 'consciousness'];
            const foundTerms = [];

            for (const file of files) {
                if (fs.existsSync(file)) {
                    const content = fs.readFileSync(file, 'utf8').toLowerCase();
                    
                    for (const term of restrictedTerms) {
                        if (content.includes(term)) {
                            foundTerms.push({
                                file,
                                term,
                                needsValidation: true
                            });
                        }
                    }
                }
            }

            governance.restricted_terms = foundTerms;
            governance.terminology_compliance = foundTerms.length > 0 ? 'NEEDS_REVIEW' : 'COMPLIANT';

            // Verificar documentação de sessão
            const sessionFiles = ['SESSION.md', 'DESENVOLVIMENTO.md', 'TODO.md'];
            const sessionStatus = sessionFiles.map(file => ({
                file,
                exists: fs.existsSync(file),
                lastModified: fs.existsSync(file) ? fs.statSync(file).mtime : null
            }));

            governance.session_documentation = sessionStatus.every(s => s.exists) ? 'COMPLETE' : 'INCOMPLETE';
            
        } catch (error) {
            governance.terminology_compliance = 'ERROR';
            console.warn('⚠️ Erro na auditoria de governança:', error.message);
        }

        this.results.governance = governance;
        console.log('✅ Governança auditada');
    }

    async auditIntegration() {
        console.log('🔗 Auditando integrações...');
        
        const integration = {
            mcp_server: 'CHECKING',
            node_modules: 'CHECKING',
            dependencies: 'CHECKING',
            api_endpoints: 'CHECKING'
        };

        try {
            // Verificar se é um servidor MCP válido
            if (fs.existsSync('package.json')) {
                const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
                integration.mcp_server = packageJson.dependencies && 
                                       Object.keys(packageJson.dependencies).some(dep => 
                                           dep.includes('mcp') || dep.includes('server')) ? 'CONFIGURED' : 'NOT_CONFIGURED';
                
                integration.dependencies = Object.keys(packageJson.dependencies || {}).length > 0 ? 'INSTALLED' : 'MISSING';
            }

            // Verificar node_modules
            integration.node_modules = fs.existsSync('node_modules') ? 'PRESENT' : 'MISSING';

            // Verificar endpoints de API no código
            if (fs.existsSync('index.js')) {
                const indexContent = fs.readFileSync('index.js', 'utf8');
                const hasEndpoints = indexContent.includes('app.') || 
                                   indexContent.includes('router.') ||
                                   indexContent.includes('server.') ||
                                   indexContent.includes('tools');
                
                integration.api_endpoints = hasEndpoints ? 'CONFIGURED' : 'NOT_CONFIGURED';
            }

        } catch (error) {
            console.warn('⚠️ Erro na auditoria de integração:', error.message);
        }

        this.results.integration = integration;
        console.log('✅ Integrações auditadas');
    }

    async auditSecurity() {
        console.log('🔒 Auditando segurança...');
        
        const security = {
            credentials_management: 'CHECKING',
            environment_variables: 'CHECKING',
            input_validation: 'CHECKING',
            error_handling: 'CHECKING'
        };

        try {
            // Verificar gerenciamento de credenciais
            const files = this.getCodeFiles();
            let hasHardcodedSecrets = false;
            let hasEnvUsage = false;

            for (const file of files) {
                if (fs.existsSync(file)) {
                    const content = fs.readFileSync(file, 'utf8');
                    
                    // Verificar segredos hardcoded
                    const secretPatterns = [
                        /api[_-]?key\s*=\s*['"]['"][^'""]+['"]/i,
                        /password\s*=\s*['"]['"][^'""]+['"]/i,
                        /token\s*=\s*['"]['"][^'""]+['"]/i
                    ];
                    
                    if (secretPatterns.some(pattern => pattern.test(content))) {
                        hasHardcodedSecrets = true;
                    }

                    // Verificar uso de variáveis de ambiente
                    if (content.includes('process.env') || content.includes('process.env.')) {
                        hasEnvUsage = true;
                    }
                }
            }

            security.credentials_management = hasHardcodedSecrets ? 'VULNERABLE' : 'SECURE';
            security.environment_variables = hasEnvUsage ? 'CONFIGURED' : 'NOT_CONFIGURED';

            // Verificar tratamento de erros
            if (fs.existsSync('index.js')) {
                const indexContent = fs.readFileSync('index.js', 'utf8');
                const hasErrorHandling = indexContent.includes('try') && indexContent.includes('catch');
                security.error_handling = hasErrorHandling ? 'IMPLEMENTED' : 'MISSING';
            }

        } catch (error) {
            console.warn('⚠️ Erro na auditoria de segurança:', error.message);
        }

        this.results.security = security;
        console.log('✅ Segurança auditada');
    }

    async auditPerformance() {
        console.log('⚡ Auditando performance...');
        
        const performance = {
            file_sizes: {},
            dependency_count: 0,
            code_complexity: 'CHECKING'
        };

        try {
            // Análise de tamanhos de arquivo
            const files = this.getCodeFiles();
            for (const file of files) {
                if (fs.existsSync(file)) {
                    const stats = fs.statSync(file);
                    performance.file_sizes[file] = {
                        size: stats.size,
                        status: stats.size > 100000 ? 'LARGE' : stats.size > 50000 ? 'MEDIUM' : 'SMALL'
                    };
                }
            }

            // Contagem de dependências
            if (fs.existsSync('package.json')) {
                const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
                const deps = Object.keys(packageJson.dependencies || {});
                const devDeps = Object.keys(packageJson.devDependencies || {});
                performance.dependency_count = deps.length + devDeps.length;
            }

        } catch (error) {
            console.warn('⚠️ Erro na auditoria de performance:', error.message);
        }

        this.results.performance = performance;
        console.log('✅ Performance auditada');
    }

    async auditTerminologyCompliance() {
        console.log('📝 Auditando compliance terminológica...');
        
        const terminologyReport = {
            violations: [],
            replacements_needed: [],
            compliance_score: 0
        };

        try {
            const files = this.getCodeFiles();
            const terminologyRules = {
                'quantum': 'advanced algorithmic',
                'neural': 'algorithmic',
                'consciousness': 'awareness',
                'transcendent': 'advanced',
                'dimensional': 'contextual'
            };

            let totalChecks = 0;
            let violations = 0;

            for (const file of files) {
                if (fs.existsSync(file)) {
                    const content = fs.readFileSync(file, 'utf8');
                    
                    for (const [term, replacement] of Object.entries(terminologyRules)) {
                        const regex = new RegExp(term, 'gi');
                        const matches = content.match(regex);
                        
                        if (matches) {
                            violations += matches.length;
                            terminologyReport.violations.push({
                                file,
                                term,
                                count: matches.length,
                                suggested_replacement: replacement
                            });
                        }
                        totalChecks++;
                    }
                }
            }

            terminologyReport.compliance_score = totalChecks > 0 ? 
                Math.round(((totalChecks - violations) / totalChecks) * 100) : 100;

        } catch (error) {
            console.warn('⚠️ Erro na auditoria terminológica:', error.message);
        }

        this.results.terminology = terminologyReport;
        console.log('✅ Compliance terminológica auditada');
    }

    async generateRecommendations() {
        console.log('💡 Gerando recomendações...');
        
        const recommendations = [];

        // Recomendações baseadas em módulos
        const missingModules = Object.entries(this.results.modules)
            .filter(([name, info]) => !info.exists || info.status === 'MISSING')
            .map(([name]) => name);

        if (missingModules.length > 0) {
            recommendations.push({
                category: 'STRUCTURE',
                priority: 'HIGH',
                description: `Módulos faltando: ${missingModules.join(', ')}`,
                action: 'Implementar módulos críticos do sistema'
            });
        }

        // Recomendações de segurança
        if (this.results.security.credentials_management === 'VULNERABLE') {
            recommendations.push({
                category: 'SECURITY',
                priority: 'CRITICAL',
                description: 'Credenciais hardcoded detectadas',
                action: 'Migrar para variáveis de ambiente'
            });
        }

        // Recomendações de governança
        if (this.results.governance.terminology_compliance === 'NEEDS_REVIEW') {
            recommendations.push({
                category: 'GOVERNANCE',
                priority: 'MEDIUM',
                description: 'Termos restritos encontrados',
                action: 'Revisar e substituir terminologia não-validada'
            });
        }

        // Recomendações de integração
        if (this.results.integration.node_modules === 'MISSING') {
            recommendations.push({
                category: 'INTEGRATION',
                priority: 'HIGH',
                description: 'Dependencies não instaladas',
                action: 'Executar npm install'
            });
        }

        this.results.recommendations = recommendations;
        console.log('✅ Recomendações geradas');
    }

    calculateOverallStatus() {
        const criticalIssues = this.results.recommendations.filter(r => r.priority === 'CRITICAL').length;
        const highIssues = this.results.recommendations.filter(r => r.priority === 'HIGH').length;
        const mediumIssues = this.results.recommendations.filter(r => r.priority === 'MEDIUM').length;

        if (criticalIssues > 0) return 'CRITICAL';
        if (highIssues > 2) return 'WARNING';
        if (highIssues > 0 || mediumIssues > 3) return 'ATTENTION';
        return 'HEALTHY';
    }

    async generateReport() {
        console.log('\n📊 RELATÓRIO DE AUDITORIA VIREON');
        console.log('═══════════════════════════════════');
        console.log(`🎯 Status Geral: ${this.results.status}`);
        console.log(`📅 Timestamp: ${this.results.timestamp}\n`);

        // Status dos módulos
        console.log('📁 MÓDULOS DO SISTEMA:');
        Object.entries(this.results.modules).forEach(([name, info]) => {
            const icon = info.exists ? '✅' : '❌';
            console.log(`${icon} ${name}: ${info.status}`);
        });

        // Governança
        console.log('\n📋 GOVERNANÇA:');
        console.log(`├─ Compliance Terminológica: ${this.results.governance.terminology_compliance}`);
        console.log(`├─ Documentação de Sessão: ${this.results.governance.session_documentation}`);
        if (this.results.governance.restricted_terms.length > 0) {
            console.log(`└─ Termos Restritos Encontrados: ${this.results.governance.restricted_terms.length}`);
        }

        // Integrações
        console.log('\n🔗 INTEGRAÇÕES:');
        Object.entries(this.results.integration).forEach(([key, value]) => {
            console.log(`├─ ${key}: ${value}`);
        });

        // Segurança
        console.log('\n🔒 SEGURANÇA:');
        Object.entries(this.results.security).forEach(([key, value]) => {
            const icon = value === 'SECURE' || value === 'IMPLEMENTED' ? '✅' : 
                        value === 'VULNERABLE' ? '🚨' : '⚠️';
            console.log(`${icon} ${key}: ${value}`);
        });

        // Performance
        console.log('\n⚡ PERFORMANCE:');
        console.log(`├─ Dependências: ${this.results.performance.dependency_count}`);
        console.log(`└─ Arquivos grandes: ${Object.values(this.results.performance.file_sizes).filter(f => f.status === 'LARGE').length}`);

        // Terminologia
        if (this.results.terminology) {
            console.log('\n📝 COMPLIANCE TERMINOLÓGICA:');
            console.log(`├─ Score: ${this.results.terminology.compliance_score}%`);
            console.log(`└─ Violações: ${this.results.terminology.violations.length}`);
        }

        // Recomendações
        if (this.results.recommendations.length > 0) {
            console.log('\n💡 RECOMENDAÇÕES:');
            this.results.recommendations.forEach((rec, index) => {
                const priorityIcon = rec.priority === 'CRITICAL' ? '🚨' : 
                                   rec.priority === 'HIGH' ? '⚠️' : '💡';
                console.log(`${priorityIcon} [${rec.priority}] ${rec.description}`);
                console.log(`   └─ Ação: ${rec.action}`);
            });
        } else {
            console.log('\n✅ Nenhuma recomendação crítica encontrada');
        }

        // Salvar relatório
        const reportFile = `vireon-audit-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
        fs.writeFileSync(reportFile, JSON.stringify(this.results, null, 2));
        console.log(`\n💾 Relatório salvo em: ${reportFile}`);
    }

    getCodeFiles() {
        const extensions = ['.js', '.ts', '.json', '.md'];
        const files = [];
        
        try {
            const dirFiles = fs.readdirSync('.');
            for (const file of dirFiles) {
                if (extensions.some(ext => file.endsWith(ext))) {
                    files.push(file);
                }
            }
        } catch (error) {
            console.warn('⚠️ Erro ao listar arquivos:', error.message);
        }
        
        return files;
    }
}

// Executar auditoria diretamente
const auditor = new VireonAuditor();
auditor.runAudit().catch(console.error);

export default VireonAuditor;
