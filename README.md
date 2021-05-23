# Bienvenue sur le dépot gitlab de la finale de Cod'INSA 2021 de l'équipe Centre-Val-de-Loire
Vous devrez déposer ici vos solutions (code exécutable) pour répondre au sujet de la finale 2021. Vous avez jusqu'au dimanche 23 mai 2021, à 19h30 précises pour rendre vos codes

# Installation

- Python 3.8 ou 3.9

```
$ pip install requests
$ pip install pygame
$ pip install socket
```

# Multiplayer 

- args : no_gui(0/1) username("user") password("pass") multiplayer(0/1) secretkey("secret"/"") room_id("room"/"") \
    eg : 1 "CVL2" "b\\0ZgPJLU=3&#]L9k'l6" 0 "CVL" "" \
         ^                                ^   ^     ^
       nogui                 use multiplayer secret room_id
    room_id => "" pour que le programme crée la room

## Documentation du sujet
|Version | Date heure     |lien      |
| :--------------- |:---------------:| -----:|
| 1 |22/05 15h30    |https://drive.google.com/file/d/1an8mo_1nowGP6dou8U79EBBnEiIj4bUR/view?usp=sharing |
| 2 |22/05 16h|https://drive.google.com/file/d/1os6bqkWkEB67eXL8NOBMDI6xvpJ8dyR8/view?usp=sharing|
|3|22/05 19h15|https://drive.google.com/file/d/1YVJczjsQTFAAp1m7UxNXZ9uSSL6Zq0BB/view?usp=sharing|

## Codes de connexion au serveur de test
Vous devrez vous connecter à http://codinsa.insa-rennes.fr/init, en post avec un dictionnaire Json (avec les clefs “username” et “password”):
|username|password|
| :--------------- | -----:|
|CVL1 |+GC;GY8]dK1EYbS=ja*;U|
|CVL2 |b\\0ZgPJLU=3&#]L9k'l6|
|CVL3 |.WCX6_KO9<PVh-F9V@PmNlL?|
