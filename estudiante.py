from dotenv import load_dotenv
from supabase import Client # Asegúrate de que tienes la biblioteca 'supabase' instalada
from conexionsupabse import conectar_db, url, key
from utlis.nextid import get_next_id
from utlis.calcularedad import calcular_edad
from utlis.buscarID import buscar_por_id
# Cargar variables de entorno del archivo .env
load_dotenv()

class GestorEstudiantesSupabase:

    def __init__(self):
        """
        Inicializa la conexión con Supabase usando el módulo externo.
        """
        self.supabase: Client = self._inicializar_conexion()
        
    # --- Métodos de Conexión y Auxiliares Internos ---

    def _inicializar_conexion(self) -> Client:
        """
        Llama a la función de conexión externa.
        Retorna el objeto Cliente de Supabase o termina el programa si falla.
        """
        # 2. LLAMAR a la función importada
        supabase_client: Client = conectar_db(url, key)
        
        if supabase_client is None:
            # Si conectar_db retorna None, la conexión falló o faltan credenciales
            print("\n🔥 ERROR CRÍTICO: La conexión a Supabase falló. El programa terminará.")
            exit()
            
        return supabase_client
    
    def agregar_estudiante(self):
        """
        Solicita datos y agrega un nuevo estudiante a la base de datos.
        """
        print("\n✏️ AGREGAR NUEVO ESTUDIANTE")
        try:
            nombre = input("Escribe el nombre: ").strip()
            if not nombre: raise ValueError("No puedes insertar un nombre vacío.")

            apellido = input("Escribe el apellido: ").strip()
            if not apellido: raise ValueError("No puedes insertar un apellido vacío.")

            sexo = input("Sexo (M/F): ").strip()
            if not sexo or sexo.upper() not in ('M', 'F'): raise ValueError("El sexo debe ser 'M' o 'F'.")

            fecha_nac = input("Fecha de nacimiento (YYYY-MM-DD): ").strip()
            edad = calcular_edad(fecha_nac)
            if edad is None: raise ValueError("Formato de fecha de nacimiento inválido (debe ser YYYY-MM-DD).")

            telefono = input("Escribe el teléfono: ").strip()
            if not telefono: raise ValueError("No puedes insertar un teléfono vacío.")

            cedula = input("Escribe la cédula: ").strip()
            if not cedula: raise ValueError("No puedes insertar una cédula vacía.")

            direccion = input("Escribe la dirección: ").strip()
            if not direccion: raise ValueError("No puedes insertar una dirección vacía.")

            correo = input("Ingresa el correo: ").strip()
            if not correo: raise ValueError("No puedes insertar un correo vacío.")

            nuevo_id = get_next_id("estudiantes", "id_estudiante")
            if nuevo_id is None:
                print("\n❌ No se pudo obtener el ID siguiente.")
                return

            # Insertar datos
            insertar = self.supabase.table("estudiantes").insert({
                "id_estudiante": nuevo_id,
                "nombre": nombre,
                "apellido": apellido,
                "sexo": sexo,
                "edad": edad,
                "fecha_nac": fecha_nac,
                "cedula": cedula,
                "direccion": direccion,
                "telefono": telefono,
                "correo": correo
            }).execute()

            if insertar.data:
                print(f"\n✅ Registro agregado correctamente con ID **{nuevo_id}**")
            else:
                # Supabase a veces no devuelve el error detallado, pero verifica la respuesta
                print("\n❌ Ocurrió un error al insertar (posible error de Supabase/esquema).")

        except ValueError as ve:
            print(f"\n❌ {ve}")
        except Exception as e:
            print(f"\n🔥 Error inesperado al agregar datos: {e}")

    
    def buscar_por_id(self):
        buscar_por_id(
            supabase_client=self.supabase, 
            nombre_tabla="estudiantes", 
            nombre_columna_id="id_estudiante"
        )
    def listar_estudiantes(self):
        """
        Lista todos los estudiantes registrados.
        """
        print("\n📋 LISTA DE ESTUDIANTES")
        try:
            # Obtener todos los estudiantes
            data = self.supabase.table("estudiantes").select("*").order("id_estudiante").execute()

            if not data.data:
                print("\n⚠️ No hay estudiantes registrados.")
                return

            print("-" * 50)
            for est in data.data:
                print(f"**ID**: {est['id_estudiante']} | **Nombre**: {est['nombre']} {est['apellido']} | "
                      f"**Tel**: {est['telefono']} | **Correo**: {est['correo']}")
            print("-" * 50)
            print("\n✔️ Fin de la lista")

        except Exception as e:
            print(f"\n🔥 Error al listar estudiantes: {e}")

    def actualizar_estudiante(self):
        """
        Permite actualizar los datos de un estudiante por su ID.
        """
        print("\n🔄 ACTUALIZAR ESTUDIANTE")
        try:
            id_edit = input("Ingrese el ID del estudiante a actualizar: ").strip()

            if not id_edit.isdigit():
                raise ValueError("El ID debe ser un número entero.")

            id_edit_int = int(id_edit)

            # 1. Buscar si existe
            data = self.supabase.table("estudiantes").select("*").eq("id_estudiante", id_edit_int).execute()

            if not data.data:
                print("\n❌ No existe un estudiante con ese ID.")
                return

            print("\nDeje el campo vacío si **no** quiere modificarlo.")

            nombre = input(f"Nuevo nombre (Actual: {data.data[0]['nombre']}): ").strip()
            apellido = input(f"Nuevo apellido (Actual: {data.data[0]['apellido']}): ").strip()
            sexo = input(f"Nuevo sexo (M/F) (Actual: {data.data[0]['sexo']}): ").strip()
            fecha_nac = input(f"Nueva fecha de nacimiento (YYYY-MM-DD) (Actual: {data.data[0]['fecha_nac']}): ").strip()
            telefono = input(f"Nuevo teléfono (Actual: {data.data[0]['telefono']}): ").strip()
            cedula = input(f"Nueva cédula (Actual: {data.data[0]['cedula']}): ").strip()
            direccion = input(f"Nueva dirección (Actual: {data.data[0]['direccion']}): ").strip()
            correo = input(f"Nuevo correo (Actual: {data.data[0]['correo']}): ").strip()

            update_data = {}

            if nombre: update_data["nombre"] = nombre
            if apellido: update_data["apellido"] = apellido
            if sexo: update_data["sexo"] = sexo
            if fecha_nac:
                edad = self._calcular_edad(fecha_nac)
                if edad is None:
                    raise ValueError("Formato de fecha inválido (debe ser YYYY-MM-DD).")
                update_data["fecha_nac"] = fecha_nac
                update_data["edad"] = edad # También actualiza la edad si cambia la fecha
            if telefono: update_data["telefono"] = telefono
            if cedula: update_data["cedula"] = cedula
            if direccion: update_data["direccion"] = direccion
            if correo: update_data["correo"] = correo

            if not update_data:
                print("\n⚠️ No se ingresaron cambios.")
                return

            # Realizar la actualización
            self.supabase.table("estudiantes").update(update_data).eq("id_estudiante", id_edit_int).execute()

            print("\n✅ Estudiante actualizado correctamente.")

        except ValueError as ve:
            print(f"\n❌ {ve}")
        except Exception as e:
            print(f"\n🔥 Error al actualizar: {e}")

    def eliminar_estudiante(self):
        """
        Elimina un estudiante de la base de datos por su ID.
        """
        print("\n🗑️ ELIMINAR ESTUDIANTE")
        try:
            id_delete = input("Ingrese el ID del estudiante a eliminar: ").strip()

            if not id_delete.isdigit():
                raise ValueError("El ID debe ser un número entero.")

            id_delete_int = int(id_delete)

            # 1. Verificar existencia
            data = self.supabase.table("estudiantes").select("id_estudiante").eq("id_estudiante", id_delete_int).execute()

            if not data.data:
                print("\n❌ No existe un estudiante con ese ID.")
                return

            confirm = input(f"¿Seguro que deseas eliminar al estudiante con ID **{id_delete}**? (**s**/n): ").lower()

            if confirm != "s":
                print("\n❎ Operación cancelada.")
                return

            # Realizar la eliminación
            self.supabase.table("estudiantes").delete().eq("id_estudiante", id_delete_int).execute()

            print("\n🗑️ Estudiante eliminado correctamente.")

        except ValueError as ve:
            print(f"\n❌ {ve}")
        except Exception as e:
            print(f"\n🔥 Error al eliminar: {e}")

    # --- Menú Principal ---

    def menu(self):
        """
        Muestra el menú principal y maneja las opciones del usuario.
        """
        while True:
            print("""
======== SISTEMA DE REGISTRO DE ESTUDIANTES ========
1. Agregar estudiante
2. Buscar estudiante por ID
3. Listar estudiantes
4. Actualizar estudiante
5. Eliminar estudiante
6. Salir
====================================================
            """)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.agregar_estudiante()

            elif opcion == "2":
                self.buscar_por_id()

            elif opcion == "3":
                self.listar_estudiantes()

            elif opcion == "4":
                self.actualizar_estudiante()

            elif opcion == "5":
                self.eliminar_estudiante()

            elif opcion == "6":
                print("\n👋 Saliendo del sistema... ¡Hasta luego!")
                break

            else:
                print("\n❌ Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    gestor = GestorEstudiantesSupabase()
    gestor.menu()