# IFT1015 : TP 2 - JEU DE ADDICTION SOLITAIRE

# Date : 19/12/2020

import math
import random

def init():
    main = document.querySelector("#main")
    main.innerHTML = styleHTML + addictSolitaireHTML() + brasserCartes + newGame

    deplacementDesCartesValide()
    casesDesDeuxVides()


brasserCartes = '<div id="brasserCartes"> Vous pouvez encore<button onclick="brassage();"> Brasser les cartes </button>  3 fois </div>'
brasse = 0  # brassé 0 fois
newGame = '<button onclick="nouvellePartie()">Nouvelle partie</button> '


styleHTML = """\
<style>
  #jeu table { float: none; width:auto ; max-width:100%; margin :10px 0px 0px 10px } 
  #jeu table td { border: 0; padding: 1px 2px; height: auto; }
  #jeu table td img { height: auto; width:100% }
  #brasserCartes { margin-left:10px ; margin-top:10px }
  button { margin-left:10px ; margin-top:10px }
</style>
"""

# -------------------------------------------------DEBUT DE L'ENCADREMENT-----------------------------------------------------------
"""
Tous les éléments compris dans cet 'encadrement' sont issues et/ou inspirés des exemples, devoirs, ou demonstrations du cours IFT1015.
Certaines fonctionnalités ont cependant étés modifées/rajoutées/adaptées en fonction des besoins du TP.
"""


# La fonction "imgHTML" prend un texte et un entier en parametre  et retourne le
# texte HTML correspondant a une balise "img" avec un attribut "src" et un "id"
# egale au texte et au nombre specifie respectivement en parametre.

def imgHTML(src, idImage):
    return '<img ' 'id=' + str(idImage) + ' src="' + src + '">'


# La fonction "tableHTML" prend un texte de HTML en parametre et
# retourne le texte HTML correspondant a une balise "table" avec le
# contenu specifie en parametre.

def tableHTML(contenu):
    return '<table>' + contenu + '</table>'


# La fonction "trHTML" prend un texte de HTML en parametre et retourne
# le texte HTML correspondant a une balise "tr" avec le contenu
# specifie en parametre.

def trHTML(contenu):
    return '<tr>' + contenu + '</tr>'


# La fonction "tdHTML" prend deux textes en parametre et retourne le
# texte HTML correspondant a une balise "td" qui a les attributs et
# contenu specifie par le premier et second parametres respectivement.

def tdHTML(attrs, contenu):
    return '<td' + attrs + '>' + contenu + '</td>'


# La fonction "trHTMLJoin" prend un tableau de textes en parametre et
# retourne le texte HTML correspondant a une balise "tr" avec un
# contenu qui est la concatenation de tous les textes du tableau passe
# en parametre.

def trHTMLJoin(tab):
    return trHTML(''.join(tab))


# La fonction "tableHTMLJoin" prend un tableau de textes en parametre
# et retourne le texte HTML correspondant a une balise "table" avec un
# contenu qui est la concatenation de tous les textes du tableau passe
# en parametre.

def tableHTMLJoin(tab):
    return tableHTML(''.join(tab))


# La fonction "grouper" prend deux parametres, un tableau T et un
# entier N plus grand ou egal a 1.  La fonction retourne un tableau de
# tableaux.  Les sous-tableaux contiennent les elements du tableau T
# par groupes de N elements, dans le meme ordre que le tableau T.
# Tous les sous-tableaux ont une longueur de N, sauf le dernier qui a
# une longueur entre 1 et N inclusivement.

def grouper(tab, taille):
    groupes = []
    accum = []
    for elem in tab:
        accum.append(elem)
        if len(accum) == taille:
            groupes.append(accum)
            accum = []
    if len(accum) > 0:
        groupes.append(accum)
    return groupes


# La fonction "tableauATableHTML" prend deux parametres, un tableau de
# textes T et un entier N plus grand ou egal a 1.  La fonction
# retourne le texte HTML correspondant à une balise "table" qui
# dispose les éléments de T dans les cellules d'une table de N
# colonnes.  Les cellules de la table sont remplies à partir de la
# rangée du haut (donc l'element de T a l'index 0 sera place dans la
# cellule dans le coin supérieur à droite de la table).

def tableauATableHTML(tab, taille):
    return tableHTMLJoin(list(map(trHTMLJoin, grouper(tab, taille)[::])))


