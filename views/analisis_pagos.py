# views/analisis_pagos.py
from components.grafico import incrustar_grafico
from tkinter import ttk, messagebox

def mostrar_analisis_pagos(app):
    """Mostrar análisis de pagos con gráficos."""
    app._limpiar_content()
    
    ttk.Label(app.content_frame, text="Análisis de Pagos",
              font=('Arial', 16, 'bold')).pack(pady=10)

    resultados = app.analisis_pagos.analizar()

    if resultados is None:
        messagebox.showerror("Error", "No se pudo cargar el análisis de pagos. Revise la conexión a la base de datos.")
        return

    if resultados:
        # Mostrar tendencia mensual (línea)
        if 'mensual' in resultados and resultados['mensual'] is not None:
            incrustar_grafico(app, resultados['mensual'],
                              "Ingresos por Mes", "Mes", "Monto", tipo='line')

        # Mostrar Top 5 estudiantes por pagos (barra horizontal)
        if 'por_estudiante' in resultados and resultados['por_estudiante'] is not None:
            incrustar_grafico(app, resultados['por_estudiante'].nlargest(5),
                              "Top 5 Estudiantes por Pagos", "Monto", "ID Estudiante",
                              tipo='barh')
