import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Patrón de la expresión regular:
# ^         -> inicio de la cadena
# [A-Z]+    -> una o más letras mayúsculas (el '+' se aplica al grupo [A-Z])
# [a-zA-Zá-ú1-5_@]* -> cero o más caracteres permitidos
# $         -> final de la cadena
regex_pattern = r"^[A-Z][a-zA-Zá-ú1-5_@]*$" 

def start_progress():
    """Inicia la barra de progreso y deshabilita el botón de validación."""
    btn_validar.config(state='disabled')  # Deshabilita el botón para evitar múltiples clics
    progress_bar['value'] = 0             # Reinicia la barra de progreso
    progress_bar.grid(row=3, column=0, columnspan=2, pady=10)
    update_progress(0)                    # Comienza a actualizar la barra

def update_progress(value):
    """Actualiza la barra de progreso cada 40 ms hasta 4 segundos (100 pasos)."""
    if value <= 100:
        progress_bar['value'] = value
        # Llama a update_progress cada 40 ms incrementando el valor en 1.
        root.after(30, update_progress, value + 1)
    else:
        # Cuando termina la barra de progreso, se valida la palabra.
        validate_word()
        btn_validar.config(state='normal')   # Rehabilita el botón
        progress_bar.grid_forget()             # Oculta la barra de progreso

def validate_word():
    """Valida la cadena ingresada según la expresión regular."""
    word = entry.get()
    if re.fullmatch(regex_pattern, word):
        messagebox.showinfo("Resultado", "La palabra es válida.")
    else:
        messagebox.showerror("Resultado", "La palabra no es válida.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Validador de Expresión Regular")
root.geometry("400x200")

# Etiqueta para indicar al usuario
label = tk.Label(root, text="Ingrese la palabra:")
label.grid(row=0, column=0, columnspan=2, pady=10)

# Campo de entrada para la palabra
entry = tk.Entry(root, width=40)
entry.grid(row=1, column=0, columnspan=2, pady=5)

# Botón para iniciar la validación y la barra de progreso
btn_validar = tk.Button(root, text="Validar", command=start_progress)
btn_validar.grid(row=2, column=0, columnspan=2, pady=10)

# Creación de la barra de progreso (inicialmente oculta)
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
# No la mostramos aún, se colocará en el grid al iniciar la validación.

# Inicia el loop de la interfaz
root.mainloop()