# Images des cartes du jeu de 52 cartes, pour chaque carte, nous avons les symboles rangés dans
# l'odre suivant : Trèfle, Carreaux, Coeur, Pique.

cartesSRC = [
    # As:
    "AC.svg",
    "AD.svg",
    "AH.svg",
    "AS.svg",
    # Deux:
    "2C.svg",
    "2D.svg",
    "2H.svg",
    "2S.svg",
    # Trois:
    "3C.svg",
    "3D.svg",
    "3H.svg",
    "3S.svg",
    # Quatre:
    "4C.svg",
    "4D.svg",
    "4H.svg",
    "4S.svg",
    # Cinq:
    "5C.svg",
    "5D.svg",
    "5H.svg",
    "5S.svg",
    # Six:
    "6C.svg",
    "6D.svg",
    "6H.svg",
    "6S.svg",
    # Sept:
    "7C.svg",
    "7D.svg",
    "7H.svg",
    "7S.svg",
    # Huit:
    "8C.svg",
    "8D.svg",
    "8H.svg",
    "8S.svg",
    # Neuf:
    "9C.svg",
    "9D.svg",
    "9H.svg",
    "9S.svg",
    # Dix:
    "10C.svg",
    "10D.svg",
    "10H.svg",
    "10S.svg",
    # Valet:
    "JC.svg",
    "JD.svg",
    "JH.svg",
    "JS.svg",
    # Dame:
    "QC.svg",
    "QD.svg",
    "QH.svg",
    "QS.svg",
    # Roi:
    "KC.svg",
    "KD.svg",
    "KH.svg",
    "KS.svg"
]

# ---------------Donnees propres au jeu du "Solitaire addict"-------------------
# dimension du jeu = 13x4
dimColonnes = 13
dimeRangees = 4

imgDesDeux = ['<img id="4" src="cards/2C.svg">',
              '<img id="5" src="cards/2D.svg">',
              '<img id="6" src="cards/2H.svg">',
              '<img id="7" src="cards/2S.svg">']
                    


# -----------------------------------------------------------------------------

# La fonction "caseHTML" prend un entier non-negatif N en parametre,
# l'index d'une case de l'echiquier, et retourne le texte HTML
# correspondant a l'element "td" de cette case.  L'element "td" aura
# un id egal a "indexN" et un traiteur d'evenement onclick qui fera
# l'appel de la procedure "clic" avec N en parametre.  L'element "td"
# aura comme contenu un element "img" de la piece sur cette case, ou
# bien un texte vide s'il n'y a pas de carte sur cette case.

# Cette varible va nous aider dans le brassage des cartes, si une carte a déjà été brassée puis placées,
# on l'ajoute à cette varible afin qu'elle ne soit plus comptée dans le brassage.

dejaBrasse = []

def caseHTML(index):
    global dejaBrasse
    i = math.floor(random.random()*52)

    if index > 51:
        return "" # Les limites ne seront pas déppasées

    if len(dejaBrasse) == 52:
        i = dejaBrasse[index]
        contenu = imgHTML('cards/' + cartesSRC[i], i)
    else:
        while True:
            if i in dejaBrasse:
                i = math.floor(random.random()*52)
                continue
            else:
                contenu = imgHTML('cards/' + cartesSRC[i], i)
                dejaBrasse.append(i)

                break

    # On remplace les trèfles par des cases vides.

    if contenu == imgHTML('cards/AC.svg', i) or contenu == imgHTML('cards/AD.svg', i) or contenu == imgHTML('cards/AH.svg', i) or contenu == imgHTML('cards/AS.svg', i):
        contenu = ''


    return tdHTML(' id="case' + str(index) +
                        '" onclick="clic(' + str(index) + ')"',
                        contenu)


# La fonction "addictSolitaireHTML" retourne le texte HTML pour l'element
# "table" correspondant au jeu complet avec les cartes à leur
# position initiale du jeu.

def addictSolitaireHTML():
    return '<div id ="jeu">' + tableauATableHTML(list(map(caseHTML, list(range(dimColonnes * dimeRangees)))), dimColonnes) + '</div>'

# La fonction "elem(n)" retourne le texte HTML correspondant au contenu de la balise
# <body> initialisé au début de la partie.
 
