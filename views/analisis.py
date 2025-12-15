# views/analisis.py
from components.grafico import incrustar_grafico
from tkinter import ttk, messagebox

def mostrar_analisis_calificaciones(app):
    """Mostrar análisis de calificaciones con gráficos."""
    app._limpiar_content()

    ttk.Label(app.content_frame, text="Análisis de Calificaciones",
              font=('Arial', 16, 'bold')).pack(pady=10)

    resultados = app.analisis_calif.analizar()

    if resultados is None:
        messagebox.showerror("Error", "No se pudo cargar el análisis de calificaciones. Revise la conexión a la base de datos.")
        return
    
    elif resultados:
        incrustar_grafico(app, resultados['promedio_nivel'],
                          "Promedio por Nivel", "Nivel", "Calificación Promedio")
        incrustar_grafico(app, resultados['ranking'].head(5),
                          "Top 5 Cursos", "Curso ID", "Calificación Promedio", tipo='barh')

