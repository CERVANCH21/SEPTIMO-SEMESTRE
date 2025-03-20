import tkinter as tk
from tkinter import ttk
import re
from categoria import categoria


def analizar_codigo():

    for item in tabla_simbolos.get_children():
        tabla_simbolos.delete(item)

    codigo = entrada_text.get("1.0", tk.END).strip()
    lineas = codigo.split('\n')
    separadores = [" ",",","=",";","+","*","-","/"]
    tipos = ["entier", "reel", "chaine"]
    sep_admitidos = separadores[1:]

    cadena = re.compile(r'^"([^"]*)"$')
    entero = re.compile(r"^[0-9]+$")
    flotante = re.compile(r"^[0-9]+\.[0-9]+$")
    identificador = re.compile(r"^[A-Z][a-zA-Zá-úÁ-Ú1-5_@]*$")

    lexema = ""
    lista_lexemas_global = []
    lista_lexemas_tipos = []

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        #print(linea)
        #print(categoria(linea))

        tipo_actual = ""

        for tipo in tipos:
            if tipo in linea:
                tipo_actual = tipo

        #print(tipo_actual + "\n")

        for caracter in linea:
            if caracter not in separadores:
                lexema += caracter  
            else:
                # Agregar el lexema actual si no está vacío
                if lexema and lexema not in lista_lexemas_global:
                    lista_lexemas_global.append(lexema)
                
                # Agregar el separador si está en sep_admitidos
                if caracter in sep_admitidos and caracter not in lista_lexemas_global:
                    lista_lexemas_global.append(caracter)

                lexema = ""
        
        # Agregar el último lexema de la línea si no está vacío
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
        
        print(lista_lexemas_global)
        print(lista_lexemas_tipos)

        if len(lista_lexemas_global) != len(lista_lexemas_tipos):
            print(f"Error: Desbalance - Lexemas: {len(lista_lexemas_global)}, Tipos: {len(lista_lexemas_tipos)}")           

        # Llenar la tabla de símbolos
    for lex, tipo in zip(lista_lexemas_global, lista_lexemas_tipos):
        tabla_simbolos.insert("", "end", values=(lex, tipo))




        


# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador de Código")
ventana.geometry("900x600")
ventana.configure(bg="#2E2E2E")

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