MAXIME ROUSSEL ET ANOUP SUNGKER
INFO L3



####################################
#      LA GUERRE DES ROBOTS        #
####################################

Principe : Des robots se battent sur une map de 30x20 grâce à des actions
qu’il est possible de faire . Les robots ont un niveau d’énergie et dès qu’une
action est faite de l’énergie est consommé. Dès qu’un robot n’a plus d’énergie,
il est considéré comme mort.

Les actions disponibles :

DD : Déplacement dans une direction donnée
AL : déplacement aléatoire
MI : pose d’une mine
IN : invisibilité
PS : repère le robot le plus proche et se déplace d’une case dans sa direction
FT : repère le robot le plus proche et s’éloigne de lui d’une case
TH : Tir horizontal
TV : Tir vertical
TT : Instruction de test, suivi de deux instructions :
si l’adversaire le plus proche est à une distance inférieure ou égale à
la portée du radar alors on fait la première instruction, sinon on fait la seconde.

Les programmes des robots contiennent une instruction par ligne

coût des instructions :

DD coût 5 d’énergies
AL coût 1 d’énergies
MI coût 10 d’énergies   provoque 200 de dégât a l'adversaire
IN coût 20 d’énergies
PS coût 4 d’énergies
FT coût 4 d’énergies
TH coût 3 d’énergies    provoque 20 de dégât a l'adversaire
TV coût 3 d’énergies    provoque 20 de dégât a l'adversaire
TT coût 4 d’énergies