def elem(n):
    return document.querySelector('#case' + str(n))
# --------------------------------------------------FIN DE L'ENCADREMENT----------------------------------------------------------------

# La fonction "nouvellePartie" lance une nouvelle partie lorsqu'on
# clique sur la "Nouvelle partie".

def nouvellePartie():
    global dejaBrasse
    global brasse

    dejaBrasse.clear()
    brasse = 0
    init()

# La fonction "brassage()" brasse le plateu de jeu en conservant les cartes à leur emplacement 
# si elles sont déjà à leurs places.
 
def brassage():
    """ 
    L'affichage du nombre de brassage est adapté en fonction du nombre de brassage restants,
    lors du brassage, on rénitialise notre tableau qui contient a brassé les cartes au début,
    si les cartes sont déjà à leurs places, on les replaces dans le tableau au préalable
    avant de refaire un autre brassage.

    """
    global dejaBrasse
    global brasse
    main = document.querySelector("#main")
    brasser = document.querySelector('#brasserCartes')

    if brasse == 0:

        brasser.innerHTML = 'Vous pouvez encore<button onclick="brassage();"> Brasser les cartes </button>  2 fois' ; brasse += 1; dejaBrasse.clear() #; indexation = 0
        brasserCartes = '<div id="brasserCartes"> Vous pouvez encore<button onclick="brassage();"> Brasser les cartes </button>  2 fois </div>'
        main.innerHTML = styleHTML + addictSolitaireHTML() + brasserCartes + newGame
        casesDesDeuxVides()
        deplacementDesCartesValide()
        nePasBrasser()

    elif brasse == 1:

        brasser.innerHTML = 'Vous pouvez encore <button onclick="brassage();"> Brasser les cartes </button>  1 fois '; brasse += 1; dejaBrasse.clear() #; indexation = 0
        brasserCartes = '<div id="brasserCartes"> Vous pouvez encore<button onclick="brassage();"> Brasser les cartes </button>  1 fois </div>'
        main.innerHTML = styleHTML + addictSolitaireHTML() + brasserCartes + newGame
        casesDesDeuxVides()
        deplacementDesCartesValide()
        nePasBrasser()

    elif brasse == 2:
        
        brasser.innerHTML = 'Vous ne pouvez plus brasser les cartes' ; dejaBrasse.clear() #; indexation = 0
        brasserCartes = '<div id="brasserCartes"> Vous ne pouvez plus brasser les cartes </div>'
        main.innerHTML = styleHTML + addictSolitaireHTML() + brasserCartes + newGame
        casesDesDeuxVides()
        deplacementDesCartesValide()
        nePasBrasser()


# La fonction "indentificateurImage(img)" nous permet de retrouver l'id de 
# l'image donnée en paramètre. Le paramètre correspond au contenu d'une 
# case du plateau.

def indentificateurImage(img):
    """
    On réalise une boucle qui cherche pour chaque image possible, laquelle correspond
    à celle donné en paramètre. 

    """
    for i in range(51):
        balise = '<img id=' + '"' + str(i)+'"' + ' src="cards/' + str(cartesSRC[i])+'"''>'
        if img == balise:
            return i
    else:
        return 0

#--------------------------------------------POUR LA FIN DE LA PARTIE--------------------------------------
# Utile pour determiner la fin de la partie

# "memeSymbole" et "memeValeur" prennent en paramètre le DOM correspondants aux cases voulues.

def memeSymbole(carte1, carte2):
    """ Retoune True si les images correspondant DOM donnés en paramètre ont le même symbole. """
    if indentificateurImage(elem(carte1).innerHTML) % 4 == indentificateurImage(elem(carte2).innerHTML) % 4:
        return True
    else:
        return False


def memeValeure(carte1, carte2):
    """ Retoune True si les images correspondant DOM donnés en paramètre ont la même valeur. """
    if indentificateurImage(elem(carte1).innerHTML)//4 == indentificateurImage(elem(carte2).innerHTML)//4:
        return True
    else:
        return False
#--------------------------------------------POUR LA FIN DE LA PARTIE----------------------------------------

# La procedure "clic" prend un entier non-negatif en parametre qui
# correspond a l'index de la case de la carte qui vient d'etre
# cliquee avec la souris.  La case en haut a gauche a l'index 0, celle
# a sa droite a l'index 1, etc.


