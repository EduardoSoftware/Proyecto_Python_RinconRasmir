import json
from datetime import datetime
from basedatos import cargar_datos, guardar_datos, guardar_prescripcion_json

from basedatos import (cargar_datos, guardar_datos, guardar_prescripcion_json, cargar_diagnosticos_para_reporte, guardar_reporte_anual)

def reporte_anual_diagnosticos():
    print("\n==== REPORTE ANUAL DE DIAGNÓSTICOS ====")
    diagnosticos = cargar_diagnosticos_para_reporte()

    if len(diagnosticos) == 0:
        print("No hay diagnósticos registrados para generar el reporte.")
        return

    agrupados_por_anio = {}
    invalidos = 0

    for diag in diagnosticos:
        fecha = str(diag.get("fecha", "")).strip()

        if len(fecha) >= 10 and fecha[:4].isdigit() and fecha[4] == "-" and fecha[7] == "-":
            anio = fecha[:4]
            if anio not in agrupados_por_anio:
                agrupados_por_anio[anio] = []
            agrupados_por_anio[anio].append(diag)
        else:
            invalidos += 1

    if invalidos > 0:
        print(f"Aviso: Se ignoraron {invalidos} diagnóstico(s) por tener fecha inválida o vacía.")

    resultado_final = {
        "años": {}
    }

    for anio in sorted(agrupados_por_anio.keys()):
        lista_anio = agrupados_por_anio[anio]
        total_diagnosticos = len(lista_anio)

        medicos_unicos = []
        pacientes_unicos = []
        suma_sintomas = 0
        suma_medicamentos = 0
        conteo_enfermedades = {}

        primer_diag = lista_anio[0]
        ultimo_diag = lista_anio[0]

        for d in lista_anio:
            medico = d.get("medico", "Desconocido")
            if medico not in medicos_unicos:
                medicos_unicos.append(medico)

            paciente = d.get("id_paciente", d.get("paciente", "Desconocido"))
            if paciente not in pacientes_unicos:
                pacientes_unicos.append(paciente)
            # --- sintomas ---
            sintomas = d.get("sintomas", "")
            if isinstance(sintomas, list):
                suma_sintomas += len(sintomas)
            elif isinstance(sintomas, str) and sintomas.strip() != "":
                lista_s = [s for s in sintomas.split(",") if s.strip() != ""]
                suma_sintomas += len(lista_s)

            # --- Conteo de medicamentos ---
            medicamentos = d.get("prescripcion", d.get("medicamentos", []))
            if isinstance(medicamentos, list):
                suma_medicamentos += len(medicamentos)

            # --- Frecuencia de cada diagnóstico ---
            enfermedad = d.get("diagnostico", "Sin especificar").strip()
            if enfermedad not in conteo_enfermedades:
                conteo_enfermedades[enfermedad] = 1
            else:
                conteo_enfermedades[enfermedad] += 1

            # --- Comparar fechas para hallar el primero y el último del año ---
            if d["fecha"] < primer_diag["fecha"]:
                primer_diag = d
            if d["fecha"] > ultimo_diag["fecha"]:
                ultimo_diag = d

        # Encontrar el diagnóstico más común del año
        diagnostico_mas_comun = ""
        mayor_frecuencia = 0
        for enfermedad, cantidad in conteo_enfermedades.items():
            if cantidad > mayor_frecuencia:
                mayor_frecuencia = cantidad
                diagnostico_mas_comun = enfermedad

        # Calcular promedios redondeados a 2 decimales
        promedio_sintomas = round(suma_sintomas / total_diagnosticos, 2)
        promedio_medicamentos = round(suma_medicamentos / total_diagnosticos, 2)

        # Guardamos el resumen de este año con las llaves exactas pedidas
        resultado_final["años"][anio] = {
            "total_diagnosticos": total_diagnosticos,
            "medicos_participantes": len(medicos_unicos),
            "pacientes_atendidos": len(pacientes_unicos),
            "promedio_sintomas": promedio_sintomas,
            "promedio_medicamentos": promedio_medicamentos,
            "diagnostico_mas_comun": diagnostico_mas_comun,
            "primer_diagnostico": f"{primer_diag['fecha']} - {primer_diag['diagnostico']}",
            "ultimo_diagnostico": f"{ultimo_diag['fecha']} - {ultimo_diag['diagnostico']}"
        }

    guardar_reporte_anual(resultado_final)
    print("\n==================================================")
    print("      REPORTE ANUAL DE DIAGNÓSTICOS - ACME")
    print("==================================================")

    for anio, datos_anio in resultado_final["años"].items():
        print("\n>>> AÑO:", anio)
        print("--------------------------------------------------")
        print("Total de diagnósticos     :", datos_anio["total_diagnosticos"])
        print("Médicos participantes     :", datos_anio["medicos_participantes"])
        print("Pacientes atendidos       :", datos_anio["pacientes_atendidos"])
        print("Promedio de síntomas      :", datos_anio["promedio_sintomas"])
        print("Promedio de medicamentos  :", datos_anio["promedio_medicamentos"])
        print("Diagnóstico más común     :", datos_anio["diagnostico_mas_comun"])
        print("Primer diagnóstico        :", datos_anio["primer_diagnostico"])
        print("Último diagnóstico        :", datos_anio["ultimo_diagnostico"])
        print("--------------------------------------------------")

    print("\nArchivo 'reporte_anual_diagnosticos.json' guardado correctamente.")
    input("Presione ENTER para volver al menú...")


