% Base de Hechos
persona(maria).
persona(pepe).
persona(jose).
persona(juan).
persona(zair).

gusta(maria, coches).
gusta(pepe, coches).
gusta(jose, motos).
gusta(zair, motos).

es(pepe,rico).
es(maria,rico).
es(jose, rico).
es(zair, pobre).
es(juan, pobre).

% Base de Conocimientos
% juan es amigo de aquellos que les gustan los coches y son ricos
es_amigo(juan, Amigo):-
    gusta(Amigo, coches), es(Amigo,rico).
le_gusta_lo_mismo(Amigo1, Amigo2, Algo):-
    gusta(Amigo1, Algo), gusta(Amigo2, Algo),
    Amigo1 \= Amigo2.

% Consultas
% A) ¿Quiénes son amigos de Juan?
% ?- amigo(juan, Quien).

% B) ¿A quiénes les gusta lo mismo?
% ?- le_gusta_lo_mismo(pepe, maria, Algo).

% C) ¿Hay algo que le guste a Juan o a María?
% ?- gusta(juan, Algo).
% ?- gusta(maria, Algo).
