gusta(maria,coches).
gusta(pepe,coches).
gusta(jose,motos).

rico(pepe,si).
rico(maria,si).
rico(jose,si).

%Regla1
amigo_de_juan(Persona) :-
    gusta(Persona,coches),
    rico(Persona,si).
%regla2
mismo_gusto(Person) :-
    gusta(Person,coches),
    rico(Person,si).
%Regla3
le_gusta_a_juan_o_maria(Gusto) :-
    gusta(juan, Gusto);
    gusta(maria, Gusto).
