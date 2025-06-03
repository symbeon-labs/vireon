use std::{io, sync::Arc, time::Duration};
use tokio::sync::Mutex;
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use tui::{
    backend::{Backend, CrosstermBackend},
    layout::{Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    symbols,
    text::{Span, Spans},
    widgets::{Block, Borders, Chart, Dataset, Gauge, List, ListItem, Paragraph},
    Frame, Terminal,
};

use crate::{
    monitoring::ContinuousMonitor,
    core::{
        quantum::QuantumState,
        metrics::QuantumMetrics,
        consciousness::ConsciousnessState,
    },
};

/// Estrutura principal do dashboard
pub struct DashboardUI {
    monitor: Arc<Mutex<ContinuousMonitor>>,
    quantum_history: Vec<(f64, f64)>,
    consciousness_history: Vec<(f64, f64)>,
    alerts: Vec<String>,
    selected_tab: usize,
}

impl DashboardUI {
    /// Cria nova instância do dashboard
    pub fn new(monitor: Arc<Mutex<ContinuousMonitor>>) -> Self {
        Self {
            monitor,
            quantum_history: Vec::with_capacity(100),
            consciousness_history: Vec::with_capacity(100),
            alerts: Vec::new(),
            selected_tab: 0,
        }
    }

    /// Inicia o dashboard
    pub async fn run(&mut self) -> io::Result<()> {
        // Terminal setup
        enable_raw_mode()?;
        let mut stdout = io::stdout();
        execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
        let backend = CrosstermBackend::new(stdout);
        let mut terminal = Terminal::new(backend)?;

        // Main loop
        let res = self.run_app(&mut terminal).await;

        // Cleanup
        disable_raw_mode()?;
        execute!(
            terminal.backend_mut(),
            LeaveAlternateScreen,
            DisableMouseCapture
        )?;
        terminal.show_cursor()?;

        res
    }

    async fn run_app<B: Backend>(&mut self, terminal: &mut Terminal<B>) -> io::Result<()> {
        let tick_rate = Duration::from_millis(250);
        let mut last_tick = tokio::time::Instant::now();

        loop {
            terminal.draw(|f| self.draw(f))?;

            let timeout = tick_rate
                .checked_sub(last_tick.elapsed())
                .unwrap_or_else(|| Duration::from_secs(0));

            if event::poll(timeout)? {
                if let Event::Key(key) = event::read()? {
                    match key.code {
                        KeyCode::Char('q') => return Ok(()),
                        KeyCode::Tab => {
                            self.selected_tab = (self.selected_tab + 1) % 4;
                        }
                        KeyCode::Left => {
                            if self.selected_tab > 0 {
                                self.selected_tab -= 1;
                            }
                        }
                        KeyCode::Right => {
                            if self.selected_tab < 3 {
                                self.selected_tab += 1;
                            }
                        }
                        _ => {}
                    }
                }
            }

            if last_tick.elapsed() >= tick_rate {
                self.update_data().await;
                last_tick = tokio::time::Instant::now();
            }
        }
    }

    /// Atualiza dados do dashboard
    async fn update_data(&mut self) {
        let monitor = self.monitor.lock().await;
        
        // Atualiza histórico quântico
        if let Ok(metrics) = monitor.get_quantum_metrics().await {
            let timestamp = monitor.get_current_timestamp().as_secs_f64();
            self.quantum_history.push((timestamp, metrics.coherence));
            if self.quantum_history.len() > 100 {
                self.quantum_history.remove(0);
            }
        }

        // Atualiza histórico de consciência
        if let Ok(state) = monitor.get_consciousness_state().await {
            let timestamp = monitor.get_current_timestamp().as_secs_f64();
            self.consciousness_history.push((timestamp, state.level));
            if self.consciousness_history.len() > 100 {
                self.consciousness_history.remove(0);
            }
        }

        // Atualiza alertas
        if let Ok(new_alerts) = monitor.get_alerts().await {
            self.alerts = new_alerts;
        }
    }

    fn draw<B: Backend>(&self, f: &mut Frame<B>) {
        let size = f.size();

        // Layout principal
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .margin(1)
            .constraints([
                Constraint::Length(3),  // Título
                Constraint::Min(0),     // Conteúdo principal
                Constraint::Length(3),  // Status bar
            ])
            .split(size);

        // Renderiza título
        self.draw_title(f, chunks[0]);

        // Layout do conteúdo principal
        let main_chunks = Layout::default()
            .direction(Direction::Horizontal)
            .constraints([
                Constraint::Percentage(70),
                Constraint::Percentage(30),
            ])
            .split(chunks[1]);

        // Renderiza painéis principais baseado na tab selecionada
        match self.selected_tab {
            0 => self.draw_quantum_view(f, main_chunks[0]),
            1 => self.draw_consciousness_view(f, main_chunks[0]),
            2 => self.draw_metrics_view(f, main_chunks[0]),
            3 => self.draw_system_view(f, main_chunks[0]),
            _ => {}
        }

        // Sempre renderiza alertas no painel direito
        self.draw_alerts(f, main_chunks[1]);
        
        // Renderiza status bar
        self.draw_status_bar(f, chunks[2]);
    }

    fn draw_title<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let title = Paragraph::new(Spans::from(vec![
            Span::styled(
                "VIREON Quantum Monitor ",
                Style::default()
                    .fg(Color::Cyan)
                    .add_modifier(Modifier::BOLD)
            ),
            Span::raw("- Press 'q' to quit"),
        ]))
        .block(Block::default().borders(Borders::ALL));

        f.render_widget(title, area);
    }

    fn draw_quantum_view<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .constraints([
                Constraint::Percentage(50),
                Constraint::Percentage(50),
            ])
            .split(area);

        // Gráfico de coerência quântica
        let quantum_dataset = Dataset::default()
            .name("Quantum Coherence")
            .marker(symbols::Marker::Braille)
            .style(Style::default().fg(Color::Cyan))
            .data(&self.quantum_history);

        let chart = Chart::new(vec![quantum_dataset])
            .block(Block::default().title("Quantum State").borders(Borders::ALL))
            .x_axis(
                tui::widgets::Axis::default()
                    .style(Style::default().fg(Color::Gray))
                    .bounds([
                        self.quantum_history.first().map(|p| p.0).unwrap_or(0.0),
                        self.quantum_history.last().map(|p| p.0).unwrap_or(100.0),
                    ])
            )
            .y_axis(
                tui::widgets::Axis::default()
                    .style(Style::default().fg(Color::Gray))
                    .bounds([0.0, 1.0])
            );

        f.render_widget(chart, chunks[0]);

        // Métricas quânticas detalhadas
        let metrics_block = Block::default()
            .title("Quantum Metrics")
            .borders(Borders::ALL);
        f.render_widget(metrics_block, chunks[1]);
    }

    fn draw_consciousness_view<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .constraints([
                Constraint::Percentage(50),
                Constraint::Percentage(50),
            ])
            .split(area);

        // Gráfico de nível de consciência
        let consciousness_dataset = Dataset::default()
            .name("Consciousness Level")
            .marker(symbols::Marker::Braille)
            .style(Style::default().fg(Color::Magenta))
            .data(&self.consciousness_history);

        let chart = Chart::new(vec![consciousness_dataset])
            .block(Block::default().title("Consciousness Evolution").borders(Borders::ALL))
            .x_axis(
                tui::widgets::Axis::default()
                    .style(Style::default().fg(Color::Gray))
                    .bounds([
                        self.consciousness_history.first().map(|p| p.0).unwrap_or(0.0),
                        self.consciousness_history.last().map(|p| p.0).unwrap_or(100.0),
                    ])
            )
            .y_axis(
                tui::widgets::Axis::default()
                    .style(Style::default().fg(Color::Gray))
                    .bounds([0.0, 1.0])
            );

        f.render_widget(chart, chunks[0]);

        // Estados de consciência detalhados
        let details_block = Block::default()
            .title("Consciousness States")
            .borders(Borders::ALL);
        f.render_widget(details_block, chunks[1]);
    }

    fn draw_metrics_view<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let metrics_block = Block::default()
            .title("System Metrics")
            .borders(Borders::ALL);
        f.render_widget(metrics_block, area);
    }

    fn draw_system_view<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let system_block = Block::default()
            .title("System Status")
            .borders(Borders::ALL);
        f.render_widget(system_block, area);
    }

    fn draw_alerts<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let alerts: Vec<ListItem> = self.alerts
            .iter()
            .map(|alert| {
                ListItem::new(vec![Spans::from(Span::styled(
                    alert,
                    Style::default().fg(Color::Red),
                ))])
            })
            .collect();

        let alerts_list = List::new(alerts)
            .block(Block::default().title("Active Alerts").borders(Borders::ALL))
            .style(Style::default().fg(Color::White))
            .highlight_style(Style::default().add_modifier(Modifier::BOLD))
            .highlight_symbol(">> ");

        f.render_widget(alerts_list, area);
    }

    fn draw_status_bar<B: Backend>(&self, f: &mut Frame<B>, area: Rect) {
        let status = Paragraph::new(format!(
            "Tab: {} | Press TAB to switch views",
            match self.selected_tab {
                0 => "Quantum",
                1 => "Consciousness",
                2 => "Metrics",
                3 => "System",
                _ => "Unknown",
            }
        ))
        .style(Style::default().fg(Color::White))
        .block(Block::default().borders(Borders::ALL));

        f.render_widget(status, area);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::monitoring::tests::create_test_monitor;

    #[tokio::test]
    async fn test_dashboard_creation() {
        let monitor = create_test_monitor().await;
        let dashboard = DashboardUI::new(Arc::new(Mutex::new(monitor)));
        assert_eq!(dashboard.selected_tab, 0);
        assert!(dashboard.quantum_history.is_empty());
        assert!(dashboard.consciousness_history.is_empty());
    }

    #[tokio::test]
    async fn test_data_update() {
        let monitor = create_test_monitor().await;
        let mut dashboard = DashboardUI::new(Arc::new(Mutex::new(monitor)));
        dashboard.update_data().await;
        assert!(!dashboard.quantum_history.is_empty());
        assert!(!dashboard.consciousness_history.is_empty());
    }
}

