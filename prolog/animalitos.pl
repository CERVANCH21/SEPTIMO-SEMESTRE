lagarto(iguana).
lagarto(cocodrilo).
lagarto(caiman).
lagarto(camaleon).
lagarto(dragon_de_komodo).

serpiente(vibora).
serpiente(anaconda).
serpiente(piton).
serpiente(cobra).
serpiente(boa).


tiene_pelo(conejo).
tiene_pelo(perro).
tiene_pelo(gato).
tiene_pelo(oso).
tiene_pelo(nutria).

come(conejo,zanahorias).
come(perro, hueso).
come(gato,raton).
come(oso,pescado).
come(nutria, pescado).
come(vibora, animales_pequeno).
come(anaconda, animales_pequeno).
come(dragon_de_komodo, animales_pequeno).

animal_feo(Animal, animales_pequeno):-
    come(Animal, animales_pequeno).











































/*
animal_lindo(Animal, Comida):-
    come(Animal, Comida), tiene_pelo(Animal).

*/
