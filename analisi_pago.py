import pandas as pd
from supabase import Client
from conexionsupabse import conectar_db, url, key
import matplotlib.pyplot as plt


class AnalisisPagos:
    def __init__(self):
        try:
            self.supabase: Client = conectar_db(url, key)
        except Exception as e:
            print(f"🔥 Error conectando AnalisisPagos: {e}")

    def cargar_datos(self):
        try:
            est = self.supabase.table("estudiantes").select("*").execute().data
            pag = self.supabase.table("pago").select("*").execute().data

            return pd.DataFrame(est), pd.DataFrame(pag)
        except Exception as e:
            print(f"❌ Error cargando pagos: {e}")
            return None, None

    def analizar(self):
        print("\n💰 ANALIZANDO PAGOS...\n")
        try:
            df_est, df_pag = self.cargar_datos()

            if df_pag is None or df_pag.empty:
                print("⚠️ No hay pagos registrados.")
                return

            df_pag["fecha_pago"] = pd.to_datetime(df_pag["fecha_pago"], errors="coerce")

            total = df_pag["monto"].sum()
            pagos_mes = df_pag.groupby(df_pag["fecha_pago"].dt.to_period("M"))["monto"].sum().rename(lambda x: str(x))
            pagos_estudiante = df_pag.groupby("id_estudiante")["monto"].sum()

            print("💵 TOTAL:", total)
            print("📅 POR MES:\n", pagos_mes)
            print("👤 POR ESTUDIANTE:\n", pagos_estudiante)

            return {
                "total": total,
                "mensual": pagos_mes,
                "por_estudiante": pagos_estudiante
            }

        except Exception as e:
            print(f"🔥 Error analizando pagos: {e}")
            return None

    def visualizar_ingresos_mensuales(self, data):
        """Generar gráfico de ingresos mensuales."""
        try:
            if data is not None and not data.empty:
                data.plot(kind='line', figsize=(10, 5), title="Ingresos por Mes")
                plt.ylabel("Monto")
                plt.xlabel("Mes")
                plt.tight_layout()
                plt.show()
        except Exception as e:
            print(f"Error visualizando ingresos mensuales: {e}")
    
    def visualizar_top_ingresos(self, data):
        """Generar gráfico de top ingresos por estudiante."""
        try:
            if data is not None and not data.empty:
                data.nlargest(5).plot(kind='barh', figsize=(10, 5), title="Top 5 Estudiantes por Pagos")
                plt.xlabel("Monto")
                plt.ylabel("ID Estudiante")
                plt.tight_layout()
                plt.show()
        except Exception as e:
            print(f"Error visualizando top ingresos: {e}")

    