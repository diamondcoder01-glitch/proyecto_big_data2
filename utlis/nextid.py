from conexionsupabse import conectar_db, url, key
def get_next_id(table_name: str, id_column: str): 
    try:
        supabase = conectar_db(url, key)
        data = ( supabase.table(table_name).select(id_column).order(id_column, desc=True).limit(1).execute() )

        if not data.data:
            return 1

        ultimo_id = data.data[0][id_column]
        return ultimo_id + 1

    except Exception as e:
        print("Error obteniendo siguiente ID:", e)
        return

