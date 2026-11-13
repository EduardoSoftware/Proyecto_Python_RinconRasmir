# Proyecto_Python_RinconRasmir
Gestor de Diagnóstico Clínico – ACME Clinic

Aplicación de consola desarrollada en Python para sistematizar y agilizar el proceso de atención, diagnóstico médico y control de historias clínicas en la Clínica ACME, reemplazando el manejo manual de registros.

Este proyecto fue desarrollado como práctica del primer módulo de programación en Python, aplicando lógica estructurada, modularización de archivos, manejo de diccionarios/listas y persistencia de datos mediante archivos JSON.

## Funcionalidades principales

El sistema cuenta con un acceso controlado y un menú interactivo con las siguientes opciones:

1. **Inicio de Sesión (Login):** Validación de credenciales mediante correo corporativo y contraseña antes de acceder al sistema. Incluye un usuario administrador por defecto.
2. **Registro de Usuarios (Operarios):** Permite crear cuentas para médicos y personal administrativo, validando que no se repitan números de identificación ni correos electrónicos.
3. **Registro de Pacientes:** Captura los datos personales y de contacto de los pacientes que ingresan a la clínica.
4. **Diagnóstico Médico y Prescripción:** Permite al médico activo registrar los síntomas y el diagnóstico de un paciente previamente registrado, además de formular uno o varios medicamentos (con cantidad, dosis y días de tratamiento). Al finalizar, genera automáticamente un archivo `.json` individual con la fórmula médica.
5. **Consulta de Historias Clínicas:** Busca a un paciente por su número de identificación y muestra en pantalla sus datos personales junto con todo el historial de consultas, médicos tratantes y medicamentos recetados.

## Estructura del proyecto

Proyecto_Python_RinconRasmir
├── principal.py        # Archivo principal con el login, menú y flujo del programa
├── basedatos.py        # Módulo encargado de leer, crear y guardar los archivos JSON
├── base_datos.json     # Archivo generado automáticamente con usuarios, pacientes e historiales
└── prescripciones/     # Carpeta generada automáticamente con las fórmulas médicas individuales en JSON
