% Base de hechos: Lista de regalos con sus cualidades
regalo(flores, [romantico, economico, fragil]).
regalo(chocolate, [dulce, economico, perecedero]).
regalo(libro, [educativo, duradero, economico]).
regalo(reloj, [caro, duradero, elegante]).

% Cualidades que nos deciden a comprar un regalo
cualidad_deseada(romantico).
cualidad_deseada(economico).
cualidad_deseada(duradero).

% Regla general para ir de compras: Si al menos dos cualidades deseadas están presentes, comprar el regalo.
comprar_regalo(Regalo) :-
    regalo(Regalo, Cualidades),
    findall(Cualidad, (member(Cualidad, Cualidades), cualidad_deseada(Cualidad)), CualidadesDeseadas),
    length(CualidadesDeseadas, NumCualidadesDeseadas),
    NumCualidadesDeseadas >= 2.

% Regla de excepción: No comprar un regalo si es frágil.
excepcion(Regalo) :-
    regalo(Regalo, Cualidades),
    member(fragil, Cualidades).

% Regla final que considera la excepción
decidir_comprar(Regalo) :-
    comprar_regalo(Regalo),
    \+ excepcion(Regalo).

% Consulta para encontrar todos los regalos que se pueden comprar
posibles_compras(Regalos) :-
    findall(Regalo, decidir_comprar(Regalo), Regalos).
