# VIREON Neural Interface

Esta interface neural foi projetada para o projeto VIREON, apresentando uma visualização gamificada e interativa do sistema. A interface inclui:

- Visualização de rede neural interativa
- Terminal de comandos simulado
- Dashboard de métricas do sistema
- Tema claro/escuro
- Animações e efeitos visuais avançados

## Configuração do Projeto

Devido a possíveis corrupções nos arquivos existentes, alguns arquivos foram criados com extensão `.new`. Siga estas instruções para configurar o projeto:

1. Renomeie os arquivos `.new` para substituir os originais:

```powershell
# No PowerShell
Move-Item -Path ".\frontend\package.json.new" -Destination ".\frontend\package.json" -Force
Move-Item -Path ".\frontend\tailwind.config.js.new" -Destination ".\frontend\tailwind.config.js" -Force
Move-Item -Path ".\frontend\src\index.css.new" -Destination ".\frontend\src\index.css" -Force
```

2. Instale as dependências necessárias:

```bash
cd frontend
npm install
npm install -D tailwindcss postcss autoprefixer tw-animate-css
npx tailwindcss init -p
```

3. Execute a aplicação em modo de desenvolvimento:

```bash
npm run dev
```

## Estrutura de Arquivos

- `src/neural-styles.css` - Estilos personalizados com animações e temas
- `src/VireonApp.tsx` - Componente principal da aplicação
- `src/components/NeuralDashboard.tsx` - Interface neural interativa
- `tailwind.config.js` - Configuração do Tailwind CSS
- `postcss.config.js` - Configuração do PostCSS

## Recursos Implementados

- **Nós Neurais Interativos**: Representação visual de componentes do sistema VIREON
- **Terminal Simulado**: Interface de linha de comando para interação com o sistema
- **Métricas em Tempo Real**: Visualização de métricas do sistema com atualizações dinâmicas
- **Modo Escuro/Claro**: Suporte a temas com transição suave
- **Efeitos Visuais Avançados**: Animações, glass morphism, e efeitos de hover
- **Interfaces Responsivas**: Layout adaptável a diferentes tamanhos de tela

## Personalização

Você pode personalizar facilmente a interface:

- Edite `neural-styles.css` para modificar animações e efeitos visuais
- Ajuste os nós e conexões em `NeuralDashboard.tsx`
- Adicione novos componentes e métricas conforme necessário
