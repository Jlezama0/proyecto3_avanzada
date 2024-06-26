# proyecto3_avanzada

# Proyecto3_Avanzada

## Proyecto 3 Programación Avanzada

### Miembros del Equipo:

- Juan Pablo Lezama Cantor
- Tatiana Jimenez
- Alejandro Diaz Sarmiento

---

### Descripción del Proyecto:

Este proyecto consiste en una API desarrollada en FastAPI para la gestión de empleados y pagos. La API está diseñada para interactuar con una base de datos MySQL. A continuación, se detallan aspectos importantes para probar y entender el funcionamiento del proyecto.

---

### Configuración de la Base de Datos:

Es necesario crear la base de datos y realizar las inserciones correspondientes para poder utilizar la API correctamente. Los pasos a seguir son los siguientes:

1. Conectar con la base de datos: La conexión con la base de datos se realiza a través del archivo `db_conection.py`.
2. Creación de Tablas: Al ejecutar el archivo `main.py` en el servidor, las tablas se crean automáticamente.
3. Inserciones de Datos: Para las inserciones de datos, se proporciona un archivo `inserts.sql` que contiene las inserciones necesarias para la tabla `departamentos`. Estas inserciones deben realizarse directamente en MySQL.

---

### Creación de Empleados y Pruebas:

Para la tabla de empleados, las inserciones no pueden realizarse directamente debido a que el sistema cifra la contraseña al hacer una petición POST en el método `"/crearEmpleado/"`. Para probar la API y realizar inserciones de prueba, se proporciona un método adicional `"/crear/"` que permite realizar peticiones POST a la base de datos sin las restricciones de seguridad de `"/crearEmpleado/"`.

Los datos de prueba se encuentran en el archivo `datos.json`. Se recomienda utilizar estos datos para probar las funcionalidades de la API.

---

### Generación de Desprendibles de Pago:

El archivo `crear_pdf.py` está diseñado para ejecutarse automáticamente el día 30 de cada mes a las 6 de la tarde. Este archivo verifica si se ha realizado el pago a los empleados y genera el desprendible de pago correspondiente. Posteriormente, modifica la base de datos para indicar que se ha realizado el pago a los empleados.

Además, el día 15 de cada mes, el sistema restablece el estado de pago para que se pueda realizar el pago de manera mensual de forma adecuada.

---