def clic(case):
    """ 
    La fonction clic va nous permettre de faire appelle à toutes les fonctions nécessaires
    lors du clics du joueurs afin d'executer les bonnes actions.

    """
                          
    # Pour simplifier les choses, le DOM de notre objet va correspondre
    # à la variable caseEchiquier.

    caseEchiquier = elem(case)

    if caseEchiquier.innerHTML == "":
        # Optionnel -  on peut tout aussi ne rien renvoyer ou même utiliser un "alert".
        msg = print("Selectionnez une case non vide !")
        return msg

    deplacementDesCartes(case) 
    deplacementDesDeux(case)

    casesDesDeuxVides()
    deplacementDesCartesValide()

    if condtitionVictoire() == True:
        alert("Partie terminée, vous avez placés toutes les cartes.")


# "deplacementDesDeuxValide()" va nous permettre de savoir le nombre de case sur la première
# ligne verticale sont libres, afin de savoir si les 2 sont déplaçables.

def deplacementDesDeuxValide():
    """ Retourne le nombre de cases vides sur la première colonne. """
    casesLibres = 0
    if elem(0).innerHTML == '':
        casesLibres += 1
    if elem(13).innerHTML == '':
        casesLibres += 1
    if elem(26).innerHTML == '':
        casesLibres += 1
    if elem(39).innerHTML == '':
        casesLibres += 1
    return casesLibres

# En fonction de si une case sur la première ligne verticale et libre ou non, va attribuer
# la couleur d'arrière-plan 'lime' aux cartes 2.

def casesDesDeuxVides():
    """ 
    Attribut la couleur verte(lime) aux cartes qui ont pour valeures 2.

    """
    if deplacementDesDeuxValide() > 0:
        for i in range(51):
            if elem(i).innerHTML in imgDesDeux:
                elem(i).setAttribute("style", "background-color: lime")

    else:
        for i in range(52):
            if elem(i).innerHTML in imgDesDeux:
                elem(i).removeAttribute("style")


# La fonction "deplacementDesCartesValide()" va attibuer la couleur d'arrière-plan 'lime'
# aux autres cartes en fonction de si elles sont déplaçables ou non selon les règles du jeu.

def deplacementDesCartesValide():
    """
    La fonction va dans un premier temps chercher toutes les cases qui ont un emplacement vide,
    en fonction de ça, on cherche la valeure qui prècède cette case. Une fois cela fait,
    on cherche la valeur supérieur à cette carte qui a le même signe pour afficher son arrière plan
    en vert afin d'indiquer que cette carte est déplaçable selon les règles du jeu.

    """
    global brasse

    # Le tableau t va prendre toutes les valeurs qui sont déplaçables et les stoker.
    # "deplacer" retourne False si aucune carte est déplaçable et retourne True
    # si au moins une carte peut être bougée.
    deplacer = False
    t = []
    msg = document.querySelector('#brasserCartes')

    #  Une boucle qui traite chaque carte du jeu.

    # carteValeurInf = valeur inférieur de la carte déplaçable;
    # carteValeurSup = valeur de la carte déplaçable.

    for i in range(51):
        if elem(i+1).innerHTML == '' and i!=12 and i!=25 and i!=38 and i!=51:
            carteValeurSup = indentificateurImage((elem(i).innerHTML)) + 4

            for j in range(51):
                cartevaleurInf = indentificateurImage((elem(j).innerHTML))

                if cartevaleurInf == carteValeurSup and cartevaleurInf!= 4 and cartevaleurInf!= 5 and cartevaleurInf!= 6 and cartevaleurInf!= 7:  
                    deplacer = True
                    elem(j).setAttribute("style", "background-color: lime")
                    t.append(cartevaleurInf)

                if cartevaleurInf not in t and cartevaleurInf!= 4 and cartevaleurInf!= 5 and cartevaleurInf!= 6 and cartevaleurInf!= 7:
                    elem(j).removeAttribute("style")
                    
    if deplacer == False and brasse != 2:
        # Aucune carte ne peut être bougée, brassage nécessaire.
        msg.innerHTML = 'Vous devez<button onclick="brassage();"> Brasser les cartes </button>' 
    elif deplacer == False and brasse == 2:
        msg.innerHTML = "Vous n'avez pas réussi à placer toutes les cartes..."     

                    

