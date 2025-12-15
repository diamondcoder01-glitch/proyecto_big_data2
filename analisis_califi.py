import pandas as pd
from supabase import Client
from conexionsupabse import conectar_db, url, key
import matplotlib.pyplot as plt


class AnalisisCalificaciones:
    def __init__(self):
        try:
            self.supabase: Client = conectar_db(url, key)
        except Exception as e:
            print(f"🔥 Error conectando en AnalisisCalificaciones: {e}")

    def cargar_datos(self):
        try:
            est = self.supabase.table("estudiantes").select("*").execute().data
            ins = self.supabase.table("inscripcion").select("*").execute().data
            cal = self.supabase.table("calificaciones").select("*").execute().data
            cur = self.supabase.table("curso").select("*").execute().data
            niv = self.supabase.table("nivel").select("*").execute().data

            return (
                pd.DataFrame(est),
                pd.DataFrame(ins),
                pd.DataFrame(cal),
                pd.DataFrame(cur),
                pd.DataFrame(niv),
            )
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None, None, None, None, None

    def analizar(self):
        print("\n📊 ANALIZANDO CALIFICACIONES...\n")
        try:
            df_est, df_ins, df_cal, df_cur, df_niv = self.cargar_datos()

            if df_cal is None:
                print("⚠️ No se pudo cargar la información.")
                return

            data = (
                df_cal
                .merge(df_est, on="id_estudiante", how="left")
                .merge(df_ins, on=["id_estudiante", "id_curso"], how="left")
                .merge(df_cur, on="id_curso", how="left")
                .merge(df_niv, on="id_nivel", how="left")
            )

            data["puntuacion"] = pd.to_numeric(data["puntuacion"], errors="coerce")

            promedio_nivel = data.groupby("nombre_nivel")["puntuacion"].mean()
            promedio_curso = data.groupby("id_curso")["puntuacion"].mean()
            ranking = promedio_curso.sort_values(ascending=False)

            print("📌 PROMEDIO POR NIVEL:\n", promedio_nivel)
            print("\n📌 PROMEDIO POR CURSO:\n", promedio_curso)
            print("\n🏆 RANKING:\n", ranking)

            return {
                "promedio_nivel": promedio_nivel,
                "promedio_curso": promedio_curso,
                "ranking": ranking
            }

        except Exception as e:
            print(f"🔥 Error en análisis de calificaciones: {e}")
            return None
    
    def visualizar_promedio_nivel(self, data):
        """Generar gráfico de promedio por nivel."""
        try:
            if data is not None and not data.empty:
                data.plot(kind='bar', figsize=(10, 5), title="Promedio por Nivel")
                plt.ylabel("Calificación Promedio")
                plt.xlabel("Nivel")
                plt.tight_layout()
                plt.show()
        except Exception as e:
            print(f"Error visualizando promedio nivel: {e}")
    
    def visualizar_ranking_cursos(self, data):
        """Generar gráfico de ranking de cursos."""
        try:
            if data is not None and not data.empty:
                data.plot(kind='barh', figsize=(10, 5), title="Top 5 Cursos")
                plt.xlabel("Calificación Promedio")
                plt.ylabel("Curso ID")
                plt.tight_layout()
                plt.show()
        except Exception as e:
            print(f"Error visualizando ranking cursos: {e}")
    
    