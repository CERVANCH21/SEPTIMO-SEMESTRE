ubica(casa,cerca).
ubica(casita,lejos).
ubica(casota,cerca).
ubica(casa_propia,cerca).
ubica(casa_abuela, cerca).
ubica(casa_vecino, cerca).

tamanio(casa,grande).
tamanio(casita,chica).
tamanio(casota,xgrande).
tamanio(casa_propia,muy_grande).
tamanio(casa_abuela, muy_grande).
tamanio(casa_vecino, chica).

costo(casa,barata).
costo(casita,barata).
costo(casota,cara).
costo(casa_propia,barata).
costo(casa_abuela, barata).
costo(casa_vecino, cara).

permite(casota).
permite(casa_propia).


buscar_casa(Casa):-
    ubica(Casa,cerca),costo(Casa,barata).


buscar_casa(Casa):-
    ubica(Casa, lejos), costo(Casa, cara), tamanio(Casa, chica), permite(Casa).










































/*
buscar_casa(Casa):-
    ubica(Casa,cerca),tamanio(Casa,xgrande),
    costo(Casa,cara), permite(Casa,si).
buscar_casa(Casa):-
    ubica(Casa,cerca),tamanio(Casa,muy_grande),
    costo(Casa,barata),permite(Casa,si).
*/