comment marche le projet :

  un robots est définies par un fichier texte.txt (pas .rbt j'ai oublier de changer)
  ensuite nous allons sélectionner une map et les robots qui vont jouer


  la map est un objet de la class map qui contient matrice qui vas contenir les murs,
  mines,robots,tir
  ainsi que les attribut suivant : pourcentage d'obstacle , lignes et colonnes

  un robot est un objet de la class Robot, il contient les attribut suivant:
  -nom du robot
  -id du robot
  -batterie
  -radar
  -invisibilité
  -et il connaît sa position dans la map

  une fois la map choisie parmi celle qui sont importer
  nous allons devoir choisir entre tous les robots importer

  nous devons en choisir entre 2 et 6 pas plus pas moins sinon l'application bug
  une fois les robots choisie on va crée une liste avec le nom des robots choisie
  puis avec cette liste et les réglages de la batterie ,et du radar.

  Nous allons donc pouvoir placer aléatoirement les robots dans la map.

  maintenant lançons la game.
  nous allons donc lire leur instructions, si un robot meurt il est supprimer
  de la map et naturellement, nous ne lisons plus ces instructions

  une fois la partit terminer le dernier robot ajouter a la liste des robots mort
  et gagnant

  il ne peut y avoir d'égalité. par ailleurs les premiers robots ajouté dans la map
  sont avantagé puisque leur instruction sont exécuter en premier il peuvent donc tiré
  placer une mine en premier par rapport au prochain robot

  ils s'agit d'un choix conceptuel qui permet de gérer plus efficacement le
  déroulement de la partit

  chaque robot exécute sont instructions, si il n'a plus de batterie il meurt

  les instructions sont exécuter selon l'ordre d'initialisation des robots
  dans la map

  donc dans l'ordre ou on n'a choisie les robots.

  pour ce qui est du déroulement de la partit dans l'interface graphique
  (testgraph.py)

  les robots ont tous une couleur différentes indiqué sur leur
  profil en bas a gauche

  les mines sont représenter par un carré rouge
  et les tir par un carré vert qui parcours la map



ce qui bug :

  on peut certes retourner en arrière dans le menu etc...
  mais une fois les map ou les robots instancié aucune fonction pour réinitialiser
  les objet on était mis en place car j'y avais pas pensé sur le coup

  pour les scales il faut cliquer dessus même si la valeur que l'on n'a voulu sélectionner
  est bonne,sinon la valeur par default est sélectionner


                    ######################
                        LES AIDES
                    ######################

étant donner que je n'ai pas eu le temps de programmer les aides interactives
voici comment se servir le l'interface :

-Dans la fenetre MENU, on peut y trouver 3 options :
  1-play renvoi a la sélection de la map permet de choisir sur qu'elle map les robots
    vont jouer

  2-options : permet d'importer des robots et des map directement dans le jeu

  3-quitter : permet de quitter l'application


############################
-La fenêtre CHOIX DES MAPS :
############################

on choisie qu'elle mode de map on désire entre libre : sélection précise de la map
ou RANDOM : une map random est alors Générer selon le pourcentage d'obstacle indiqué
les maps peuvent etre choisie parmi les maps importer dans l'application


le bouton précédent permet de revenir au MENU
et le bouton suivant permet de passer a la sélection des robots

ATTENTION : -les fichiers des maps sont considérer comme juste
              si une mauvaise maps est donné il se peut que l'application crash

une map doit être au format suivant :

(dois être entourer de murs)

################################
#______________________________#
#___________________#____#_____#
#______######__######______#___#
##_____#____________#______#___#
#_____##__####_____#####___#___#
#__________________#_______#___#
#___##___####______#___#####___#
#__________##______#___#_______#
####_____####______#___#####___#
#___________#______#___#___#___#
#___####____#______#___#___#___#
#___#_______#______#___#___#___#
#___#___#####______#___#_______#
#___#_______#__________#####___#
#___##______#__##__________#___#
#____#______#______________#___#
#____#______############___#___#
#____#_________________#_______#
#____#####_____________________#
#______________________________#
################################


# : les murs
_ : espace vide

murs(#) en diagonal sont interdit


un map dois être JOUABLE sur un dimension par 20*30 :
le nombre de obstacle dois être au maximum de 120 soit 20 %

seul la fonction Random Map vérifie ces spécificité
la sélection libre repose sur la confiance de l'utilisateur et de l'importation
de ces map



############################
-La fenêtre CHOIX DES ROBOTS :
############################

on choisie ici les robots qui vont jouer parmi les robot importer dans l'application

ATTENTION : -ils faut au moins 2 robots sélectionner pour jouer
            -les fichiers des robots sont considérer comme juste syntaxiquement et
            sémantiquement aucune vérification hormis le nombre d'instruction
            n'est effectuer

            si un robot n'a pas le nombre d'instruction requis il est supprimer
            et la game ne se lance pas et l'application peut donc freez

le fichier d'un robot dois êtres présenté comme celui ci :

waynneer.txt

AL   (instruction de secours)
TT PS AL
AL
MI
AL
DD H
DD B
TT PS AL
TT PS AL
TT PS AL
MI
TT IN AL
IN


au maximum 21 lignes d’instruction en comptant l'instruction de secours
et au minimum 6 lignes avec l’instruction de secours.


#################
-la fenêtre PLAY :
#################

comporte la liste des robots choisie au préalable avec leur nombre de vie
l'affichage de la map avec les robots dedans
et un bouton start pour lancer la game


##################
la fenêtre option :
##################
comporte une scale censé régler la vitesse de jeu
2 bouton import map et robot pour importer une map ou un robot dans leur dossier
respectif



########################
arborescence du projet :
########################


PROJET
.
├── 1rock.png
├── image ----------------<dossier des images>
│   └── pngtree-future-intelligent-technology-robot-ai-png-image_2588803.jpg
│ 
├── MAIN.py -----------------------------<programme gestion des robots>
│ 
├── maps (dossier des maps)
│   ├── illusion.txt
│   ├── MapInGame.txt
│   └── test.txt
├── modele ---------------------------------< fichier qui contient les classes >
│   │ 
│   ├── map.py -----------------------------<classe qui gère la map>
│   ├── robot.py ----------------------------<classe qui gère les robots>
│  
├── play.py ---------------------------------<contient les variables global>
├── progRobot (fichier contenant tous les robots)
│   ├── anoupMK3.txt
│   ├── burton.txt
│   ├── maxilef.txt
│   ├── test.txt
│   └── waynneer.txt 
│  
├── README.txt
├── robot1.png (image de fond de la fenêtre MENU)
│ 
└── testgraph.py ---------------------------------<interface graphique>

Structure du programme :

Dossier maps :dossier où sont stockés les maps jouables
Dossier progRobots : dossier où sont stockés les programmes des différents robots
Testgraph.py : interface graphique
Map.py : définition de la class Map
Robots.py : définition de la class Robot
Main.py : définition des différentes actions des robots
Play.py : fonctions pour lancer la partie.




########################
      BON JEUX !!
########################
