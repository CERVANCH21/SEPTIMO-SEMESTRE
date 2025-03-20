import tkinter as tk
from tkinter import ttk
import re
from categoria import categoria

def analizar_codigo():
    # Limpiar las tablas anteriores
    for item in tabla_simbolos.get_children():
        tabla_simbolos.delete(item)
    for item in tabla_errores.get_children():
        tabla_errores.delete(item)

    codigo = entrada_text.get("1.0", tk.END).strip()
    lineas = codigo.split('\n')
    separadores = [" ", ",", "=", ";", "+", "*", "-", "/"]
    tipos = ["entier", "reel", "chaine"]

    # Expresiones regulares definidas
    cadena = re.compile(r'^"([^"]*)"$')
    entero = re.compile(r"^[0-9]+$")
    flotante = re.compile(r"^[0-9]+\.[0-9]+$")
    identificador = re.compile(r"^[A-Z]+[a-zA-Zá-úÁ-Ú1-5_@]*$")

    lista_lexemas_global = []
    lista_lexemas_tipos = []
    
    # Diccionario para almacenar las variables declaradas:
    # clave: nombre de la variable, valor: tipo declarado
    tabla_variables = {}

    # Función para verificar la asignación según el tipo de variable y los tokens de la expresión.
    def verificar_asignacion(var_type, tokens):
        operadores_permitidos = {
            "chaine": ["+"],
            "entier": ["+", "-", "*"],
            "reel": ["+", "-", "*", "/"]
        }
        for token in tokens:
            if token in ["+", "-", "*", "/"]:
                if token not in operadores_permitidos[var_type]:
                    return "Error aritmético"
            else:
                if var_type == "chaine":
                    if not cadena.match(token):
                        return "Error de asignación"
                elif var_type == "entier":
                    if not entero.match(token):
                        return "Error de asignación"
                elif var_type == "reel":
                    if not flotante.match(token):
                        return "Error de asignación"
        return None

    # Procesamos cada línea, utilizando enumerate para contar el renglón.
    for i, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue

        # Separamos la línea en tokens (quitando el ';')
        tokens_linea = linea.replace(";", "").split()

        # Si la línea es de declaración (empieza con un tipo)
        if tokens_linea[0] in tipos:
            var_type = tokens_linea[0]
            var_name = tokens_linea[1]
            tabla_variables[var_name] = var_type
            # Si en la misma línea se realiza asignación
            if "=" in tokens_linea:
                pos_igual = tokens_linea.index("=")
                expression_tokens = tokens_linea[pos_igual+1:]
                error = verificar_asignacion(var_type, expression_tokens)
                if error:
                    tabla_errores.insert("", "end", values=(i, var_name, error, "Asignación"))
        # Línea de asignación sin declaración (por ejemplo: P1 = 24;)
        elif "=" in tokens_linea:
            pos_igual = tokens_linea.index("=")
            var_name = tokens_linea[pos_igual - 1]
            expression_tokens = tokens_linea[pos_igual+1:]
            var_type = tabla_variables.get(var_name, None)
            if var_type is None:
                tabla_errores.insert("", "end", values=(i, var_name, "Variable no declarada", "Asignación"))
            else:
                error = verificar_asignacion(var_type, expression_tokens)
                if error:
                    tabla_errores.insert("", "end", values=(i, var_name, error, "Asignación"))

        # Proceso de tokenización para la tabla de símbolos (manteniendo tu lógica original)
        tipo_actual = ""
        for tipo in tipos:
            if tipo in linea:
                tipo_actual = tipo

        lexema = ""
        for caracter in linea:
            if caracter not in separadores:
                lexema += caracter  
            else:
                if lexema and lexema not in lista_lexemas_global:
                    lista_lexemas_global.append(lexema)
                if caracter in separadores[1:] and caracter not in lista_lexemas_global:
                    lista_lexemas_global.append(caracter)
                lexema = ""
        if lexema:
            lista_lexemas_global.append(lexema)
            lexema = ""

        inicio = len(lista_lexemas_tipos)
        for lex in lista_lexemas_global[inicio:]:
            if cadena.match(lex):
                lista_lexemas_tipos.append("chaine")
            elif entero.match(lex):
                lista_lexemas_tipos.append("entier")
            elif flotante.match(lex):
                lista_lexemas_tipos.append("reel")
            elif identificador.match(lex):
                lista_lexemas_tipos.append(tipo_actual if tipo_actual else "indefinido")
            else:
                lista_lexemas_tipos.append(" ")

        if len(lista_lexemas_global) != len(lista_lexemas_tipos):
            print(f"Error: Desbalance - Lexemas: {len(lista_lexemas_global)}, Tipos: {len(lista_lexemas_tipos)}")           

    # Llenar la tabla de símbolos con los lexemas y sus tipos
    for lex, tipo in zip(lista_lexemas_global, lista_lexemas_tipos):
        tabla_simbolos.insert("", "end", values=(lex, tipo))


# INTERFAZ GRÁFICA
ventana = tk.Tk()
ventana.title("Analizador de Código")
ventana.geometry("900x600")
ventana.configure(bg="#2E2E2E")

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

tabla_errores = ttk.Treeview(frame_errores, columns=("Renglón", "Lexema", "Descripción", "Token error"), show="headings")
tabla_errores.heading("Renglón", text="Renglón")
tabla_errores.heading("Lexema", text="Lexema")
tabla_errores.heading("Descripción", text="Descripción")
tabla_errores.heading("Token error", text="Token error")
tabla_errores.pack(expand=True, fill="both")

ventana.mainloop()
