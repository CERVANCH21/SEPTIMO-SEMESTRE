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
    
    variables = {}
    errores = []
    contador_errores = 1
    variables_declaradas = set()  # Conjunto para evitar variables repetidas
    simbolos_especiales = set()   # Conjunto para evitar repetir = y ;

    # Expresiones regulares para tipos de datos
    regex_entero = re.compile(r'^\d+$')
    regex_real = re.compile(r'^\d+\.\d+$')
    regex_cadena = re.compile(r'^"([^"]+)"$')
    
    
    patron_declaracion = re.compile(r'^(entier|reel|chaine)\s+([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*(?:,[A-Z][a-zA-Zá-úÁ-Ú1-5_@]*)*);?$')
    #patron_asignacion = re.compile(r'^([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*)\s*=\s*([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*);?$')
    patron_asignacion = re.compile(r'^([A-Z][a-zA-Zá-úÁ-Ú1-5_@]*)\s*=\s*([A-Za-z0-9_+\-*\/.\s"]+);?$')

    for num_linea, linea in enumerate(lineas, start=1):

        for c in linea:
            print(c)

        linea = linea.strip()
        if not linea:
            continue

        print(linea)

        # Detectar palabras clave (entier, reel, chaine)
        for tipo in ["entier", "reel", "chaine"]:
            if tipo in linea:
                # Insertar la palabra clave con la celda de Tipo vacía
                tabla_simbolos.insert("", tk.END, values=(tipo, ""))

        # Detectar declaraciones de variables
        match_declaracion = patron_declaracion.match(linea)
        if match_declaracion:
            tipo, variable = match_declaracion.groups()
            lista_variables = [var.strip() for var in variable.split(',')]

            for variable in lista_variables:
                if variable not in variables_declaradas:  # Evitar variables repetidas
                    variables[variable] = tipo
                    variables_declaradas.add(variable)
                    tabla_simbolos.insert("", tk.END, values=(variable, tipo))
                    
                print(variables_declaradas)
            continue

        # Detectar asignaciones y valores
        match_asignacion = patron_asignacion.match(linea)
        if match_asignacion:
            variable_inde, expresion = match_asignacion.groups()

            # Insertar el símbolo = con la celda de Tipo vacía (si no está ya insertado)
            if "=" not in simbolos_especiales:
                tabla_simbolos.insert("", tk.END, values=("=", ""))
                simbolos_especiales.add("=")
            if "+" in expresion:
                tabla_simbolos.insert("", tk.END, values=("+", ""))
            if ";" not in simbolos_especiales:
                tabla_simbolos.insert("", tk.END, values=(";", ""))
                simbolos_especiales.add(";")
            if variable_inde not in variables:
                errores.append((num_linea, variable_inde, "Variable indefinida",f"ER{contador_errores}"))
                contador_errores += 1
                tabla_simbolos.insert("", tk.END, values=(variable_inde, ""))
            

            tipo_variable = variables[variable_inde]
        
            # Capturar valores numéricos, cadenas y operadores
            tokens = re.split(r'(\s+|;|,|\+|\-|\*|\/|=)', expresion)
            for token in tokens:
                token = token.strip()
                if not token:
                    continue
                # Clasificar el tipo del token
                if regex_entero.match(token):
                    tipo_elem = "entier"
                elif regex_real.match(token):
                    tipo_elem = "reel"
                elif regex_cadena.match(token):
                    tipo_elem = "chaine"
                
                else:
                    if token in variables:
                        tipo_elem = variables[token]
                    else:
                        
                        continue  # Ignorar elementos no válidos
                # Verificar si el token es una variable indefinida
                if token in variables:
                    # El token es una variable definida, no hay error
                    pass
                elif regex_entero.match(token) or regex_real.match(token) or regex_cadena.match(token):
                    # El token es un número o cadena, no hay error
                    pass
                
                else:
                    # El token no es una variable definida, número, cadena ni operador
                    errores.append((num_linea, token, "Variable indefinida", f"ER{contador_errores}"))
                    contador_errores += 1
                    tabla_simbolos.insert("", tk.END, values=(token, ""))
                
                # Insertar el token en la tabla de símbolos
                if token not in variables_declaradas:
                    tabla_simbolos.insert("", tk.END, values=(token, tipo_elem))
                
                
                # Verificar incompatibilidad de tipos en asignaciones
                if tipo_variable == "chaine" and tipo_elem != "chaine":
                    errores.append((num_linea, token, f"Incompatibilidad de tipos {tipo_variable} con {tipo_elem}", f"ER{contador_errores}"))
                    contador_errores += 1
                elif tipo_variable == "entier" and tipo_elem != "entier":
                    errores.append((num_linea, token, f"Incompatibilidad de tipos {tipo_variable} con {tipo_elem}", f"ER{contador_errores}"))
                    contador_errores += 1
                elif tipo_variable == "reel" and tipo_elem != "reel":
                    errores.append((num_linea, token, f"Incompatibilidad de tipos {tipo_variable} con {tipo_elem}", f"ER{contador_errores}"))
                    contador_errores += 1
                
            continue
        errores.append((num_linea, linea, "indefinido", f"ER{contador_errores}"))
        contador_errores += 1
    
    for err in errores:
        tabla_errores.insert("", tk.END, values=err)

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador de Código")
ventana.geometry("900x600")

#Entrada de código
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

tabla_errores = ttk.Treeview(frame_errores, columns=( "Renglón","Lexema", "Descripción","Token error"), show="headings")

tabla_errores.heading("Token error", text="Token error")
tabla_errores.heading("Renglón", text="Renglón")
tabla_errores.heading("Lexema", text="Lexema")
tabla_errores.heading("Descripción", text="Descripción")
tabla_errores.pack(expand=True, fill="both")

ventana.mainloop()