import pandas as pd
from supabase import Client
from conexionsupabse import conectar_db, url, key
import matplotlib.pyplot as plt


class AnalisisAvanzados:
    """Análisis adicionales: distribución, asistencia, comparativas, etc."""
    
    def __init__(self):
        try:
            self.supabase: Client = conectar_db(url, key)
        except Exception as e:
            print(f"🔥 Error conectando AnalisisAvanzados: {e}")

    def cargar_datos(self):
        try:
            est = self.supabase.table("estudiantes").select("*").execute().data
            cal = self.supabase.table("calificaciones").select("*").execute().data
            ins = self.supabase.table("inscripcion").select("*").execute().data
            cur = self.supabase.table("curso").select("*").execute().data
            niv = self.supabase.table("nivel").select("*").execute().data

            return (
                pd.DataFrame(est),
                pd.DataFrame(cal),
                pd.DataFrame(ins),
                pd.DataFrame(cur),
                pd.DataFrame(niv),
            )
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return None, None, None, None, None

    def analizar_distribucion_estudiantes(self):
        """Análisis de distribución de estudiantes por nivel."""
        print("\n📊 ANÁLISIS DE DISTRIBUCIÓN DE ESTUDIANTES...\n")
        try:
            df_est, df_cal, df_ins, df_cur, df_niv = self.cargar_datos()

            if df_est is None or df_est.empty:
                print("⚠️ No hay estudiantes registrados.")
                return None

            # Contar estudiantes por nivel (a través de inscripciones)
            if df_ins.empty or df_cur.empty or df_niv.empty:
                print("⚠️ Faltan datos de inscripciones, cursos o niveles.")
                print(f"   Inscripciones: {len(df_ins)} registros")
                print(f"   Cursos: {len(df_cur)} registros")
                print(f"   Niveles: {len(df_niv)} registros")
                return None

            # Merge paso a paso con debug
            print(f"Merging inscripción con curso...")
            data = df_ins.merge(df_cur, on="id_curso", how="left", suffixes=('_ins', '_cur'))
            print(f"  Resultado: {len(data)} filas")
            
            print(f"Merging con nivel...")
            data = data.merge(df_niv, on="id_nivel", how="left")
            print(f"  Resultado: {len(data)} filas")

            print(f"Agrupando por nombre_nivel...")
            dist_nivel = data.groupby("nombre_nivel").size()
            print(f"  Resultado:\n{dist_nivel}")

            return {"distribucion_nivel": dist_nivel}

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"🔥 Error en análisis de distribución: {e}")
            return None

    def analizar_asistencia(self):
        """Análisis de asistencia promedio."""
        print("\n📋 ANÁLISIS DE ASISTENCIA...\n")
        try:
            df_est, df_cal, df_ins, df_cur, df_niv = self.cargar_datos()

            if df_cal is None or df_cal.empty:
                print("⚠️ No hay datos de calificaciones/asistencia.")
                return None

            # Convertir asistencia a porcentaje numérico
            df_cal["asistencia_num"] = df_cal["asistencia"].str.rstrip('%').astype(float, errors='ignore')

            # Promedios por estudiante
            asistencia_promedio = (
                df_cal
                .merge(df_est, on="id_estudiante", how="left")
                .groupby("nombre")["asistencia_num"]
                .mean()
                .sort_values(ascending=False)
            )

            print("📌 PROMEDIO DE ASISTENCIA POR ESTUDIANTE:\n", asistencia_promedio)

            return {"asistencia_promedio": asistencia_promedio}

        except Exception as e:
            print(f"🔥 Error en análisis de asistencia: {e}")
            return None

    def analizar_comparativa_niveles(self):
        """Comparativa de calificaciones promedio por nivel."""
        print("\n🏆 COMPARATIVA POR NIVEL...\n")
        try:
            df_est, df_cal, df_ins, df_cur, df_niv = self.cargar_datos()

            if df_cal is None or df_cal.empty:
                print("⚠️ No hay datos de calificaciones.")
                return None

            df_cal["puntuacion"] = pd.to_numeric(df_cal["puntuacion"], errors="coerce")

            data = (
                df_cal
                .merge(df_est, on="id_estudiante", how="left")
                .merge(df_ins, on=["id_estudiante", "id_curso"], how="left")
                .merge(df_cur, on="id_curso", how="left")
                .merge(df_niv, on="id_nivel", how="left")
            )

            comparativa = data.groupby("nombre_nivel")["puntuacion"].agg(['mean', 'std', 'count'])
            print("📌 COMPARATIVA DE CALIFICACIONES:\n", comparativa)

            return {"comparativa_niveles": comparativa}

        except Exception as e:
            print(f"🔥 Error en comparativa: {e}")
            return None

    def visualizar_distribucion_nivel(self, data_serie):
        """Gráfico circular de distribución por nivel."""
        plt.figure(figsize=(10, 6))
        data_serie.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
        plt.title('Distribución de Estudiantes por Nivel', fontsize=14, fontweight='bold')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    def visualizar_asistencia(self, data_serie):
        """Gráfico de barras de asistencia promedio."""
        plt.figure(figsize=(12, 6))
        data_serie.sort_values(ascending=True).plot(kind='barh', color='#95E1D3')
        plt.title('Promedio de Asistencia por Estudiante', fontsize=14, fontweight='bold')
        plt.xlabel('Porcentaje de Asistencia (%)', fontsize=12)
        plt.ylabel('Estudiante', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()

    def visualizar_comparativa_niveles(self, data_df):
        """Gráfico de barras agrupadas para comparativa de niveles."""
        plt.figure(figsize=(12, 6))
        data_df['mean'].plot(kind='bar', color='#6C5CE7', label='Promedio')
        plt.title('Calificación Promedio por Nivel', fontsize=14, fontweight='bold')
        plt.xlabel('Nivel', fontsize=12)
        plt.ylabel('Calificación', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.show()