# La fonction "deplacementDesCartes(index)" nous permet de deplacer les cartes au bon endroit.
# index correspond à la case sur laquel le joueur a cliqué. -- donc de renvoyée par la fonction clics(case).

def deplacementDesCartes(index):
    """ 
    La fonction déplace les cartes avec un fond vert au bon endroit; 
    pour cela faire, elle cherche la valeur infirieure de la carte à 
    déplacer et la place juste devant cette dernière.

    """
    #  carteADeplacer corresponf à l'id de l'image contenu dans la case cliquée.

    carteADeplacer = indentificateurImage((elem(index).innerHTML)) 

    if elem(index).innerHTML not in imgDesDeux:
        # carteADeplacer prend la valeur inférieure de la carte à déplacer, donc on fait id - 4 selon les règles du jeu
        carteADeplacer -= 4
        for i in range(51):            
            if indentificateurImage((elem(i).innerHTML)) == carteADeplacer:
                if elem(i+1).innerHTML == '' and i!=12 and i!=25 and i!=38 and i!=51:
                    elem(i+1).innerHTML = elem(index).innerHTML
                    elem(index).innerHTML = ''
                    elem(index).removeAttribute("style")
                    break 

# La fonction "deplacementDesDeux(index)" nous permet de deplacer les 2 dans le jeu car elles ont 
# des restrictions de déplacements spéciales par rapport aux autres cartes.

def deplacementDesDeux(index):
    """ 
    Cherche quelles cases sont libres sur la première ligne verticale en commençant de la gauche,
    elle place la carte sur la première avec un emplacement libre.

    """
    carteADeplacer = elem(index).innerHTML
    
    if carteADeplacer in imgDesDeux:
        if elem(0).innerHTML == '':
            elem(0).innerHTML = carteADeplacer
            elem(index).innerHTML = ''
            elem(index).removeAttribute("style")
            
        elif elem(13).innerHTML == '':
            elem(13).innerHTML = carteADeplacer 
            elem(index).innerHTML = ''
            elem(index).removeAttribute("style")
            
        elif elem(26).innerHTML == '':
            elem(26).innerHTML = carteADeplacer
            elem(index).innerHTML = ''
            elem(index).removeAttribute("style")
            
        elif elem(39).innerHTML == '':
            elem(39).innerHTML = carteADeplacer 
            elem(index).innerHTML = ''
            elem(index).removeAttribute("style")


# La fonction "condtitionVictoire()" nous permet de determiner la condtion de fin du jeu.

def condtitionVictoire():

    """
    Si toutes les cartes se suivent dans un ordre croissant et que les symboles sont identiques,
    la partie est gagnée, c'est ce que fait cette fonction, elle cherche si toutes les valeures se suivent.
    et renvoies True si la partie est gagnée et False si elle n'est pas encore terminée.

    """

    cartesBienPlacees = 0
    for i in range(0,10):
        while memeSymbole(i,i+1) == True:
            cartesBienPlacees =+1
            break
    
    for i in range(13,23):
        while memeSymbole(i,i+1) == True:
            cartesBienPlacees =+1
            break
            
    for i in range(26,36):
        while memeSymbole(i,i+1) == True:
            cartesBienPlacees =+1
            break
            
    for i in range(39,49):
        while memeSymbole(i,i+1) == True:
            cartesBienPlacees =+1 
            break
            
    if cartesBienPlacees == 44:
        msg = document.querySelector('#brasserCartes')
        msg.innerHTML = "Vous avez  réussi à placer toutes les cartes !"
        return True
    else:
        return False

        

def nePasBrasser():

    #La fonction nePasBrasser devrait prendre la position des cartes qui sont bien placées, 
    #et effectuer le brassage seulement sur les cartes mal placées.
   ''' global cartesBienPlacees
    global carteADeplacer
    global imgDesDeux
    global dejaBrasse
    global brasse

    main = document.querySelector("#main")
    brasser = document.querySelector('#brasserCartes')

    if dejaBrasse != [] and memeSymbole(i,i+1) == True and cartesBienPlacees > 2:
        brasser += 1
        carteReste = elem(0).innerHTML

        if carteADeplacer in imgDesDeux:
            if elem(0).innerHTML != '':
                elem(0).innerHTML = carteReste'''





