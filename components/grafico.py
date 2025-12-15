# components/graficos.py
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def incrustar_grafico(app, data, titulo, xlabel, ylabel, tipo='bar'):
    """Incrustar gráfico en app.content_frame."""
    fig = _crear_figura(data, titulo, xlabel, ylabel, tipo)
    canvas = FigureCanvasTkAgg(fig, master=app.content_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=5, pady=5)
    canvas_widget.config(height=400, width=700)
    canvas.draw()


def incrustar_grafico_en_frame(app, frame, data, titulo, xlabel, ylabel, tipo='bar'):
    """Incrustar gráfico en frame específico."""
    fig = _crear_figura(data, titulo, xlabel, ylabel, tipo)
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=5, pady=5)
    canvas_widget.config(height=400, width=700)
    canvas.draw()


def _crear_figura(data, titulo, xlabel, ylabel, tipo):
    """Crear figura de Matplotlib con tamaño consistente y márgenes optimizados."""
    fig = Figure(figsize=(7, 4), dpi=100)
    ax = fig.add_subplot(111)

    if tipo == 'bar':
        data.plot(kind='bar', ax=ax, color='skyblue', width=0.7)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
    elif tipo == 'barh':
        data.sort_values().plot(kind='barh', ax=ax, color='lightcoral')
        ax.tick_params(axis='x', labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
    elif tipo == 'line':
        data.plot(kind='line', ax=ax, marker='o', color='#4caf54', linewidth=2, markersize=6)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
    elif tipo == 'pie':
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
        data.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=colors, textprops={'fontsize': 9})
        ax.set_ylabel('')

    ax.set_title(titulo, fontsize=11, fontweight='bold', pad=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout(pad=1)

    return fig
