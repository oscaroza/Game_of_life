# importer le repo sur ton ordi :
```
cd
git clone https://github.com/oscaroza/Game_of_life.git
```

# Avant de coder, importer les modifications des autres :
```
cd Game_of_life
git pull
```

# exporter tes modifs :
```
cd Game_of_life
git pull
git add .
git commit -m "message expliquant la modification"
git push
```


# Autre methode beacoup plus simple : 

cliquer sur l'onglet VSCode donné en capture d'ecran. 
ecrire la decription du changement ds la zone de texte
Et ensuite sur le bouton commit ya une fleche tu cliques dessus et tu vas sur commit and sync. et attendre !

# Build web (pygbag) + Netlify

Depuis la racine du projet :

```bash
./build_web.sh
```

Le site statique est généré dans :

```bash
webapp/build/web
```

Pour Netlify :
- Build command : `python3 -m pip install --upgrade pip pygbag && ./build_web.sh`
- Publish directory : `webapp/build/web`



URL web pr jeu : https://game-of-life-project-ecam.netlify.app/webapp.html
