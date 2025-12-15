from estudiante import GestorEstudiantesSupabase
from analisis_califi import AnalisisCalificaciones
from analisi_pago import AnalisisPagos
from cargar_csv import CargaCSV


class Main:
    def __init__(self):
        self.estudiantes = GestorEstudiantesSupabase()
        self.calificaciones = AnalisisCalificaciones()
        self.pagos = AnalisisPagos()
        self.csv = CargaCSV()

    def menu(self):
        while True:
            print("""
============= SISTEMA BIG DATA - INSTITUTO INGLÉS =============
1. CRUD Estudiantes
2. Análisis de Calificaciones
3. Análisis de Pagos
4. Cargar CSV a Supabase
5. Salir
===============================================================
""")

            op = input("Seleccione una opción: ")

            if op == "1":
                self.estudiantes.menu()
            elif op == "2":
                self.calificaciones.analizar()
            elif op == "3":
                self.pagos.analizar()
            elif op == "4":
                archivo = input("Ruta del CSV: ")
                tabla = input("Nombre de la tabla destino: ")
                self.csv.procesar(archivo, tabla)
            elif op == "5":
                print("👋 Saliendo...")
                break
            else:
                print("❌ Opción inválida.")


if __name__ == "__main__":
    Main().menu()