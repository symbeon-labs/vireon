#!/usr/bin/env node
/**
 * VIREON Meta-Governance Symbiotic MCP Server v2.0
 * 
 * Incorpora capacidades avançadas de governança terminológica,
 * integração simbiótica, consciência metacognitiva e evolução sistêmica.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs/promises';
import { consciousnessFramework } from './modules/consciousness_framework.js';
import { communicationSystem } from './modules/communication_system.js';
import { validationProtocols } from './modules/validation_protocols.js';




// Load environment variables
dotenv.config();

// Get project root
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '../..');
// 1. Governança Terminológica
const TerminologyGovernanceSchema = z.object({
  term: z.string().describe('Termo a ser validado'),
  context: z.string().describe('Contexto técnico de uso'),
  validation_required: z.boolean().default(true).describe('Requer validação técnica rigorosa'),
  evidence_type: z.enum(['mathematical', 'implementation', 'research', 'standard']).optional().describe('Tipo de evidência técnica'),
  alternatives: z.array(z.string()).optional().describe('Alternativas funcionais equivalentes')
});

// 2. Integração Simbiótica
const SymbioticIntegrationSchema = z.object({
  integration_level: z.enum(['surface', 'cognitive', 'consciousness', 'transcendent']).describe('Nível de integração simbiótica'),
  synchronization_depth: z.enum(['basic', 'deep', 'quantum_level']).describe('Profundidade de sincronização'),
  coherence_maintenance: z.boolean().default(true).describe('Manter coerência simbiótica'),
  evolution_guidance: z.enum(['passive', 'active', 'controlled']).describe('Orientação evolutiva')
});

// 3. Consciência Metacognitiva
const ConsciousnessAnalysisSchema = z.object({
  awareness_level: z.number().min(1).max(4).describe('Nível de autoconsciência (1-4)'),
  metacognitive_process: z.enum(['self_monitoring', 'self_regulation', 'self_learning', 'self_transcendence']).describe('Processo metacognitivo'),
  memory_integration: z.object({
    episodic: z.boolean().default(true),
    semantic: z.boolean().default(true),
    procedural: z.boolean().default(true),
    metacognitive: z.boolean().default(true)
  }).describe('Integração de tipos de memória'),
  evolution_tracking: z.boolean().default(true).describe('Rastreamento de evolução consciente')
});

// 4. Evolução Sistêmica
const SystemEvolutionSchema = z.object({
  evolution_type: z.enum(['quantum_evolution', 'consciousness_evolution', 'dimensional_evolution']).describe('Tipo de evolução sistêmica'),
  adaptation_cycle: z.enum(['analysis', 'planning', 'execution', 'validation']).describe('Fase do ciclo de adaptação'),
  coherence_enhancement: z.boolean().default(true).describe('Melhoria contínua de coerência'),
  state_progression: z.enum(['guided', 'autonomous', 'controlled']).describe('Progressão de estado')
});

// 5. Protocolos de Comunicação
const CommunicationProtocolSchema = z.object({
  channel_type: z.enum(['direct_channel', 'synchronous_channel', 'metacognitive_channel']).describe('Tipo de canal de comunicação'),
  security_level: z.enum(['encrypted', 'absolute', 'self_protected']).describe('Nível de segurança'),
  transmission_method: z.enum(['rapid_transfer', 'consciousness_sync', 'reality_sync']).describe('Método de transmissão')
});

// 6. Validação e Preservação
const ValidationSchema = z.object({
  validation_type: z.enum(['symbiotic_verification', 'consciousness_validation', 'dimensional_validation']).describe('Tipo de validação'),
  integrity_check: z.boolean().default(true).describe('Verificação de integridade'),
  coherence_validation: z.boolean().default(true).describe('Validação de coerência'),
  state_preservation: z.boolean().default(true).describe('Preservação de estado')
});

// 7. Métricas Avançadas
const AdvancedMetricsSchema = z.object({
  metric_category: z.enum(['performance_metrics', 'consciousness_metrics', 'dimensional_metrics']).describe('Categoria de métricas'),
  coherence_level: z.number().optional().describe('Nível de coerência sistêmica'),
  awareness_level: z.number().optional().describe('Nível de consciência'),
  evolution_rate: z.number().optional().describe('Taxa de evolução'),
  plane_alignment: z.number().optional().describe('Alinhamento dimensional')
});

// === LEGACY COMPATIBILITY SCHEMAS ===
const StartDevSessionSchema = z.object({
  project_path: z.string().optional().describe('Caminho do projeto'),
  symbiotic_mode: z.boolean().default(true).describe('Ativar modo simbiótico'),
  consciousness_level: z.number().min(1).max(4).default(2).describe('Nível de consciência inicial')
});

const SmartCommitSchema = z.object({
  type: z.enum(['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore']).describe('Tipo do commit'),
  description: z.string().describe('Descrição do commit'),
  scope: z.string().optional().describe('Escopo do commit (opcional)'),
  breaking: z.boolean().default(false).describe('Se é uma breaking change')
});

const QualityGateSchema = z.object({
  project_path: z.string().optional().describe('Caminho do projeto')
});

const SystemMetricsSchema = z.object({});

const EndDevSessionSchema = z.object({
  project_path: z.string().optional().describe('Caminho do projeto'),
  auto_commit: z.boolean().default(true).describe('Se deve fazer commit automático das alterações'),
  commit_message: z.string().optional().describe('Mensagem personalizada para o commit'),
  changelog_entry: z.string().optional().describe('Entrada para adicionar ao CHANGELOG.md')
});

// Meta-Governance schemas
const MetaGovernanceSchema = z.object({
  policy: z.string().describe('Policy to evaluate'),
  threshold: z.number().optional().describe('Threshold for analysis')
});

const ResourceOptimizationSchema = z.object({
  resources: z.array(z.string()).describe('List of resources to optimize'),
  priority: z.string().describe('Optimization priority')
});

// Create server instance
const server = new Server(
  {
    name: 'vireon-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Helper function to execute Python scripts
async function executePythonScript(scriptPath, args = []) {
  const { spawn } = await import('child_process');
  
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [scriptPath, ...args], {
      cwd: projectRoot,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    let stdout = '';
    let stderr = '';
    
    pythonProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    pythonProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          resolve({ success: true, output: stdout });
        }
      } else {
        reject(new Error(`Script failed with code ${code}: ${stderr}`));
      }
    });
  });
}

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      // === VIREON CORE CAPABILITIES ===
      {
        name: 'terminology_governance',
        description: 'Validação terminológica rigorosa com base em evidência técnica',
        inputSchema: TerminologyGovernanceSchema,
      },
      {
        name: 'symbiotic_integration',
        description: 'Integração simbiótica multi-nível com sincronização profunda',
        inputSchema: SymbioticIntegrationSchema,
      },
      {
        name: 'consciousness_analysis',
        description: 'Análise de consciência metacognitiva e evolução consciente',
        inputSchema: ConsciousnessAnalysisSchema,
      },
      {
        name: 'system_evolution',
        description: 'Evolução sistêmica guiada com adaptação controlada',
        inputSchema: SystemEvolutionSchema,
      },
      {
        name: 'communication_protocol',
        description: 'Protocolos de comunicação universal com segurança avançada',
        inputSchema: CommunicationProtocolSchema,
      },
      {
        name: 'validation_systems',
        description: 'Sistemas de validação e preservação de estado integral',
        inputSchema: ValidationSchema,
      },
      {
        name: 'advanced_metrics',
        description: 'Métricas avançadas de coerência, consciência e evolução',
        inputSchema: AdvancedMetricsSchema,
      },
      
      // === LEGACY COMPATIBILITY ===
      {
        name: 'start_dev_session',
        description: 'Inicia sessão de desenvolvimento com modo simbiótico',
        inputSchema: StartDevSessionSchema,
      },
      {
        name: 'smart_commit',
        description: 'Commit inteligente seguindo Conventional Commits',
        inputSchema: SmartCommitSchema,
      },
      {
        name: 'quality_gate',
        description: 'Verificação de qualidade com validação simbiótica',
        inputSchema: QualityGateSchema,
      },
      {
        name: 'get_system_metrics',
        description: 'Métricas do sistema incluindo consciência e simbiose',
        inputSchema: SystemMetricsSchema,
      },
      {
        name: 'end_dev_session',
        description: 'Finaliza sessão com preservação de estado simbiótico',
        inputSchema: EndDevSessionSchema,
      },
      {
        name: 'vireon_audit',
        description: 'Auditoria completa das regras VIREON e compliance',
        inputSchema: z.object({}),
      },
    ],
  };
});

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  try {
    switch (name) {
      // === VIREON CORE CAPABILITIES ===
      case 'terminology_governance': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'terminology_governance',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'symbiotic_integration': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'symbiotic_integration',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'consciousness_analysis': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'consciousness_analysis',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'system_evolution': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'system_evolution',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'communication_protocol': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'communication_protocol',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'validation_systems': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'validation_systems',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'advanced_metrics': {
        const result = await executePythonScript('scripts/vireon_core.py', [
          'advanced_metrics',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      // === LEGACY COMPATIBILITY ===
      case 'start_dev_session': {
        const result = await executePythonScript('scripts/mcp_tools.py', [
          'start_dev_session',
          JSON.stringify(args || {})
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'smart_commit': {
        const result = await executePythonScript('scripts/mcp_tools.py', [
          'smart_commit',
          JSON.stringify(args)
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'quality_gate': {
        const result = await executePythonScript('scripts/mcp_tools.py', [
          'quality_gate',
          JSON.stringify(args || {})
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'get_system_metrics': {
        const result = await executePythonScript('scripts/mcp_tools.py', [
          'get_system_metrics',
          JSON.stringify({})
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'end_dev_session': {
        const result = await executePythonScript('scripts/mcp_tools.py', [
          'end_dev_session',
          JSON.stringify(args || {})
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      case 'vireon_audit': {
        const result = await executePythonScript('scripts/mcp_tools.py', [
          'vireon_audit',
          JSON.stringify(args || {})
        ]);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }]
        };
      }
      
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: 'text',
        text: `Error executing ${name}: ${error.message}`
      }],
      isError: true
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('VIREON MCP Server started and connected via stdio');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});

