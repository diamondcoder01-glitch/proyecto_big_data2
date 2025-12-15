# components/carga.py
from tkinter import ttk, filedialog, simpledialog

def mostrar_carga_csv(app):
    """Interfaz para cargar archivos CSV."""
    app._limpiar_content()

    ttk.Label(app.content_frame, text="Carga de CSV",
              font=('Arial', 16, 'bold')).pack(pady=10)

    def ejecutar():
        ruta = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if ruta:
            tabla = simpledialog.askstring("Tabla", "Nombre de la tabla destino:")
            if tabla:
                app.cargador_csv.procesar(ruta, tabla)

    ttk.Button(app.content_frame, text="Seleccionar CSV",
               style='Green.TButton',
               command=ejecutar).pack(pady=20)