def login():
    print("==== INICIO SESION - CLINICA ACME ====\n")
    while True:
        datos = cargar_datos()
        usuarios = datos["usuarios"]
        
        email_ingresado = input("Ingresa tu usuario (e-mail): ")
        clave_ingresada = input("Ingresa tu clave: ")

        for usuario in usuarios:
            if usuario["email"] == email_ingresado and usuario["clave"] == clave_ingresada:
                print(f"\nBienvenido {usuario['nombres']} {usuario['apellidos']}.")
                return usuario

        print("\nError, usuario o clave invalido..")
        input("Presione ENTER para reintentar..\n")


def registro_usuarios():
    print("\n==== REGISTRO DE USUARIOS ====")
    datos = cargar_datos()
    usuarios = datos["usuarios"]

    identificacion = input("Ingrese número de identificación: ")
    email = input("Ingrese e-mail corporativo (será su usuario): ")

    # Validamos que no exista ya ese usuario
    for usuario in usuarios:
        if usuario["identificacion"] == identificacion:
            print("\nError: Ya existe un usuario con esa identificación.")
            return
        if usuario["email"] == email:
            print("\nError: Ya existe un usuario con ese e-mail.")
            return

    nombres = input("Ingrese nombres: ")
    apellidos = input("Ingrese apellidos: ")
    telefono = input("Ingrese número de teléfono: ")
    direccion = input("Ingrese dirección: ")
    clave = input("Asigne una contraseña: ")

    nuevo_usuario = {
        "identificacion": identificacion,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "clave": clave
    }

    usuarios.append(nuevo_usuario)
    guardar_datos(datos)
    print(f"\nUsuario {nombres} {apellidos}, registrado y guardado exitosamente.")


def registro_pacientes():
    print("\n==== REGISTRO DE PACIENTES ====")
    datos = cargar_datos()
    pacientes = datos["pacientes"]

    identificacion = input("Ingrese número de identificación: ")

    for paciente in pacientes:
        if paciente["identificacion"] == identificacion:
            print("\nError: Este paciente ya se encuentra registrado.")
            return

    nombres = input("Ingrese nombres: ")
    apellidos = input("Ingrese apellidos: ")
    telefono = input("Ingrese número de teléfono: ")
    email = input("Ingrese e-mail: ")
    direccion = input("Ingrese dirección: ")
    genero = input("Ingrese género: ")
    estado_civil = input("Ingrese estado civil: ")

    nuevo_paciente = {
        "identificacion": identificacion,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "email": email,
        "direccion": direccion,
        "genero": genero,
        "estado_civil": estado_civil,
        "historial": []
    }

    pacientes.append(nuevo_paciente)
    guardar_datos(datos)
    print(f"\nPaciente {nombres} {apellidos}, registrado exitosamente.")


def diagnosticar_paciente(medico_activo):
    print("\n==== DIAGNOSTICAR PACIENTE ====")
    datos = cargar_datos()
    pacientes = datos["pacientes"]

    identificacion = input("Ingrese número de identificación del paciente: ")

    for paciente in pacientes:
        if paciente["identificacion"] == identificacion:
            print(f"\nPaciente encontrado: {paciente['nombres']} {paciente['apellidos']}")
            
            sintomas = input("Ingrese los síntomas que presenta el paciente: ")
            diagnostico = input("Ingrese el diagnóstico de la enfermedad: ")

            print("\n--- PRESCRIPCIÓN MÉDICA ---")
            prescripcion = []
            while True:
                medicamento = input("Medicamento: ")
                cantidad = input("Cantidad: ")
                dosis = input("Dosis (cuánto debe tomar diariamente): ")
                tiempo = input("Tiempo de aplicación (días de tratamiento): ")

                item_medicamento = {
                    "medicamento": medicamento,
                    "cantidad": cantidad,
                    "dosis": dosis,
                    "tiempo_aplicacion": tiempo
                }
                prescripcion.append(item_medicamento)

                continuar = input("\n¿Desea agregar otro medicamento? (s/n): ").lower()
                if continuar != "s":
                    break

            ahora = datetime.now()
            fecha_consulta = ahora.strftime("%Y-%m-%d %H:%M:%S")
            fecha_archivo = ahora.strftime("%Y%m%d_%H%M%S")
            nombre_medico = f"{medico_activo['nombres']} {medico_activo['apellidos']}"

            # Guardamos en la historia clínica del paciente
            nueva_consulta = {
                "fecha": fecha_consulta,
                "medico": nombre_medico,
                "sintomas": sintomas,
                "diagnostico": diagnostico,
                "prescripcion": prescripcion
            }
            paciente["historial"].append(nueva_consulta)
            guardar_datos(datos)

            # Generamos el JSON individual de la prescripción médica
            datos_prescripcion = {
                "fecha": fecha_consulta,
                "paciente": {
                    "identificacion": paciente["identificacion"],
                    "nombres": paciente["nombres"],
                    "apellidos": paciente["apellidos"]
                },
                "medico": {
                    "identificacion": medico_activo["identificacion"],
                    "nombres": medico_activo["nombres"],
                    "apellidos": medico_activo["apellidos"]
                },
                "diagnostico": diagnostico,
                "prescripcion_medica": prescripcion
            }
            ruta_json = guardar_prescripcion_json(paciente["identificacion"], fecha_archivo, datos_prescripcion)

            print("\nDiagnóstico registrado en la Historia Clínica.")
            print(f"Archivo de prescripción generado en: {ruta_json}")
            return

    print("\nError: Paciente no encontrado. Debe registrarlo previamente.")


def historia_clinica():
    print("\n==== HISTORIA CLÍNICA ====")
    datos = cargar_datos()
    pacientes = datos["pacientes"]

    identificacion = input("Ingrese número de identificación del paciente: ")

    for paciente in pacientes:
        if paciente["identificacion"] == identificacion:
            print("\n==========================================")
            print("        HISTORIA CLÍNICA - ACME")
            print("==========================================")
            print(f"Identificación : {paciente['identificacion']}")
            print(f"Nombres        : {paciente['nombres']} {paciente['apellidos']}")
            print(f"Teléfono       : {paciente['telefono']}")
            print(f"E-mail         : {paciente['email']}")
            print(f"Dirección      : {paciente['direccion']}")
            print(f"Género         : {paciente['genero']}")
            print(f"Estado Civil   : {paciente['estado_civil']}")
            print("==========================================")

            historial = paciente["historial"]
            if len(historial) == 0:
                print("El paciente no tiene consultas registradas.")
            else:
                contador = 1
                for consulta in historial:
                    print(f"\n--- Consulta #{contador} ---")
                    print(f"Fecha       : {consulta['fecha']}")
                    print(f"Médico      : {consulta['medico']}")
                    print(f"Síntomas    : {consulta['sintomas']}")
                    print(f"Diagnóstico : {consulta['diagnostico']}")
                    print("Medicamentos prescritos:")
                    for med in consulta["prescripcion"]:
                        print(f"  - {med['medicamento']} | Cant: {med['cantidad']} | Dosis: {med['dosis']} | Días: {med['tiempo_aplicacion']}")
                    contador += 1
            print("==========================================")
            return

    print("\nError: No existe un paciente registrado con esa identificación.")


# ----------------- MENU -----------------

def menu():
    print("""
****MENU ACME****
1. Registrar usuario
2. Registrar paciente
3. Diagnostico paciente
4. Historias clinicas
5. Reporte anual diagnosticos
6. Salir
-------------------
""")


def leerOpcion():
    opcion = input(">>> Opcion?: ")
    while opcion < "1" or opcion > "6":
        print("Opcion invalida.")
        input("Presione ENTER para reintentar. ")
        print("\n\n")
        menu()
        opcion = input(">>> Opcion?: ")

    return int(opcion)


# ----------------- EJECUCIÓN PRINCIPAL -----------------

if __name__ == "__main__":
    usuario_activo = login()
    if usuario_activo:
        while True:
            menu()
            opcion = leerOpcion()
            match opcion:
                case 1:
                    registro_usuarios()
                case 2:
                    registro_pacientes()
                case 3:
                    diagnosticar_paciente(usuario_activo)
                case 4:
                    historia_clinica()
                case 5:
                    reporte_anual_diagnosticos()
                case 6:
                    print("Gracias por usar nuestros servicios.")
                    break

        input("Presiona ENTER para continuar.")