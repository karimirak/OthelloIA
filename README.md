
# Othello-IA
IA pour le jeu "Othello" jouant sur le serveur : 
https://github.com/qlurkin/PI2CChampionshipRunner

 
# Lancement 
Lancer le serveur : https://github.com/qlurkin/PI2CChampionshipRunner
Une fois le serveur démarré sur localhost, lancer l'IA.
````
 python main.py
````
# Configuration des joueurs
Exemple :
- karim    ==> joue en random
- Ali      ==> joue avec la stratégie minimax
- Husein   ==> joue avec la stratégie weight
````
main.py
  karim = MyInfo('karim', 4000, '5845', 'random')
  Ali = MyInfo('Ali', 4001, '87455','minimax')
  Husein = MyInfo('Husein', 3004, '6352','weight')
````

## Requirements 

Python 3
```
 asyncio
 json
 random
 json
 pytest
 dataclass
 time
 stopit
```




