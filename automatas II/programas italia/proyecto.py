import tkinter as tk
from tkinter import ttk
import re


def analizar_codigo():
    # Limpiamos las tablas antes de analizar
    for item in tabla_simbolos.get_children():
        tabla_simbolos.delete(item)
    for item in tabla_errores.get_children():
        tabla_errores.delete(item)

    codigo = entrada_text.get("1.0", tk.END).strip()
    lineas = codigo.split('\n')

    simbolos = {}
    errores = []

    patron_declaracion = re.compile(
        r'^(entier|reel|chaine)\s+([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*(?:,[A-Z][a-zA-Zá-úÁ-Ú1-5_@]*)*);?$')
    patron_asignacion = re.compile(r'^([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*)\s*=\s*([^;]+);?$')
    patron_operacion = re.compile(r'([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*)\s*([+\-*/])\s*([A-Za-z0-9_."]+)')

    for num_linea, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue

        # Detectar palabras clave (entier, reel, chaine)
        for palabra in ["entier", "reel", "chaine"]:
            if palabra in linea:
                tabla_simbolos.insert("", tk.END, values=(palabra, palabra))

        # Detectar identificadores (variables declaradas)
        match_declaracion = patron_declaracion.match(linea)
        if match_declaracion:
            tipo, lista_variables = match_declaracion.groups()
            nombres_variables = [var.strip() for var in lista_variables.split(',')]

            for nombre in nombres_variables:
                simbolos[nombre] = tipo
                tabla_simbolos.insert("", tk.END, values=(nombre, tipo))
            continue

        # Detectar asignaciones y valores
        match_asignacion = patron_asignacion.match(linea)
        if match_asignacion:
            variable, expresion = match_asignacion.groups()
            tabla_simbolos.insert("", tk.END, values=("=", "operador"))

            if variable not in simbolos:
                errores.append((num_linea, variable, "Variable indefinida"))
                continue

            tipo_variable = simbolos[variable]

            # Capturar valores numéricos, cadenas y operadores
            tokens = re.split(r'(\s+|;|,|\+|\-|\*|\/|=)', expresion)  # Separar operadores y valores
            for token in tokens:
                token = token.strip()
                if not token:
                    continue

                # Clasificar el tipo del token
                if token.isdigit():
                    tabla_simbolos.insert("", tk.END, values=(token, "entier"))
                elif re.match(r'^\d+\.\d+$', token):
                    tabla_simbolos.insert("", tk.END, values=(token, "reel"))
                elif re.match(r'^".*"$', token):
                    tabla_simbolos.insert("", tk.END, values=(token, "chaine"))
                elif token in ["+", "-", "*", "/"]:
                    tabla_simbolos.insert("", tk.END, values=(token, "operador"))
                elif token in simbolos:
                    tabla_simbolos.insert("", tk.END, values=(token, simbolos[token]))
                elif token == ";":
                    tabla_simbolos.insert("", tk.END, values=(";", "símbolo"))

            continue

        # Si la línea no es reconocida, se considera error
        errores.append((num_linea, linea, "Error de sintaxis"))

        continue

        match_declaracion = patron_declaracion.match(linea)
        if match_declaracion:
            tipo, lista_variables = match_declaracion.groups()

            # Separar los nombres de variables en una lista
            nombres_variables = [var.strip() for var in lista_variables.split(',')]

            for nombre in nombres_variables:
                nombre = nombre.strip()  # Asegurar que no haya espacios
                if nombre:  # Verificar que la variable no esté vacía
                    simbolos[nombre] = tipo  # Guardar en el diccionario de símbolos
                    tabla_simbolos.insert("", tk.END, values=(nombre, tipo))  # Insertar en la tabla

            continue

        match_asignacion = patron_asignacion.match(linea)
        if match_asignacion:
            variable, expresion = match_asignacion.groups()

            #----------------------------------------


            if variable not in simbolos:
                errores.append((num_linea, variable, "Variable indefinida"))
                continue

            tipo_variable = simbolos[variable]
            # Detectar el tipo del valor asignado
            if expresion.isdigit():
                tipo_expresion = "entier"  # Número entero
            elif re.match(r'^\d+\.\d+$', expresion):
                tipo_expresion = "reel"  # Número flotante
            elif re.match(r'^".*"$', expresion) or re.match(r"^'.*'$", expresion):
                tipo_expresion = "chaine"  # Cadena de texto
            else:
                tipo_expresion = "Desconocido"  # Caso en que no se pueda determinar el tipo

            # Comprobar si el tipo de la variable coincide con el tipo del valor asignado
            if tipo_variable != tipo_expresion and tipo_expresion != "Desconocido":
                errores.append((num_linea, linea,
                                f"Error de asignación: '{variable}' es {tipo_variable}, pero se asignó {tipo_expresion}"))
            match_operacion = patron_operacion.match(expresion)

            if match_operacion:
                var1, operador, var2 = match_operacion.groups()

                tipo1 = simbolos.get(var1,
                                     "Desconocido") if var1.isalpha() else "int" if var1.isdigit() else "float" if '.' in var1 else "string"
                tipo2 = simbolos.get(var2,
                                     "Desconocido") if var2.isalpha() else "int" if var2.isdigit() else "float" if '.' in var2 else "string"

                if tipo1 != tipo2:
                    errores.append((num_linea, expresion, "Incompatibilidad de tipos"))

            continue

        errores.append((num_linea, linea, "Error de sintaxis"))

    for err in errores:
        tabla_errores.insert("", tk.END, values=err)


# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador de Código")
ventana.geometry("900x600")

# Entrada de código
frame_entrada = tk.Frame(ventana)
frame_entrada.place(x=10, y=10, width=400, height=300)

label_entrada = tk.Label(frame_entrada, text="Código de entrada:")
label_entrada.pack(anchor='nw')

entrada_text = tk.Text(frame_entrada, wrap="word")
entrada_text.pack(expand=True, fill="both")

# Botón para analizar
boton_analizar = tk.Button(ventana, text="Analizar", command=analizar_codigo)
boton_analizar.place(x=420, y=10, width=80, height=30)

# Tabla de símbolos
frame_simbolos = tk.Frame(ventana)
frame_simbolos.place(x=510, y=10, width=350, height=250)

label_simbolos = tk.Label(frame_simbolos, text="Tabla de Símbolos")
label_simbolos.pack(anchor='nw')

tabla_simbolos = ttk.Treeview(frame_simbolos, columns=("Lexema", "Tipo"), show="headings")
tabla_simbolos.heading("Lexema", text="Lexema")
tabla_simbolos.heading("Tipo", text="Tipo")
tabla_simbolos.pack(expand=True, fill="both")

# Tabla de errores
frame_errores = tk.Frame(ventana)
frame_errores.place(x=10, y=320, width=770, height=250)

label_errores = tk.Label(frame_errores, text="Tabla de Errores")
label_errores.pack(anchor='nw')

tabla_errores = ttk.Treeview(frame_errores, columns=("Lexema", "Renglón", "Descripción"), show="headings")

tabla_errores.heading("Lexema", text="Lexema")
tabla_errores.heading("Renglón", text="Renglón")
tabla_errores.heading("Descripción", text="Descripción")
tabla_errores.pack(expand=True, fill="both")

ventana.mainloop()