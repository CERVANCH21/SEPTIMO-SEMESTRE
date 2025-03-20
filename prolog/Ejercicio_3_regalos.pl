regalo(reloj).
regalo(libro).
regalo(perfume).
regalo(bicicleta).
regalo(bolso).

bueno(reloj).
bueno(libro).
bonito(perfume).
divertido(bicicleta).
practico(bolso).

quiere_comprar(ana, reloj).
quiere_comprar(ana, bicicleta).
quiere_comprar(carlos, perfume).
quiere_comprar(carlos, bolso).

%Excepci�n: algo puede ser muy caro
caro(bicicleta).
caro(bolso).

%Regla para comprar algo
puede_comprar(Persona, Regalo) :-
    regalo(Regalo),
    (bueno(Regalo) ; bonito(Regalo) ; divertido(Regalo) ; practico(Regalo)),
    quiere_comprar(Persona, Regalo),  % La persona lo quiere
    \+ muy_caro(Persona, Regalo).  % Pero no debe ser muy caro

%Regla de excepcion: si algo es caro, no se compra
muy_caro(Persona, Regalo):-
    caro(Regalo),
    quiere_comprar(Persona, Regalo).
