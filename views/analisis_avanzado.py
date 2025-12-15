# views/analisis_avanzado.py
import tkinter as tk
from tkinter import ttk
from components.grafico import incrustar_grafico_en_frame


def mostrar_analisis_avanzado(app):
    """Mostrar análisis avanzado con tabs de navegación."""
    app._limpiar_content()

    ttk.Label(app.content_frame, text="Análisis Avanzado",
              font=('Arial', 16, 'bold')).pack(pady=10)

    frame_tabs = tk.Frame(app.content_frame, bg='#35373b')
    frame_tabs.pack(pady=5, fill='x')

    ttk.Button(frame_tabs, text="📍 Distribución",
               style='Green.TButton',
               command=lambda: _render(app, "dist")).pack(side='left', padx=5)

    ttk.Button(frame_tabs, text="📋 Asistencia",
               style='Green.TButton',
               command=lambda: _render(app, "asis")).pack(side='left', padx=5)

    ttk.Button(frame_tabs, text="🏆 Comparativa",
               style='Green.TButton',
               command=lambda: _render(app, "comp")).pack(side='left', padx=5)

    # FRAME donde irán los gráficos
    app.analisis_frame = tk.Frame(app.content_frame, bg='#35373b')
    app.analisis_frame.pack(fill='both', expand=True, padx=10, pady=10)

    _render(app, "dist")  # vista por defecto


def _render(app, modo):
    """Renderizar gráfico según modo seleccionado."""
    # Limpiar frame anterior
    for w in app.analisis_frame.winfo_children():
        w.destroy()

    if modo == "dist":
        data = app.analisis_avanzados.analizar_distribucion_estudiantes()
        if data and 'distribucion_nivel' in data:
            incrustar_grafico_en_frame(app, app.analisis_frame,
                                       data['distribucion_nivel'],
                                       "Distribución por Nivel",
                                       "Nivel", "Cantidad", tipo='pie')
        else:
            ttk.Label(app.analisis_frame, text="⚠️ No hay datos disponibles.", foreground='orange').pack(pady=20)

    elif modo == "asis":
        data = app.analisis_avanzados.analizar_asistencia()
        if data and 'asistencia_promedio' in data:
            incrustar_grafico_en_frame(app, app.analisis_frame,
                                       data['asistencia_promedio'].head(10),
                                       "Top 10 Asistencia", "Porcentaje",
                                       "Estudiante", tipo='barh')
        else:
            ttk.Label(app.analisis_frame, text="⚠️ No hay datos de asistencia.", foreground='orange').pack(pady=20)

    elif modo == "comp":
        data = app.analisis_avanzados.analizar_comparativa_niveles()
        if data and 'comparativa_niveles' in data:
            incrustar_grafico_en_frame(app, app.analisis_frame,
                                       data['comparativa_niveles']['mean'],
                                       "Promedio por Nivel",
                                       "Nivel", "Calificación Promedio", tipo='bar')
        else:
            ttk.Label(app.analisis_frame, text="⚠️ No hay datos de comparativa.", foreground='orange').pack(pady=20)

