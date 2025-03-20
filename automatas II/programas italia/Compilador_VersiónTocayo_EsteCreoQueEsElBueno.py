import re
import tkinter as tk
from tkinter import ttk

# Expresión regular para variables (permite @ y ' después del primer carácter)
VAR_PATTERN = re.compile(r"^[A-Z]+[a-zA-Zá-úÁ-Ú1-5_@]*$")

data_types = {}  # Diccionario de tipos de datos
errors = []  # Lista de errores


# Función para procesar la entrada
def process_input():
    global data_types, errors
    data_types.clear()
    errors.clear()

    input_text = entrada_text.get("1.0", tk.END).strip()

    lines = input_text.split("\n")
    lexemes = []
    error_count = 1

    # Conjunto para evitar duplicados
    unique_lexemes = set()

    # Expresión regular para operadores, comas, puntos y comas, y otros separadores
    SEPARATOR_PATTERN = re.compile(r"[\+\-\*/%,=;:]")

    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        # Asignación de tipo de datos (entier, reel, chaine)
        if line.startswith(("entier", "reel", "chaine")):
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                errors.append([f"ER{error_count}", "", line_num, "Declaración de tipo incompleta"])
                error_count += 1
                continue

            data_type = parts[0]
            if data_type not in unique_lexemes:  # Evitar duplicados
                lexemes.append([data_type, ""])
                unique_lexemes.add(data_type)

            # Dividir la línea en tokens (variables y separadores)
            tokens = re.findall(r"[\+\-\*/%,=;:]|[A-Za-z][a-zA-Zá-úÁ-Ú1-5_@]*|[\"'][^\"']*[\"']", parts[1])
            for token in tokens:
                if SEPARATOR_PATTERN.match(token):  # Es un separador (coma, punto y coma, etc.)
                    if token not in unique_lexemes:
                        lexemes.append([token, ""])  # Agregar separador con valor vacío
                        unique_lexemes.add(token)
                else:  # Es una variable
                    if VAR_PATTERN.match(token):  # Validar con la expresión regular
                        data_types[token] = data_type  # Asignar el tipo de dato
                        if token not in unique_lexemes:  # Evitar duplicados
                            lexemes.append([token, data_type])
                            unique_lexemes.add(token)
                    else:
                        # Agregar la variable inválida a la tabla de símbolos con tipo vacío
                        if token not in unique_lexemes:
                            lexemes.append([token, ""])
                            unique_lexemes.add(token)
                        # Registrar el error en la tabla de errores
                        errors.append([f"ER{error_count}", token, line_num, "Error de sintaxis"])
                        error_count += 1

        # Procesamiento de asignaciones (a = valor) y operaciones
        elif "=" in line:
            parts = line.split("=")
            if len(parts) != 2:
                errors.append([f"ER{error_count}", "", line_num, "Asignación inválida"])
                error_count += 1
                continue

            var = parts[0].strip()
            expression = parts[1].strip()

            # Agregar la variable a la tabla de símbolos, incluso si no está declarada
            if var not in unique_lexemes:
                lexemes.append([var, data_types.get(var, "")])  # Agregar con tipo vacío si no está declarada
                unique_lexemes.add(var)

            # Validación de tipo de variable (lado izquierdo)
            if var not in data_types:
                errors.append([f"ER{error_count}", var, line_num, "Variable no definida"])
                error_count += 1

            # Agregar el símbolo "=" como lexema
            if "=" not in unique_lexemes:
                lexemes.append(["=", ""])
                unique_lexemes.add("=")

            # Procesar la expresión (validar operadores y operandos)
            tokens = re.findall(r"[\+\-\*/%,=;:]|\d+\.\d+|\d+|\w+|[\"'][^\"']*[\"']", expression)
            error_tokens = []
            undefined_vars = []  # Para agrupar errores en la misma línea
            for i, token in enumerate(tokens):
                if SEPARATOR_PATTERN.match(token):  # Es un operador, coma, punto y coma, etc.
                    if token not in unique_lexemes:
                        lexemes.append([token, ""])  # Agregar separador con valor vacío
                        unique_lexemes.add(token)

                    # Validar operadores no permitidos
                    if var in data_types:
                        expected_type = data_types[var]
                        if expected_type == "chaine" and token not in ("+", "="):
                            error_tokens.append(token)  # Operador no permitido en cadenas
                        elif expected_type == "entier" and token == "/":
                            error_tokens.append(token)  # Operador no permitido en enteros
                else:  # Es un valor o variable
                    if token in data_types:  # Es una variable definida
                        token_type = data_types[token]
                    else:  # Es un valor
                        if token.isdigit():
                            token_type = "entier"
                        elif re.match(r"^\d+\.\d+$", token):
                            token_type = "reel"
                        elif token.startswith('"') and token.endswith('"'):
                            token_type = "chaine"
                        else:
                            token_type = None  # Variable no definida

                    # Validar compatibilidad de tipos
                    if var in data_types:
                        expected_type = data_types[var]
                        if token_type is not None:
                            if expected_type == "entier" and token_type != "entier":
                                error_tokens.append(token)
                            elif expected_type == "reel" and token_type not in ("entier", "reel"):
                                error_tokens.append(token)
                            elif expected_type == "chaine" and token_type != "chaine":
                                error_tokens.append(token)
                        else:  # Es una variable no definida
                            undefined_vars.append(token)

                    if token not in unique_lexemes:
                        lexemes.append([token, token_type if token_type else ""])
                        unique_lexemes.add(token)

            # Agrupar errores en la misma línea
            if error_tokens:
                error_tokens = [token for token in error_tokens if token.strip() and token != ";"]

            if error_tokens:
                errors.append([f"ER{error_count}", ", ".join(error_tokens), line_num,
                               f"Incompatibilidad de tipos({data_types.get(var, 'desconocido')})"])
                error_count += 1

            if undefined_vars:
                errors.append([f"ER{error_count}", ", ".join(undefined_vars), line_num, "Variable no definida"])
                error_count += 1

    update_tables(lexemes, errors)


# Función para actualizar las tablas
def update_tables(lexemes, errors):
    # Limpiar la tabla de lexemas
    for i in tabla_simbolos.get_children():
        tabla_simbolos.delete(i)
    # Agregar lexemas a la tabla
    for lexeme, dtype in lexemes:
        tabla_simbolos.insert("", "end", values=(lexeme, dtype))

    # Limpiar la tabla de errores
    for i in tabla_errores.get_children():
        tabla_errores.delete(i)
    # Agregar errores a la tabla
    for error in errors:
        tabla_errores.insert("", "end", values=error)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Analizador de codigo")
ventana.geometry("900x600")

# Entrada de código
frame_entrada = tk.Frame(ventana)
frame_entrada.place(x=10, y=10, width=400, height=300)

label_entrada = tk.Label(frame_entrada, text="Código de entrada:")
label_entrada.pack(anchor='nw')

entrada_text = tk.Text(frame_entrada, wrap="word")
entrada_text.pack(expand=True, fill="both")

# Botón para analizar
boton_analizar = tk.Button(ventana, text="Analizar", command=process_input)
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

tabla_errores = ttk.Treeview(frame_errores, columns=("Token error", "Lexema", "Renglón", "Descripción"),
                             show="headings")
tabla_errores.heading("Token error", text="Token error")
tabla_errores.heading("Renglón", text="Renglón")
tabla_errores.heading("Lexema", text="Lexema")
tabla_errores.heading("Descripción", text="Descripción")
tabla_errores.pack(expand=True, fill="both")

ventana.mainloop()