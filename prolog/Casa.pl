ubica(casa,cerca).
ubica(casita,lejos).
ubica(casota,cerca).
ubica(casa_perfecta,cerca).

tamanio(casa,grande).
tamanio(casita,chica).
tamanio(casota,xgrande).
tamanio(casa_perfecta,muy_grande).

costo(casa,barata).
costo(casita,barata).
costo(casota,cara).
costo(casa_perfecta,barata).

permite(casa,no).
permite(casita,no).
permite(casota,si).
permite(casa_perfecta,si).




buscar_casa(Casa):-
    ubica(Casa,cerca),costo(Casa,barata).
buscar_casa(Casa):-
    ubica(Casa,cerca),tamanio(Casa,xgrande),
    costo(Casa,cara), permite(Casa,si).
buscar_casa(Casa):-
    ubica(Casa,cerca),tamanio(Casa,muy_grande),
    costo(Casa,barata),permite(Casa,si).
