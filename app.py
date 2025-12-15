import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from estudiante import GestorEstudiantesSupabase
from analisis_califi import AnalisisCalificaciones
from analisi_pago import AnalisisPagos
from analisis_avanzados import AnalisisAvanzados
from cargar_csv import CargaCSV

# Importar módulos de vistas
from views.crud_estudiante import mostrar_crud_estudiantes as vista_crud
from views.analisis import mostrar_analisis_calificaciones
from views.analisis_pagos import mostrar_analisis_pagos
from views.analisis_avanzado import mostrar_analisis_avanzado
from components.carga import mostrar_carga_csv


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cedife - Instituto Inglés")
        self.geometry("1000x700")
        self.configure(bg='#35373b')

        # Inicializar servicios
        self.gestor_estudiantes = GestorEstudiantesSupabase()
        self.analisis_calif = AnalisisCalificaciones()
        self.analisis_pagos = AnalisisPagos()
        self.analisis_avanzados = AnalisisAvanzados()
        self.cargador_csv = CargaCSV()

        # UI frames
        self.nav_frame = ttk.Frame(self, padding="10")
        self.nav_frame.pack(side="top", fill="x")

        self.content_frame = tk.Frame(self, bg='#35373b')
        self.content_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

        self._crear_botones_navegacion()
        self.mostrar_crud_estudiantes()

    def _crear_botones_navegacion(self):
        """Crear barra de navegación con 6 botones principales."""
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('TFrame', background='#35373b')
        s.configure('TLabel', background='#35373b', foreground='white')
        s.configure('Green.TButton', background='#4caf54', foreground='white', 
                   font=('Arial', 10, 'bold'), borderwidth=1, relief='sunken')
        s.map('Green.TButton', background=[('active', '#45a049'), ('pressed', '#3d8b40')])
        
        ttk.Button(self.nav_frame, text="✅ CRUD Estudiantes", style='Green.TButton', 
                  command=self.mostrar_crud_estudiantes).pack(side="left", padx=5)
        ttk.Button(self.nav_frame, text="📊 Análisis Calificaciones", style='Green.TButton', 
                  command=lambda: mostrar_analisis_calificaciones(self)).pack(side="left", padx=5)
        ttk.Button(self.nav_frame, text="💰 Análisis de Pagos", style='Green.TButton', 
                  command=lambda: mostrar_analisis_pagos(self)).pack(side="left", padx=5)
        ttk.Button(self.nav_frame, text="📈 Análisis Avanzado", style='Green.TButton', 
                  command=lambda: mostrar_analisis_avanzado(self)).pack(side="left", padx=5)
        ttk.Button(self.nav_frame, text="⬆️ Cargar CSV", style='Green.TButton', 
                  command=lambda: mostrar_carga_csv(self)).pack(side="left", padx=5)
        ttk.Button(self.nav_frame, text="👋 Salir", style='Green.TButton', 
                  command=self.quit).pack(side="right", padx=5)

    def _limpiar_content(self):
        """Destruir todos los widgets en content_frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_crud_estudiantes(self):
        """Delegar a módulo de vistas."""
        self._limpiar_content()
        vista_crud(self)

    # --- MÉTODOS CRUD COMPARTIDOS ---
    
    def cargar_estudiantes_completo(self):
        """Cargar datos para filtrado local."""
        try:
            self.estudiantes_list = self.gestor_estudiantes.supabase.table("estudiantes").select("*").execute().data or []
            inscripciones = self.gestor_estudiantes.supabase.table("inscripcion").select("*").execute().data or []
            cursos = self.gestor_estudiantes.supabase.table("curso").select("*").execute().data or []
            niveles = self.gestor_estudiantes.supabase.table("nivel").select("*").execute().data or []
            
            self.curso_map = {c['id_curso']: c for c in cursos}
            self.nivel_map = {n['id_nivel']: n for n in niveles}
            self.inscripcion_map = {ins['id_estudiante']: ins for ins in inscripciones}
            
            niveles_unicos = sorted(set(n.get('nombre_nivel', 'N/A') for n in niveles if n.get('nombre_nivel')))
            cursos_unicos = sorted(set(c.get('nombre_curso', 'N/A') for c in cursos if c.get('nombre_curso')))
            
            if hasattr(self, 'nivel_combo'):
                self.nivel_combo['values'] = [''] + niveles_unicos
            if hasattr(self, 'curso_combo'):
                self.curso_combo['values'] = [''] + cursos_unicos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar datos: {e}")

    def _filtrar_tabla(self):
        """Filtrar tabla por búsqueda y combos."""
        search_text = self.search_entry.get().lower()
        nivel_filter = self.nivel_combo.get() if hasattr(self, 'nivel_combo') else ''
        curso_filter = self.curso_combo.get() if hasattr(self, 'curso_combo') else ''
        
        filtered = []
        for est in self.estudiantes_list:
            match_search = (search_text == '' or 
                          search_text in est.get('nombre', '').lower() or
                          search_text in est.get('apellido', '').lower() or
                          search_text in str(est.get('id_estudiante', '')).lower())
            
            if not match_search:
                continue
            
            match_nivel = True
            if nivel_filter:
                ins = self.inscripcion_map.get(est.get('id_estudiante'))
                if ins:
                    id_curso = ins.get('id_curso')
                    curso = self.curso_map.get(id_curso, {})
                    id_nivel = curso.get('id_nivel')
                    nivel = self.nivel_map.get(id_nivel, {})
                    match_nivel = nivel.get('nombre_nivel', '') == nivel_filter
                else:
                    match_nivel = False
            
            match_curso = True
            if curso_filter:
                ins = self.inscripcion_map.get(est.get('id_estudiante'))
                if ins:
                    id_curso = ins.get('id_curso')
                    curso = self.curso_map.get(id_curso, {})
                    match_curso = curso.get('nombre_curso', '') == curso_filter
                else:
                    match_curso = False
            
            if match_search and match_nivel and match_curso:
                filtered.append(est)
        
        self._actualizar_tabla_con_datos(filtered)

    def _limpiar_filtros(self):
        """Limpiar todos los filtros."""
        self.search_entry.delete(0, tk.END)
        self.nivel_combo.set('')
        self.curso_combo.set('')
        self._actualizar_tabla_con_datos(self.estudiantes_list)

    def _actualizar_tabla_con_datos(self, estudiantes):
        """Actualizar Treeview con datos."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for est in estudiantes:
            self.tree.insert("", "end", values=(
                est.get('id_estudiante', ''),
                est.get('nombre', ''),
                est.get('apellido', ''),
                est.get('telefono', ''),
                est.get('correo', '')
            ))
                
    def mostrar_tabla_estudiantes(self):
        """Crear Treeview para estudiantes."""
        tree = ttk.Treeview(self.content_frame, columns=("ID", "Nombre", "Apellido", "Teléfono", "Correo"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Apellido", text="Apellido")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Correo", text="Correo")
        
        self.tree = tree

        for est in self.estudiantes_list:
            tree.insert("", "end", values=(
                est.get('id_estudiante', ''),
                est.get('nombre', ''),
                est.get('apellido', ''),
                est.get('telefono', ''),
                est.get('correo', '')
            ))

        tree.pack(fill='both', expand=True, pady=10)
        tree.bind("<Double-1>", self._on_tree_double_click)

    def _on_tree_double_click(self, event):
        """Abrir formulario en modo edición."""
        sel = self.tree.selection()
        if not sel:
            return
        item = sel[0]
        values = self.tree.item(item, 'values')
        if not values:
            return
        try:
            id_est = int(values[0])
        except Exception:
            id_est = values[0]

        try:
            resp = self.gestor_estudiantes.supabase.table("estudiantes").select("*").eq("id_estudiante", id_est).execute()
            if resp.data:
                self.mostrar_formulario_registro(resp.data[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener datos: {e}")

    def editar_estudiante(self):
        """Editar estudiante seleccionado."""
        if not hasattr(self, 'tree'):
            messagebox.showwarning("Aviso", "No hay datos cargados.")
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un estudiante.")
            return
        item = sel[0]
        values = self.tree.item(item, 'values')
        try:
            id_est = int(values[0])
        except Exception:
            id_est = values[0]
        try:
            resp = self.gestor_estudiantes.supabase.table("estudiantes").select("*").eq("id_estudiante", id_est).execute()
            if resp.data:
                self.mostrar_formulario_registro(resp.data[0])
            else:
                messagebox.showerror("Error", "No se encontró el estudiante.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar: {e}")

    def eliminar_estudiante(self):
        """Eliminar estudiante seleccionado."""
        if not hasattr(self, 'tree'):
            messagebox.showwarning("Aviso", "No hay datos cargados.")
            return
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un estudiante.")
            return
        item = sel[0]
        values = self.tree.item(item, 'values')
        try:
            id_est = int(values[0])
        except Exception:
            id_est = values[0]

        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar estudiante {id_est}?")
        if not confirm:
            return
        try:
            self.gestor_estudiantes.supabase.table("estudiantes").delete().eq("id_estudiante", id_est).execute()
            self.mostrar_crud_estudiantes()
            messagebox.showinfo("Eliminado", f"Estudiante {id_est} eliminado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def mostrar_formulario_registro(self, estudiante=None):
        """Formulario para registrar/editar estudiante."""
        ventana_registro = tk.Toplevel(self)
        if estudiante:
            ventana_registro.title("Editar Estudiante")
        else:
            ventana_registro.title("Registrar Nuevo Estudiante")
        ventana_registro.geometry("450x520")
        ventana_registro.configure(bg='#35373b')
        
        frame_form = tk.Frame(ventana_registro, bg='#35373b')
        frame_form.pack(padx=15, pady=15, fill="both", expand=True)
        
        titulo = "Editar Estudiante" if estudiante else "Nuevo Estudiante"
        ttk.Label(frame_form, text=titulo, font=('Arial', 14, 'bold')).pack(pady=10)
        
        frame_campos = tk.Frame(frame_form, bg='#35373b')
        frame_campos.pack(fill="both", expand=True)
        
        campos = [
            ("Nombre", "nombre"),
            ("Apellido", "apellido"),
            ("Sexo (M/F)", "sexo"),
            ("Fecha Nac. (YYYY-MM-DD)", "fecha_nac"),
            ("Teléfono", "telefono"),
            ("Cédula", "cedula"),
            ("Dirección", "direccion"),
            ("Correo", "correo")
        ]
        
        entries = {}
        
        for idx, (label_text, campo_key) in enumerate(campos):
            lbl = ttk.Label(frame_campos, text=f"{label_text}:")
            lbl.grid(row=idx, column=0, sticky="w", pady=6, padx=(0, 10))
            
            entry = ttk.Entry(frame_campos, width=28)
            entry.grid(row=idx, column=1, sticky="ew", pady=6)
            entries[campo_key] = entry
        
        if estudiante:
            for k, v in estudiante.items():
                if k in entries:
                    entries[k].delete(0, tk.END)
                    entries[k].insert(0, str(v))
        
        frame_campos.columnconfigure(1, weight=1)
        
        frame_botones = tk.Frame(frame_form, bg='#35373b')
        frame_botones.pack(pady=15, fill="x")
        
        def guardar_estudiante():
            try:
                from tkinter import messagebox as mb
                datos = {campo_key: entries[campo_key].get().strip() for _, campo_key in campos}
                
                if not datos['nombre'] or not datos['apellido'] or not datos['telefono'] or not datos['cedula']:
                    raise ValueError("Campos requeridos: nombre, apellido, teléfono, cédula.")
                if datos['sexo'].upper() not in ('M', 'F'):
                    raise ValueError("El sexo debe ser 'M' o 'F'.")
                
                from utlis.calcularedad import calcular_edad
                edad = calcular_edad(datos['fecha_nac'])
                if edad is None:
                    raise ValueError("Formato de fecha inválido (YYYY-MM-DD).")
                
                if estudiante:
                    id_edit = estudiante.get('id_estudiante')
                    update_data = {
                        "nombre": datos['nombre'],
                        "apellido": datos['apellido'],
                        "sexo": datos['sexo'].upper(),
                        "edad": edad,
                        "fecha_nac": datos['fecha_nac'],
                        "cedula": datos['cedula'],
                        "direccion": datos['direccion'],
                        "telefono": datos['telefono'],
                        "correo": datos['correo']
                    }
                    resp = self.gestor_estudiantes.supabase.table("estudiantes").update(update_data).eq("id_estudiante", id_edit).execute()
                    if resp.data is not None:
                        mb.showinfo("Éxito", f"Estudiante {id_edit} actualizado.")
                        ventana_registro.destroy()
                        self.mostrar_crud_estudiantes()
                    else:
                        mb.showerror("Error", "No se pudo actualizar.")
                else:
                    from utlis.nextid import get_next_id
                    nuevo_id = get_next_id("estudiantes", "id_estudiante")
                    if nuevo_id is None:
                        raise ValueError("No se pudo obtener el ID siguiente.")

                    self.gestor_estudiantes.supabase.table("estudiantes").insert({
                        "id_estudiante": nuevo_id,
                        "nombre": datos['nombre'],
                        "apellido": datos['apellido'],
                        "sexo": datos['sexo'].upper(),
                        "edad": edad,
                        "fecha_nac": datos['fecha_nac'],
                        "cedula": datos['cedula'],
                        "direccion": datos['direccion'],
                        "telefono": datos['telefono'],
                        "correo": datos['correo']
                    }).execute()

                    mb.showinfo("Éxito", f"Estudiante registrado con ID: {nuevo_id}")
                    ventana_registro.destroy()
                    self.mostrar_crud_estudiantes()
            
            except ValueError as ve:
                from tkinter import messagebox as mb
                mb.showerror("Error de Validación", str(ve))
            except Exception as e:
                import traceback
                traceback.print_exc()
                from tkinter import messagebox as mb
                mb.showerror("Error", f"Error al registrar: {str(e)}")
        
        def cancelar():
            ventana_registro.destroy()
        
        ttk.Button(frame_botones, text="Guardar cambios" if estudiante else "✅ Guardar", 
                  command=guardar_estudiante, style='Green.TButton').pack(side="left", padx=5)
        ttk.Button(frame_botones, text="❌ Cancelar", command=cancelar).pack(side="left", padx=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
