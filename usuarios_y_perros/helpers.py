#funciones auxiliares

from datetime import date

def es_menor_18(birth):
    now = date.today()
    return (
        now.year - birth.year < 18
        or now.year - birth.year == 18 and (
            now.month < birth.month 
            or now.month == birth.month and now.day <= birth.day
        )
    )

def generarContraseña():
    return 1234