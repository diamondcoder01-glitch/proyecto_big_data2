from datetime import date, datetime
def calcular_edad(fecha_nacimiento_str):
    """Calcula la edad de una persona a partir de su fecha de nacimiento (YYYY-MM-DD).
    """
    try:

        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
    except ValueError:
        return None #retorna none si el  formato es incorrecto
    
    hoy = date.today()

    #restar los  años
    edad = hoy.year - fecha_nacimiento.year

    #ajustar si todavia no ha cumplido años este año
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad
