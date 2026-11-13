from datetime import datetime
from basedatos import cargar_datos, guardar_datos, guardar_prescripcion_json


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
                # Retornamos el usuario completo para saber qué médico está atendiendo
                return usuario

        # Si recorrió todo el 'for' y no encontró coincidencia:
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
5. Salir
-------------------
""")


def leerOpcion():
    opcion = input(">>> Opcion?: ")
    while opcion < "1" or opcion > "5":
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
                    print("Gracias por usar nuestros servicios.")
                    break

        input("Presiona ENTER para continuar.")