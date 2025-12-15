# views/crud_estudiantes.py
import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_crud_estudiantes(app):
    """
    Renderiza la vista CRUD dentro de app.content_frame
    """

    # --- TITULO ---
    ttk.Label(app.content_frame, text="Gestión de Estudiantes (CRUD)",
              font=('Arial', 16, 'bold')).pack(pady=10)

    # --- BOTONES ---
    btn_frame = tk.Frame(app.content_frame, bg='#35373b')
    btn_frame.pack(pady=5, fill='x')

    ttk.Button(btn_frame, text="➕ Registrar",
               style='Green.TButton',
               command=lambda: app.mostrar_formulario_registro()
               ).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="✏️ Editar",
               style='Green.TButton',
               command=app.editar_estudiante
               ).pack(side='left', padx=5)

    ttk.Button(btn_frame, text="🗑️ Eliminar",
               style='Green.TButton',
               command=app.eliminar_estudiante
               ).pack(side='left', padx=5)

    # --- FILTROS / BUSCADOR ---
    search_frame = tk.Frame(app.content_frame, bg='#35373b')
    search_frame.pack(pady=10, fill='x', padx=10)

    ttk.Label(search_frame, text="🔍 Buscar por nombre/ID:").pack(side='left', padx=5)
    app.search_entry = ttk.Entry(search_frame, width=20)
    app.search_entry.pack(side='left', padx=5)
    app.search_entry.bind("<KeyRelease>", lambda e: app._filtrar_tabla())

    ttk.Label(search_frame, text="Nivel:").pack(side='left', padx=5)
    app.nivel_combo = ttk.Combobox(search_frame, width=15, state='readonly')
    app.nivel_combo.pack(side='left', padx=5)
    app.nivel_combo.bind("<<ComboboxSelected>>", lambda e: app._filtrar_tabla())

    ttk.Label(search_frame, text="Curso:").pack(side='left', padx=5)
    app.curso_combo = ttk.Combobox(search_frame, width=15, state='readonly')
    app.curso_combo.pack(side='left', padx=5)
    app.curso_combo.bind("<<ComboboxSelected>>", lambda e: app._filtrar_tabla())

    ttk.Button(search_frame, text="🔄 Limpiar",
               command=app._limpiar_filtros).pack(side='left', padx=5)

    # --- DATOS ---
    app.cargar_estudiantes_completo()
    app.mostrar_tabla_estudiantes()
