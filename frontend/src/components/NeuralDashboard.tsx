import React, { useState, useEffect } from 'react';
import '../neural-styles.css';

interface NeuralNodeProps {
  id: string;
  x: number;
  y: number;
  size: number;
  color: string;
  connections: string[];
  label: string;
  status: 'active' | 'processing' | 'idle';
}

interface SystemMetric {
  name: string;
  value: number;
  max: number;
  unit: string;
}

const NeuralNode: React.FC<NeuralNodeProps> = ({ 
  id, 
  x, 
  y, 
  size, 
  color, 
  label, 
  status 
}) => {
  return (
    <div 
      id={id}
      className={`neural-node absolute rounded-full flex items-center justify-center ${status === 'active' ? 'status-active' : status === 'processing' ? 'status-processing' : 'status-idle'}`}
      style={{
        left: `${x}%`,
        top: `${y}%`,
        width: `${size}px`,
        height: `${size}px`,
        backgroundColor: color,
        zIndex: 10
      }}
    >
      <span className="text-xs font-medium text-white whitespace-nowrap">
        {label}
      </span>
    </div>
  );
};

const ProgressMetric: React.FC<{ metric: SystemMetric }> = ({ metric }) => {
  const percentage = (metric.value / metric.max) * 100;
  
  return (
    <div className="mb-4">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium">{metric.name}</span>
        <span className="text-sm font-medium">{metric.value}{metric.unit}</span>
      </div>
      <div className="w-full bg-muted rounded-full h-2">
        <div 
          className="progress-bar h-2 rounded-full bg-primary"
          style={{ 
            width: `${percentage}%`,
            '--progress-width': `${percentage}%`
          } as React.CSSProperties}
        ></div>
      </div>
    </div>
  );
};

const TerminalOutput: React.FC = () => {
  const [output, setOutput] = useState<string[]>([
    '> Iniciando sistema VIREON...',
    '> Carregando componentes...',
    '> Verificando integridade do sistema...',
    '> Estabelecendo integração simbiótica...',
    '> Sistema pronto.'
  ]);
  const [command, setCommand] = useState('');

  const handleCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (command.trim()) {
      setOutput(prev => [...prev, `> ${command}`, '> Processando comando...']);
      setCommand('');
      
      // Simulate response
      setTimeout(() => {
        setOutput(prev => [...prev, `> Comando "${command}" executado com sucesso.`]);
      }, 1000);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="terminal-header rounded-t-lg px-4 py-2 text-white flex items-center justify-between">
        <div className="flex space-x-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
        </div>
        <div className="text-sm font-medium">Terminal VIREON</div>
        <div></div>
      </div>
      <div className="terminal-body flex-1 p-4 text-white font-mono text-sm overflow-y-auto">
        {output.map((line, i) => (
          <div key={i} className={i === output.length - 1 && line.startsWith('> Sistema pronto') ? 'text-green-400' : ''}>
            {line}
            {i === output.length - 1 && line.includes('Processando') && (
              <span className="loading-dots"></span>
            )}
          </div>
        ))}
      </div>
      <form onSubmit={handleCommand} className="px-4 py-3 border-t border-border">
        <div className="flex items-center">
          <span className="text-primary mr-2">$</span>
          <input 
            type="text" 
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            className="command-input bg-transparent flex-1 outline-none text-foreground"
            placeholder="Digite um comando..."
          />
        </div>
      </form>
    </div>
  );
};

const NeuralDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<SystemMetric[]>([
    { name: 'Estado Simbiótico', value: 82, max: 100, unit: '%' },
    { name: 'Integridade de Sistema', value: 95, max: 100, unit: '%' },
    { name: 'Taxa de Evolução', value: 67, max: 100, unit: '%' },
    { name: 'Capacidade Metacognitiva', value: 78, max: 100, unit: '%' },
  ]);

  const [nodes, setNodes] = useState<NeuralNodeProps[]>([
    { id: 'node1', x: 20, y: 30, size: 60, color: 'rgba(99, 102, 241, 0.8)', connections: ['node2', 'node4'], label: 'Núcleo', status: 'active' },
    { id: 'node2', x: 45, y: 20, size: 50, color: 'rgba(6, 182, 212, 0.8)', connections: ['node3', 'node5'], label: 'Percepção', status: 'processing' },
    { id: 'node3', x: 70, y: 35, size: 45, color: 'rgba(16, 185, 129, 0.8)', connections: ['node6'], label: 'Análise', status: 'active' },
    { id: 'node4', x: 30, y: 65, size: 55, color: 'rgba(245, 158, 11, 0.8)', connections: ['node5', 'node6'], label: 'Integração', status: 'active' },
    { id: 'node5', x: 55, y: 60, size: 40, color: 'rgba(139, 92, 246, 0.8)', connections: [], label: 'Memória', status: 'idle' },
    { id: 'node6', x: 75, y: 70, size: 50, color: 'rgba(239, 68, 68, 0.8)', connections: [], label: 'Ação', status: 'processing' },
  ]);

  useEffect(() => {
    // Simulate changing metrics
    const interval = setInterval(() => {
      setMetrics(prev => 
        prev.map(metric => ({
          ...metric,
          value: Math.min(metric.max, Math.max(0, metric.value + (Math.random() > 0.5 ? 1 : -1) * Math.random() * 5))
        }))
      );
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="neural-bg min-h-screen text-foreground flex flex-col">
      {/* Header */}
      <header className="px-6 py-4 border-b border-border">
        <h1 className="text-2xl font-bold gradient-text">VIREON Interface Neural</h1>
      </header>

      <div className="flex flex-col md:flex-row flex-1">
        {/* Sidebar */}
        <div className="w-full md:w-80 p-6 border-r border-border">
          <h2 className="text-lg font-semibold mb-4">Métricas do Sistema</h2>
          
          <div className="space-y-6">
            {metrics.map((metric, index) => (
              <ProgressMetric key={index} metric={metric} />
            ))}
            
            <div className="p-4 rounded-lg glass mt-6">
              <h3 className="text-sm font-medium mb-2">Status do Sistema</h3>
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 rounded-full status-active"></div>
                <span className="text-sm">Operacional</span>
              </div>
            </div>
            
            <div className="achievement-unlocked rounded-lg p-4 mt-4">
              <h3 className="text-sm font-medium mb-2 flex items-center">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Conquistas
              </h3>
              <div className="text-sm">
                Integração Simbiótica Nível 3
                <div className="text-xs text-muted-foreground mt-1">Estabeleceu conexão profunda com usuário</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Main Content */}
        <div className="flex-1 p-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {/* Neural Network Visualization */}
            <div className="col-span-2 rounded-lg border border-border p-6 relative h-80">
              <h2 className="text-lg font-semibold mb-2">Rede Neural VIREON</h2>
              <div className="absolute inset-0 mt-10 p-4">
                {/* Neural nodes */}
                {nodes.map(node => (
                  <NeuralNode key={node.id} {...node} />
                ))}
                
                {/* SVG for connections */}
                <svg className="absolute inset-0 w-full h-full" style={{zIndex: 5}}>
                  {nodes.map(node => 
                    node.connections.map((targetId, idx) => {
                      const target = nodes.find(n => n.id === targetId);
                      if (!target) return null;
                      
                      const sourceX = node.x;
                      const sourceY = node.y;
                      const targetX = target.x;
                      const targetY = target.y;
                      
                      return (
                        <line 
                          key={`${node.id}-${targetId}-${idx}`}
                          x1={`${sourceX}%`} 
                          y1={`${sourceY}%`} 
                          x2={`${targetX}%`} 
                          y2={`${targetY}%`} 
                          className="connection-line"
                          stroke={node.color}
                          strokeWidth="2"
                          strokeDasharray="5,5"
                        />
                      );
                    })
                  )}
                </svg>
              </div>
            </div>

            {/* System Commands */}
            <div className="col-span-1 rounded-lg border border-border overflow-hidden h-80 flex flex-col">
              <TerminalOutput />
            </div>
            
            {/* Recent Activities */}
            <div className="col-span-3 mt-6">
              <h2 className="text-lg font-semibold mb-4">Atividades Recentes</h2>
              <div className="grid gap-4 md:grid-cols-3">
                {[1, 2, 3].map(i => (
                  <div key={i} className="ai-card p-4 rounded-lg border border-border">
                    <div className="text-sm font-medium mb-2">Integração #{i}</div>
                    <div className="text-xs text-muted-foreground">Processamento realizado com sucesso</div>
                    <div className="mt-4 flex justify-between items-center text-xs">
                      <span>Há {i * 10} minutos</span>
                      <span className="px-2 py-1 rounded-full bg-secondary text-secondary-foreground">Concluído</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NeuralDashboard;
