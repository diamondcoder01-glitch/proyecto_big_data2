from supabase import Client

def buscar_por_id(supabase_client: Client, nombre_tabla: str, nombre_columna_id: str):
    
    print(f"\n🔍 BUSCAR REGISTRO EN TABLA '{nombre_tabla.upper()}' POR ID")
    try:
        supabase = supabase_client
        
        # Pedir el ID al usuario
        id_buscar = input(f"Ingrese el ID a buscar en {nombre_tabla}: ").strip()

        if not id_buscar.isdigit():
            raise ValueError("El ID debe ser un número entero.")
        
        id_int = int(id_buscar)

        # 1. Ejecutar la consulta de forma genérica
        # Usamos nombre_columna_id para el filtro .eq()
        data = supabase.table(nombre_tabla) \
            .select("*") \
            .eq(nombre_columna_id, id_int) \
            .execute() 

        if not data.data:
            print(f"\n❌ No se encontró ningún registro con ID {id_buscar} en la tabla '{nombre_tabla}'.")
            return None # Retorna None si no encuentra nada

        # 2. Mostrar el resultado
        registro = data.data[0]
        print(f"\n✅ Registro encontrado en '{nombre_tabla}':")
        for key, value in registro.items():
            print(f"**{key.replace('_', ' ').title()}**: {value}")
        
        return registro # Retorna el diccionario del registro encontrado

    except ValueError as ve:
        print(f"\n❌ {ve}")
    except Exception as e:
        print(f"\n🔥 Error al buscar en {nombre_tabla}: {e}")
        return None