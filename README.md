# HTMLizr - Interpréteur de langage HTML minimal



## Syntaxe du langage

Soit on écrit la balise HTML standard, soit leur version raccourcie (pour celles qui en ont). 
Ajout d'opérations mathématiques entre balises : boucles, variables et conditions.

Sont définis aussi des noms de "blocs" basés sur Bootstrap4 auxquels sont associés des noms dans le langage. 

Il est possible également de définir un "thème" selon lequel seront choisies les images et les textes placeholder.

### Exemple de syntaxe des blocs

```
com:card
```

donnerait le résultat suivant :

```HTML
<div class="card">
  <img class="card-img-top" src="..." alt="Card image cap">
  <div class="card-block">
    <h4 class="card-title">Card title</h4>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

### Exemple de sytaxe avec opérations et propriétés

```
div.test > ((p > lorem) * 3)
```

donnerait le résultat suivant

```HTML
<div clas="test">
  <p>Lorem ipsum dolor...</p>
  <p>Lorem ipsum dolor...</p>
  <p>Lorem ipsum dolor...</p>
</div>
```

### Exemple de variables

```
$test = "Test variable"
$bool = True

if ($bool){
  p > $test
}
```

donnera donc 

```HTML
<p>Test variable</p>
```
