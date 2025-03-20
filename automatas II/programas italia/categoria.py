def categoria(linea):
    tipos = ["entier", "reel", "chaine"]
    operadores = ["+", "/", "*", "-"]

    tiene_tipo = False
    tiene_igual = "=" in linea
    tiene_operador = False

    for tipo in tipos:
        if tipo in linea:
            tiene_tipo = True
            break  # No es necesario seguir buscando si ya se encontró

    for operador in operadores:
        if operador in linea:
            tiene_operador = True
            break  # No es necesario seguir buscando si ya se encontró

    if tiene_tipo:
        if tiene_igual and tiene_operador:
            return "declaracion-operacion"
        elif tiene_igual:
            return "declaracion-asignacion"
        return "declaracion"
    elif tiene_operador:
        return "operacion"
    elif tiene_igual:
        return "asignacion"

    return "desconocido"  # Caso no contemplado



