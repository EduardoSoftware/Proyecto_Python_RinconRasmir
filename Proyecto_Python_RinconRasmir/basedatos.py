import json
import os

ruta = "C:\\Users\\eduvi\\OneDrive\\Escritorio\\Importante-Clases\\Clases Campuslands\\Phyton\\Proyecto_Python_RinconRasmir\\"
base_datos = ruta + "base_datos.json"
carpeta_prescripciones = ruta + "prescripciones\\"


def cargar_datos():
    if os.path.exists(base_datos):
        with open(base_datos, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            # Verificamos que sea un diccionario con la estructura nueva
            if isinstance(datos, dict) and "usuarios" in datos and "pacientes" in datos:
                return datos

    datos_iniciales = {
        "usuarios": [
            {
                "identificacion": "0000",
                "nombres": "Admin",
                "apellidos": "Administrador",
                "telefono": "555 000111",
                "email": "admin@acmeclinic.com",
                "direccion": "Cl 185 # 26 - 85",
                "clave": "123"
            }
        ],
        "pacientes": []
    }
    guardar_datos(datos_iniciales)
    return datos_iniciales


def guardar_datos(datos):
    # Aseguramos que la carpeta Proyecto2 exista antes de guardar
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    with open(base_datos, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def guardar_prescripcion_json(id_paciente, fecha_archivo, datos_prescripcion):
    # Crea la subcarpeta 'prescripciones' dentro de tu ruta exacta
    if not os.path.exists(carpeta_prescripciones):
        os.makedirs(carpeta_prescripciones)
        
    nombre_archivo = f"prescripcion_{id_paciente}_{fecha_archivo}.json"
    ruta_completa = carpeta_prescripciones + nombre_archivo
    
    with open(ruta_completa, "w", encoding="utf-8") as archivo:
        json.dump(datos_prescripcion, archivo, indent=4, ensure_ascii=False)
        
    return ruta_completa