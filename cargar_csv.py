import pandas as pd
from supabase import Client
from conexionsupabse import conectar_db, url, key


class CargaCSV:
    def __init__(self):
        try:
            self.supabase: Client = conectar_db(url, key)
        except Exception as e:
            print(f"🔥 Error conectando CargaCSV: {e}")

    def cargar_archivo(self, ruta):
        try:
            df = pd.read_csv(ruta)
            print("📄 CSV cargado.")
            return df
        except FileNotFoundError:
            print("❌ Archivo no encontrado.")
        except Exception as e:
            print(f"❌ Error cargando CSV: {e}")

        return None

    def limpiar(self, df):
        try:
            print("\n🧹 LIMPIANDO...")
            df = df.drop_duplicates()
            df = df.dropna(how="all")
            df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            print("✔️ Limpieza lista.")
            return df
        except Exception as e:
            print(f"❌ Error limpiando datos: {e}")
            return df

    def insertar_supabase_masiva(self, df, tabla):
        """
        Inserta todos los registros de un DataFrame en una sola llamada a Supabase.
        Esto es mucho más eficiente para grandes volúmenes de datos (Big Data Ingesta).
        """
        if df.empty:
            print("\n⚠️ El DataFrame está vacío después de la limpieza. No hay nada que insertar.")
            return

        print(f"\n⬆️ INSERCIÓN MASIVA en la tabla '{tabla}'...")
        
        # 1. Convertir el DataFrame a una lista de diccionarios, que es el formato JSON masivo
        datos_a_insertar = df.to_dict('records')
        
        try:
            # 2. Ejecutar la inserción en bloque
            response = self.supabase.table(tabla).insert(datos_a_insertar).execute()

            # Verificación básica de la respuesta
            if response.data:
                print(f"✅ ¡Éxito! Insertados {len(response.data)} registros en '{tabla}'.")
            else:
                # Esto es raro, pero maneja el caso donde no hay error, pero tampoco datos de retorno
                print(f"✅ Inserción completada, pero no se recibieron datos de confirmación.")

        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO durante la inserción masiva en Supabase: {e}")
            print("Asegúrate de que los nombres de las columnas del CSV coincidan exactamente con la tabla.")
    
    def procesar(self, ruta_csv, tabla):
        """
        Flujo de trabajo completo: Cargar CSV -> Limpiar -> Insertar Masivamente.
        """
        try: 
            df = self.cargar_archivo(ruta_csv)
            if df is None:
                return

            df = self.limpiar(df)
            
            self.insertar_supabase_masiva(df, tabla)
            
            print("\n🎉 *Proceso de Carga de Datos Finalizado.*")
            
        except Exception as e: 
            print(f"\n❌ ERROR FATAL en el proceso de carga: {e}")
            print("Verifique la ruta, el formato del CSV y la conexión a Supabase.")