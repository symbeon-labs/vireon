use eframe::egui;
use std::sync::Arc;
use anyhow::Result;
use chrono::Utc;

use crate::dashboard::widgets::log_viewer::{
    LogViewer,
    LogFilter,
    LogLevel,
    LogColumn,
    ExportFormat,
};

pub struct LogViewerUI {
    viewer: Arc<LogViewer>,
    filter: LogFilter,
    selected_entry: Option<String>,
    auto_refresh: bool,
}

impl LogViewerUI {
    pub fn new(viewer: Arc<LogViewer>) -> Self {
        Self {
            viewer,
            filter: LogFilter {
                text_search: None,
                levels: vec![LogLevel::Info, LogLevel::Warning, LogLevel::Error],
                time_range: None,
                quantum_state_filter: None,
                metric_threshold: None,
            },
            selected_entry: None,
            auto_refresh: true,
        }
    }

    pub fn ui(&mut self, ui: &mut egui::Ui) -> Result<()> {
        self.toolbar_ui(ui)?;
        ui.separator();
        self.log_table_ui(ui)?;
        ui.separator();
        if let Some(entry_id) = &self.selected_entry {
            self.details_panel_ui(ui, entry_id)?;
        }
        Ok(())
    }

    fn toolbar_ui(&mut self, ui: &mut egui::Ui) -> Result<()> {
        ui.horizontal(|ui| {
            // Nível de Log
            ui.label("Níveis:");
            for level in [LogLevel::Info, LogLevel::Warning, LogLevel::Error, LogLevel::Critical] {
                let mut enabled = self.filter.levels.contains(&level);
                if ui.checkbox(&mut enabled, format!("{:?}", level)).changed() {
                    if enabled {
                        self.filter.levels.push(level);
                    } else {
                        self.filter.levels.retain(|l| l != &level);
                    }
                }
            }

            ui.separator();

            // Busca
            ui.label("Buscar:");
            if let Some(text) = &mut self.filter.text_search {
                if ui.text_edit_singleline(text).changed() {
                    // Atualiza filtro em tempo real
                }
            }

            ui.separator();

            // Controles
            if ui.button("Exportar JSON").clicked() {
                if let Ok(data) = pollster::block_on(self.viewer.export_logs(ExportFormat::Json)) {
                    // Implementar salvamento do arquivo
                }
            }
            if ui.button("Exportar CSV").clicked() {
                if let Ok(data) = pollster::block_on(self.viewer.export_logs(ExportFormat::Csv)) {
                    // Implementar salvamento do arquivo
                }
            }

            let mut auto_refresh = self.auto_refresh;
            if ui.checkbox(&mut auto_refresh, "Auto Refresh").changed() {
                self.auto_refresh = auto_refresh;
            }
        });
        Ok(())
    }

    fn log_table_ui(&mut self, ui: &mut egui::Ui) -> Result<()> {
        egui::ScrollArea::vertical()
            .auto_shrink([false; 2])
            .show(ui, |ui| {
                egui::Grid::new("log_grid")
                    .striped(true)
                    .spacing([4.0, 4.0])
                    .show(ui, |ui| {
                        // Cabeçalho
                        ui.label("Timestamp");
                        ui.label("Nível");
                        ui.label("Mensagem");
                        ui.label("Contexto Quântico");
                        ui.label("Métricas");
                        ui.end_row();

                        // Dados
                        if let Ok(logs) = pollster::block_on(self.viewer.get_logs(Some(self.filter.clone()))) {
                            for log in logs {
                                ui.label(log.timestamp.to_rfc3339());
                                ui.label(format!("{:?}", log.level));
                                ui.label(&log.message);
                                
                                if let Some(ctx) = log.quantum_context {
                                    ui.label(format!("Q:{:.2}", ctx.quantum_state));
                                } else {
                                    ui.label("-");
                                }

                                if let Some(metrics) = log.metrics {
                                    ui.label(format!("M:{}", metrics.len()));
                                } else {
                                    ui.label("-");
                                }

                                ui.end_row();
                            }
                        }
                    });
            });
        Ok(())
    }

    fn details_panel_ui(&mut self, ui: &mut egui::Ui, entry_id: &str) -> Result<()> {
        ui.group(|ui| {
            ui.heading("Detalhes do Log");
            
            if let Ok(metrics) = pollster::block_on(self.viewer.correlate_metrics(entry_id.to_string())) {
                ui.collapsing("Métricas Correlacionadas", |ui| {
                    for (key, value) in metrics {
                        ui.label(format!("{}: {}", key, value));
                    }
                });
            }

            if let Ok(trends) = pollster::block_on(self.viewer.analyze_trends()) {
                ui.collapsing("Tendências", |ui| {
                    // Exibe gráficos de tendências
                    plot_trends(ui, &trends);
                });
            }
        });
        Ok(())
    }
}

fn plot_trends(ui: &mut egui::Ui, trends: &LogTrends) {
    use egui_plot::{Plot, Points, Line};

    // Plot de evolução de consciência
    Plot::new("consciousness_evolution")
        .height(120.0)
        .show(ui, |plot_ui| {
            if let Some(points) = trends.consciousness_evolution
                .iter()
                .map(|(t, s)| [t.timestamp() as f64, s.level as f64])
                .collect::<Vec<_>>()
            {
                plot_ui.line(Line::new(points));
            }
        });

    // Plot de métricas
    for (metric_name, values) in &trends.metric_patterns {
        Plot::new(format!("metric_{}", metric_name))
            .height(100.0)
            .show(ui, |plot_ui| {
                if let Some(points) = values
                    .iter()
                    .enumerate()
                    .map(|(i, v)| [i as f64, v.as_f64()])
                    .collect::<Vec<_>>()
                {
                    plot_ui.line(Line::new(points));
                }
            });
    }
}

