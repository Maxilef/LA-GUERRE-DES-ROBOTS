###################################
##############IMPORT##############
#################################
from modele.map import Map
from modele.robot import Robot
from maps import *
import play

from tkinter import messagebox


import math
import random
import time
import os
import sys


#############################################
#              PARTIT ROBOTS                #
#############################################

# ici on gére les intéraction de nos robots avec la map
# partit caché de l'iceberg

# c'est ici ou se déroule toute la partit
# initialisation des robots / map
# etc...



"""
NOTE :
    -si un robot selectionner nas pas assez de ligne ou trop de ligne
    la game ne se lance pas sans lui car il fait partit des objets
    instancier dans la parti
    surement un conflie entre RUN_robot et Lire

    -il y a beacoup de répitition de meme ligne j'ai essayé d'y remedier
    mais sur certaine il y a des erreurs que je n'ai pas le temps de corriger
    en autre car je suis le seul a avoir bosser sur la partit terminal

    -certaine fonction comme RUN sont très grandes est aurait pue etre simplifier


a faire :
partie non graphique :
    RBOT :
        lire des fichier d'extention .rbt

partie graph:
    faire bouger les robot dans tkinter
    pouvoi mettre en pause la game
"""


###################################
############## START #############
#################################

################GLOBAL#######################

#signalement si on n'a touché une mine
signal = 0

#correspond au champ d'action de la fonction TT
# 0 => detection sur toute la map sinon seulement la porté du radar
perimetre_de_detection = 0

#       robots
battery = play.battery
radar = play.radar

#liste vide des robot que l'on vas faire jouer
liste_robot = play.liste_robot

#liste des robot mort dans la partit
liste_robot_mort = []
#instruction des robots dans la partit
liste_instru_secours = []
#intruction des robots sur la map
liste_instruction = []


#map
obstacle = play.obstacle
map = play.map


#vitesse de la game
time_for_instru = play.time_for_instru


#############################################



#######################################################
# FONCTION NECCESAIRE A LA DETECTION

"""fonction du perimetre du radar"""
#retourne la liste les positions des robot compris dans le perimetre du robot
def Radar(robot,map,perimetre_de_detection):

    porte_radar = robot.__get_radar__()

    posx_robot = robot.__get_pos_x__()
    posy_robot = robot.__get_pos_y__()
    liste_des_robot_detecter = []

    #on va parcour la matrice depuis le coint en haut a gauche en fonction de la
    #porté du radar

    #porte du radar = 4
    #i

#j  # # # # # # # # #
    # # # # # # # # #
    # # # # # # # # #
    # # # # # # # # #
    # # # # X # # # #
    # # # # # # # # #
    # # # # # # # # #
    # # # # # # # # #
    # # # # # # # # #


    # si TT alors on regarde on fonction de la porté du radar
    if perimetre_de_detection != 0 :
        i = robot.__get_pos_x__() - perimetre_de_detection
        j = robot.__get_pos_y__() - perimetre_de_detection

        ip = robot.__get_pos_x__() + perimetre_de_detection
        jp = robot.__get_pos_y__() + perimetre_de_detection

    # toute la map #coin en haut a gauche
    else :
        i = 1
        j = 1

        ip = 20
        jp = 30


    # verification si radar sort de la map
    if i < 1 :
        i=1
    if j < 1 :
        j= 1

    if ip > map.l-2 :
        ip = map.l-2

    if jp > map.c-2 :
        jp = map.c-2

    # Trouver la position des robot dans la matrice
    while i <= ip :
        j = 0
        while j <= jp :

            # Vérifier si l'élément à la position (x, y) est un entier en
            # utilisant isinstance
            check = map.__get_position__(i,j)
            if isinstance(check, int) :

                # on verifie aussi que le robot ne se compte pas parmis
                # les detection
                if check != robot.__get_ident__() :

                    # on verifie aussi que le robot detecter n'est pas invisible
                    # on recupere l'id que on n'a trouver dans la map

                    id = check
                    #on regarde a qui l'id appartient dans la liste des robot in game
                    global liste_robot
                    liste_robot = play.liste_robot
                    target_robot = get_robot_by_id(id,liste_robot)



                    #si le robot detecte n'est pas invisible
                    if target_robot.__get_invisible__() == 0 :
                            #on le met dans la liste
                            liste_des_robot_detecter += [(i,j)]

            j += 1
        i += 1

    #retourn VRAI si detecter + la liste des detection
    if ( len(liste_des_robot_detecter) > 0 ) :
        return True, liste_des_robot_detecter

    #si pas de detection retourn FAUX
    return False, liste_des_robot_detecter

"""retourn si l'entrer donner en parametre est un int"""
def is_integer(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

"""choisie aleatoirement entre 2 entier"""
def choose_random_int(a, b):
    # Générer un nombre aléatoire entre 0 et 1
    rand = random.random()

    # Si le nombre aléatoire est inférieur à 0,5, retourner a, sinon retourner b
    if rand < 0.5:
        return a
    else:
        return b

"""trouve le robot le plus proche"""
def plus_proche(robot,map):
    # si on a au moin une touche on regarde la position (x,y) renvoyer par le
    # radar
    if Radar(robot,map,perimetre_de_detection)[0] == 1:
        # on recupere la liste des item detecter
        liste_des_robot_detecte = Radar(robot,map,perimetre_de_detection)[1]

        #on recup la position de notre robot
        x1 = robot.__get_pos_x__()
        y1 = robot.__get_pos_y__()

        #liste pour rentrer les différentes distance de tous les item detecter
        liste_distance=[]

        # Parcourir tous les tuples de la liste
        # exemple de liste : [(4,3),(2,1)]
        for t in liste_des_robot_detecte:
            x2 = t[0]
            y2 = t[1]

            # Calculer la distance entre les deux entiers en utilisant
            # la formule de la distance Euclidienne
            distance = abs(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

            #inserer la distance dans liste des distance
            liste_distance += [int(distance)]


         # On initialise l'indice du plus petit élément à 0
        indice_plus_petit = int(0)

        i = int(1)

        while i < len(liste_distance) :
            # Si l'élément à l'indice i est plus petit que l'élément à l'indice
            # indice_plus_petit,
            # on met à jour l'indice du plus petit élément
            if liste_distance[i] < liste_distance[indice_plus_petit]:
                indice_plus_petit = int(i)

            if (liste_distance[i] == liste_distance[indice_plus_petit]) :

                indice_plus_petit = choose_random_int(i,indice_plus_petit)

            i += 1
        # On retourne l'indice du plus petit élément
        return liste_des_robot_detecte[indice_plus_petit]


    else :
        print("pas de plus proche")
        return 0

#######################################################

"""
        GESTION INSTRUCTION ROBOT
"""

"""lit une ligne d'instruction et execute les commande associé"""
def application_instru(robot,instruction,map):

    #faire un dico pour les perte de bttery
    """
    list1 = [1, 2, 3, 4]
    val = random.choice(list1)
    dico = {1:"H", 2:"B", 3:"D",4:"G"}
    """

    dico_battery = {"AL":1, "DD":5, }


    instru = instruction.split()
    first = instru[0]
    bat_robot = robot. __get_battery__()

    #print(robot.__get_name__(),"->",first)
    if first == "AL" and bat_robot >= 1 :
        robot.damage(1)
        AL(map,robot)

    elif first == "DD" and bat_robot >= 5 :
        robot.damage(5)
        second = instru[1]
        DD(map,robot,str(second))

    elif first == "PS" and bat_robot >= 4 :
        robot.damage(4)
        PS(map,robot)

    elif first == "FT" and bat_robot >= 4 :
        robot.damage(4)
        FT(map,robot)

    elif first == "TT" and bat_robot >= 4 :
        robot.damage(4)
        second = instru[1]
        third = instru[2]
        TT(robot,map,str(second),str(third))

    elif first == "MI" and bat_robot >= 10 :
        robot.damage(10)
        Mine(robot,map)

    elif (first == "TH" or first == "TV") and bat_robot >= 3 :
        robot.damage(3)
        TIR(robot,map,first[1])

    elif first == "IN" and bat_robot >= 20 :
        robot.damage(20)
        INVISIBILITE(map,robot)

    #si aucune autre instruction n'a était effectuer
    # alors intruction mal écrie ou alors bttery robot pas suvisante pour
    # son execution

    else :

        robot.check_battery()
        # recup de ces coordonnées
        x = robot.__get_pos_x__()
        y = robot.__get_pos_y__()
        #del de la pos du rbt dans map
        map.__sup_ele_in_map__(x,y)
        global liste_robot_mort
        liste_robot_mort += [robot.__get_name__()]
        #play.liste_robot_mort = liste_robot_mort



###############
# DEPLACEMENT #
###############
"""deplacement random du robot"""
def AL(map,robot):
    # prints a random value from the list
    list1 = [1, 2, 3, 4]
    val = random.choice(list1)
    dico = {1:"H", 2:"B", 3:"D",4:"G"}

    if robot.__get_battery__() >= 1 :
        DD(map,robot,dico[val])

"""deplacement choisie robot"""
def DD(map,robot,direction):
    #x les ligne    #y les colone

    x = robot.__get_pos_x__()
    y = robot.__get_pos_y__()
    #del de la pos du rbt dans map
    map.__sup_ele_in_map__(x,y)


# deplacement sur mine possible  if ..... or check_map == tuple(map.matrix[x-1][y]) faut recup l'id de la mine aussi
#sur map fichier mine == X et sur matrice ("X",id_robot)

    #on peut se deplacer si la case est libre ou si la case contient une mine
    #dans ce cas on prend des dégat si ce n'est pas la mine du robot qui rentre
    #dedans

    #si il s'agit de la mine du robot qui rentre dedans alors le robot en question
    #ne peut pas se deplacer sur sa propre mines


    if direction == "H" :
        if check_map(map,x-1,y) == "_" or isinstance(check_map(map,x-1,y), tuple) :
            x -= 1
        else:
            print("Impossible collision ")

    if direction == "B" :
        if check_map(map,x+1,y) == "_" or isinstance(check_map(map,x+1,y), tuple):
            x += 1
        else:
            print("Impossible collision ")

    if direction == "G" :
        if check_map(map,x,y-1) == "_" or isinstance(check_map(map,x,y-1), tuple):
            y -= 1
        else:
            print("Impossible collision ")

    if direction == "D" :
        if check_map(map,x,y+1) == "_" or isinstance(check_map(map,x,y+1), tuple):
            y += 1
        else:
            print("Impossible collision ")

    print("le robot {",robot.__get_name__(),"} se deplace vers {",direction,"}")


    # si un tuple dans map alors c'est une mine
    if isinstance(check_map(map,x,y), tuple):

        # on regarde si il s'agit d'une mine a nous
        if int(check_map(map,x,y)[1]) != int(robot.__get_ident__()):
            print("le robot {",robot.__get_name__(),"} heurte une mine de plein fouet")
            # ce n'est pas notre mine on saute dessus trop tard !
            # on prend des degats

            bat_robot = robot.__get_battery__()



            #BOOM on n'a touché une mine
            #on charche a éviter que le robot apres avoir subit des dégat
            #passe en valeur négative sur sa batery
            if bat_robot >= 200 :
                robot.damage(200)
            else :
                degat = 200 - abs(bat_robot - 200)
                robot.damage(degat)

            #REMPLACEMENT PAR INSTRUCTION DE secours
            #je signal que j'ai touché une mine
            global signal
            signal = 1


            # on suprime la mine
            map.__sup_ele_in_map__(x,y)

        # si il s'agit d'une mine a nous
        elif int(check_map(map,x,y)[1]) == int(robot.__get_ident__()):

            # nous avons detecter notre propre mine donc on ne saute pas dessus
            # on re récupére la positon initial du robot avant de bouger
            x = robot.__get_pos_x__()
            y = robot.__get_pos_y__()
            #puis on replace le robot ensuite


    #ajout du rbt dans map apres avoir tous check
    ajouter_robot_in_map(map,robot,x,y)

    #récrire la map dans le fichier de map du jeu
    ecrire_map("MapInGame.txt",map)

"""Poursuite du robot dans la map"""
def PS(map,robot):
    #cout 4 de battery

    perimetre = Radar(robot,map,perimetre_de_detection)[0]
    #si un robot dans perimetre de radar
    if perimetre :
        #on regarde ou et le plus proche
        PP = plus_proche(robot,map)
        #on s'y dirige
        x = robot.__get_pos_x__()
        y = robot.__get_pos_y__()

        #direction vers x //  HAUT ET BAS
        if PP[0] == x :
            choix = choose_random_int(0,1)
            if choix == 1 and check_map(map,x-1,y) == "_":
                DD(map,robot,"B")
            elif choix != 1 and check_map(map,x+1,y) == "_":
                DD(map,robot,"H")

        elif PP[0] > x :
            DD(map,robot,"B")
        elif PP[0] < x :
            DD(map,robot,"H")

        #direction vers y // DROITE et GAUCHE
        if PP[1] == y :
            choix = choose_random_int(0,1)
            if choix == 1 and check_map(map,x,y-1):
                DD(map,robot,"D")
            elif choix != 1 and check_map(map,x,y+1):
                DD(map,robot,"G")

        elif PP[1] >= y :
            DD(map,robot,"D")
        elif PP[1] <= y :
            DD(map,robot,"G")
    else :
        #rien pas de poursuite
        pass

"""Fuite du robot dans la map"""
def FT(map,robot):
    #cout 4 de battery

    perimetre = Radar(robot,map,perimetre_de_detection)[0]
    #si un robot dans perimetre de radar
    if perimetre :
        #on regarde ou et le plus proche
        PP = plus_proche(robot,map)
        #on s'y dirige
        x = robot.__get_pos_x__()
        y = robot.__get_pos_y__()

        #direction vers x //  HAUT ET BAS
        if PP[0] == x :
            choix = choose_random_int(0,1)
            if choix == 1 and check_map(map,x-1,y) == "_":
                DD(map,robot,"H")
            elif choix != 1 and check_map(map,x+1,y) == "_":
                DD(map,robot,"B")

        elif PP[0] > x and check_map(map,x-1,y) == "_" :
            DD(map,robot,"H")

        elif PP[0] < x and check_map(map,x+1,y) == "_" :
            DD(map,robot,"B")



        #direction vers y // DROITE et GAUCHE
        if PP[1] == y :
            choix = choose_random_int(0,1)
            if choix == 1 and check_map(map,x,y-1):
                DD(map,robot,"G")
            elif choix != 1 and check_map(map,x,y+1):
                DD(map,robot,"D")

        elif PP[1] > y and check_map(map,x,y-1) == "_" :
            DD(map,robot,"G")

        elif PP[1] < y and check_map(map,x,y+1) == "_" :
            DD(map,robot,"D")

"""condition si detection"""
def TT(robot,map,instru1,instru2):

    perimetre_de_detection = robot.__get_radar__()
    #si un robot dans perimetre de radar
    if Radar(robot,map,perimetre_de_detection)[0]:
        #faire premiere instru
        perimetre_de_detection = 0
        #print(instru1)
        application_instru(robot,str(instru1),map)

    elif not Radar(robot,map,perimetre_de_detection)[0]:
        #faire deuxieme instru
        perimetre_de_detection = 0
        #print(instru2)
        application_instru(robot,str(instru2),map)


#########
# ARMES #
#########

"""fonction Mine du robot"""
def Mine(robot,map) :
    #but mettre une mine sur la map avec l'id du joueur qu'il a posé
    # au format (X,id_robot)
    # une mine peut etre posé que de la façon suivante :

#    _X_
#    XRX
#    _X_

    # => choix d'une position random pour la mine
    list1 = [1, 2, 3, 4]
    val = random.choice(list1)
    dico = {1:"H", 2:"B", 3:"D",4:"G"}


    #pose de la mine
    Pose_Mine(map,robot,dico[val])


"""fonction pour poser mines autour du robot"""
def Pose_Mine(map,robot,direction):

    x = robot.__get_pos_x__()
    y = robot.__get_pos_y__()

    # si case libre (ou qu'il y a un robot)
    # pose de la mine possible sur la map des mines
    if direction == "H" and ( check_map(map,x-1,y) == "_" ):
        #ajouter mine in map de mine
        x -= 1

    if direction == "B" and ( check_map(map,x+1,y) == "_" ):
        x += 1

    if direction == "G" and ( check_map(map,x,y-1) == "_" ):
        y -= 1

    if direction == "D" and ( check_map(map,x,y+1) == "_" ):
        y += 1

    if check_map(map,x,y) == "_" :
        #ajout de la mine sur la map
        print("le robot {",robot.__get_name__(),"}place une MINE a {",direction,"{")
        map.__set_mine_in_map__(robot,x,y)


"""fonction pour que un robot TIR"""#TH #TV
def TIR(robot,map,direction):
    list1 = [1, 2]
    #savoir si direction Vertical ou Horisontal
    if direction == "H" :
        #apres choisir aléatoirement si tir Droite ou Gauche
        val = random.choice(list1)
        dicoH = {1:"D", 2:"G"}

        application_tir(robot,map,dicoH[val])


    elif direction == "V" :
        #apres choisir aléatoirement si tir Haut ou Bas
        val = random.choice(list1)
        dicoV = {1:"H", 2:"B"}

        application_tir(robot,map,dicoV[val])

#retoune le robot avec l'id donné
def get_robot_by_id(id, robot_list):
    for Robot in robot_list:
        if Robot.__get_ident__() == id:
            return Robot

#le tir parcour la map
def application_tir(robot,map,direction) :

    #recup pos du robot
    x = robot.__get_pos_x__()
    y = robot.__get_pos_y__()
    tir_precedentx = x
    tir_precedenty = y
    deja_tiré = 0

    if direction == "H" :
        direction_tir = "^"
        x -= 1
        while check_map(map,x,y) == "_" or isinstance(check_map(map,x,y), tuple) or isinstance(check_map(map,x,y),int) :
            #si case vide ou il y a un mine ou c'est un robot
            res = exe_tir(map,direction_tir,x,y,robot)

            if res == 1 :
                break

            if  deja_tiré == 0 :
                # ajout du tir
                map.__set_tir_in_map__(direction_tir,x,y)
                deja_tiré = 1

            else :
                #on delete le tir precedent
                map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
                map.__set_tir_in_map__(direction_tir,x,y)

            #puisque on n'a deja tiré on réucpére le tir précedent
            tir_precedentx = x
            tir_precedenty = y

            #map
            # on écrie dans notre map le tir effectuer et on l'affiche
            ecrire_map("MapInGame.txt",map)
            affiche_mapingame("MapInGame.txt")
            #on suprime le tir précedent
            map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
            #on affiche l'état des robots
            for j in range(len(liste_robot)) :
                etat_robot(liste_robot[j])

            #on attent que le tir de propage
            time.sleep(0.015)


            x -= 1

    if direction == "B" :
        direction_tir = "v"
        x += 1
        while check_map(map,x,y) == "_" or isinstance(check_map(map,x,y), tuple) or isinstance(check_map(map,x,y),int) :
            #si case vide ou il y a un mine ou c'est un robot
            res = exe_tir(map,direction_tir,x,y,robot)
            if res == 1 :
                break
            if  deja_tiré == 0 :
                # ajout du tir
                map.__set_tir_in_map__(direction_tir,x,y)
                deja_tiré = 1

            else :
                #on delete le tir precedent
                map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
                map.__set_tir_in_map__(direction_tir,x,y)

            tir_precedentx = x
            tir_precedenty = y
            #map
            ecrire_map("MapInGame.txt",map)
            affiche_mapingame("MapInGame.txt")
            map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
            for j in range(len(liste_robot)) :
                etat_robot(liste_robot[j])
            time.sleep(0.015)

            x += 1


    #tir a gauche
    if direction == "G" :
        direction_tir = "<"
        y -= 1
        while check_map(map,x,y) == "_" or isinstance(check_map(map,x,y), tuple) or isinstance(check_map(map,x,y),int) :
            #si case vide ou il y a un mine ou c'est un robot
            res = exe_tir(map,direction_tir,x,y,robot)
            if res == 1 :
                break

            if  deja_tiré == 0 :
                # ajout du tir
                map.__set_tir_in_map__(direction_tir,x,y)
                deja_tiré = 1

            else :
                #on delete le tir precedent
                map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
                map.__set_tir_in_map__(direction_tir,x,y)

            tir_precedentx = x
            tir_precedenty = y
            #map
            ecrire_map("MapInGame.txt",map)
            affiche_mapingame("MapInGame.txt")
            map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
            for j in range(len(liste_robot)) :
                etat_robot(liste_robot[j])
            time.sleep(0.015)

            y -= 1



    if direction == "D" :
        direction_tir = ">"
        y += 1
        while check_map(map,x,y) == "_" or isinstance(check_map(map,x,y), tuple) or isinstance(check_map(map,x,y),int) :
            #si case vide ou il y a un mine ou c'est un robot
            res = exe_tir(map,direction_tir,x,y,robot)

            if res == 1 :
                break

            if  deja_tiré == 0 :
                # ajout du tir
                map.__set_tir_in_map__(direction_tir,x,y)
                deja_tiré = 1

            else :
                #on delete le tir precedent
                map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
                map.__set_tir_in_map__(direction_tir,x,y)

            tir_precedentx = x
            tir_precedenty = y
            #map
            ecrire_map("MapInGame.txt",map)
            affiche_mapingame("MapInGame.txt")
            map.__sup_ele_in_map__(tir_precedentx,tir_precedenty)
            for j in range(len(liste_robot)) :
                etat_robot(liste_robot[j])

            time.sleep(0.015)

            y += 1

#une fois tiré on regarde ce qu'on a touché
def exe_tir(map,direction_tir,x,y,robot):

        #on vérifie si on hit une mine ou un robot

        #si c'est une mine
        if isinstance(check_map(map,x,y), tuple):

            #on regarde si elle nous appartient
            if int(check_map(map,x,y)[1]) != int(robot.__get_ident__()):
                #elle n'est pas a nous, on peut la détruire
                map.__sup_ele_in_map__(x,y)

            return 1


        #sinon c'est un robot
        elif isinstance(check_map(map,x,y), int):

            # on affige des dégat au robot touché

            #problematique :
            """comment trouver le robot que on n'a touché"""

            # on recupere l'id que on n'a trouver dans la map
            id = check_map(map,x,y)

            #on regarde a qui l'id appartient dans la liste des robot in game
            global liste_robot
            target_robot = get_robot_by_id(id,liste_robot)

            #on lui infflige des dégats
            robot.attack_robot(target_robot)

            return 1

""""""
#rend invisible un robot
def INVISIBILITE(map,robot):
    # on met le robot a l'état d'invisible
    robot.set_invisible(1)
    #note :
    # il faut le remttre visible au prochain tour donc
    # dans RUN_robot apres avoir executer les instruction de tous les autres
    # robot on remet visible le robot

    # pour que le mode IN marche il faut que la detection de detecte pas les
    # robot invisible


#######################################################

"""
            GESTIONS DE LA MAP
"""

"""ecrie la matrice dans le fichier de la map du jeu"""
def ecrire_map(fichier,map):

    name = str(fichier)
    racine_du_fichier = "./maps/"+str(name) #print(racine_du_fichier)
    #verification si le fichier peut s'ouvrir
    try :
        fichier = open(str(racine_du_fichier), "w")
        for i in range(map.l):
            for j in range(map.c):
                val = map.matrix[i][j]
                if isinstance(val, tuple):
                    fichier.write(str(val[0]))
                else :
                    fichier.write(str(val))
                if j+1 == map.c :
                    fichier.write("\n")

        fichier.close()

    except FileNotFoundError:
        print("le fichier n'a pas pue etre ouvert ou n'existe pas ")


"""affiche dans le terminal la map depuis le fichier de la map in game """
def affiche_mapingame(fichier) :

    #clear le terminal
    os.system('clear')


    name = str(fichier)
    racine_du_fichier = "./maps/"+str(name)

    #verification si le fichier peut s'ouvrir
    try :
        fichier = open(str(racine_du_fichier), "r")
        readf = fichier.read()
        print(readf)
        # on souhait affaicher la map dans le canvas
        # on récupere la fonction dans la partit graph

        print(play.battery)
        if play.canvasforgame != 0 :
            # Utilise la fonction RUN_GAME ici
            play.RUN_GAME(play.canvasforgame)



        fichier.close()

    except FileNotFoundError: #traite l'erreur quand le fichier n'est pas trouvé
        print("le fichier n'a pas pue etre ouvert ou n'existe pas ")


"""INITIALISATION DES ROBOT DANS LA MAP"""
def init_robot_in_map_alea(liste_robot,map):

    for i in range(len(liste_robot)):
        ajouter_alea_robot_in_map(map,liste_robot[i]) #id 0


"""fonction pour recup se qu'il y a la la pos x,y de la matrice """
def check_map(map,x,y):
    pos = map.__get_position__(x,y)
    return pos


"""fonction pour reset la map de jeu"""
def resetmap(map,fichier):
    name = str(fichier)
    racine_du_fichier = "./maps/"+str(name) #print(racine_du_fichier)
    #verification si le fichier peut s'ouvrir
    try :
        fichier = open(str(racine_du_fichier), "w")
        for i in range(map.l):
            for j in range(map.c):
                fichier.write("#")
                if j+1 == map.c :
                    fichier.write("\n")
        fichier.close()

    except FileNotFoundError:
        print("le fichier n'a pas pue etre ouvert ou n'existe pas ")


"""fonction pour ajouter un robot dans une map """
def ajouter_robot_in_map(map,robot,x,y):
    #resetmap(map,"MapInGame.txt")

    map.__set_robot_in_map__(robot,x,y) #ajout d'un robot sur la map
    robot.__set_pos_robot__(x,y) #ajout de la position sur la map au robot
    ecrire_map("MapInGame.txt",map)


"""fonction pour ajouter aleatoirement un robot dans une map """
def ajouter_alea_robot_in_map(map,robot):

    max_x = map.l
    max_y = map.c

    random_x = 0
    random_y = 0

    #verifier avant si pos random_x et random_y sont libre avant ajout
    while (map.matrix[random_x][random_y]) != "_" :
        #on ne prend pas en compte le tour de la map
        random_x = random.randint(1, max_x-2)
        random_y = random.randint(1, max_y-2)

    map.__set_robot_in_map__(robot,random_x,random_y) #ajout d'un robot sur la map
    robot.__set_pos_robot__(random_x,random_y) #ajout de la position sur la map au robot
    ecrire_map("MapInGame.txt",map)


""" affiche matrice de la map dans le terminal """
def affiche_matrice(map):
    for i in range(map.l) :
        print(map.matrix[i])

#######################################################

"""
            GESTIONS DES ROBOTS
"""

""" liste les état des robot """
def etat_robot(robot):
    print("J",str(robot.__get_ident__()),":", robot.__get_name__(), "/ Points de vie:", robot.__get_battery__())


"""lire un fichier et recup première chaine"""
def lire(liste_robot):
    # BUT : recuperer toute les instruction des robot puis une liste
    # qui va servir a savoir qu'elle instruciton on n'a effectuer pour chaque rbt
    global liste_instruction
    global liste_instru_secours


    try :

        liste_instruction = ["0"]*len(liste_robot)
        pointeur_liste = ["0"]*len(liste_robot)

        liste_instru_secours =["0"]*len(liste_robot)


        #len(liste_robot) = nb de robot dans liste
        i=0
        while i < (len(liste_robot)):

            #on récupére le nom du fichier qui correspond au nom du robot + .txt
            #=> robot.txt
            name = (str(liste_robot[i].__get_name__())+str(".txt"))

            #fichier ou se trouve tous les robot stockés
            racine_du_fichier = "./progRobot/"+str(name)

            #ouverture du fichier du robot en mode lecture
            fichier = open(str(racine_du_fichier), "r")

            #init des liste vide
            liste_instruction[i]=[]
            pointeur_liste[i]=[]

            #récupération des instructions des différent robot INITIALISER
            # sous la forme : ["AL","TT PS FT","DD"]
            for ligne in fichier:
                line = ligne
                line = line.strip()
                liste_instruction[i].append(line)
                pointeur_liste[i].append("0")


            # a se stade nous avons la liste d'un robot
            # on va donc verifier si il a les conditions requise pour jouer

            # un robot dois avoir entre 6 et 21 pas dinstruction avec instru scr
            if len(liste_instruction[i]) <6 or len(liste_instruction[i]) >21 :
                # on le met pas dans la liste des robots

                liste_robot.pop(i)
                play.liste_robot = liste_robot

                # on suprime également le pointeur des intructions
                liste_instruction.pop(i)

                play.liste_instruction = liste_instruction

                pointeur_liste.pop(i)

                continue


            #je suprime un ele car instru de secours ne compte pas
            pointeur_liste[i].pop(0)
            fichier.close()
            i+=1




        return liste_instruction, pointeur_liste

    except FileNotFoundError: #traite l'erreur quand le fichier n'est pas trouvé
        print("le fichier n'a pas pue etre ouvert ou n'existe pas ")


"""fonction pour faire les intruction des différent robot"""
def RUN_robot(liste_robot,map):

    #tant que il y a un plus d'un robot en vie sur la map on lit les instruction de tous le monde

    global signal
    #instruction des robot a executé
    global liste_instruction
    global liste_instru_secours


    liste_instruction = lire(liste_robot)[0]
    #print(liste_instruction)

    # liste pour savoir qu'elle est la position de l'instruction a exécuter
    pointeur = lire(liste_robot)[1]

    # permiere instruction a exe tj la premiere
    # on met toute les premieres valeur de la liste pointeur a 1

    #on vas récupérer la liste des instruction de secours

    for robot in range(len(liste_robot)):
        liste_instru_secours[robot] = (liste_instruction[robot][0])
        # on suprime également l'instruction de secours de la liste_instruction
        liste_instruction[robot].pop(0)
        #play.liste_instruction = liste_instruction


    # print(liste_instru_secours)

    #verification si les instructions de secours sont valide

    # instru de secour peut etre AL, MI, IN, PS, FT

    liste_valide = ["AL","MI","IN","PS","FT"]

    for i in range(len(liste_instru_secours)):
        if liste_instru_secours[i] not in liste_valide :
            # Choisir un indice au hasard de la liste valide
            indice_aleatoire = random.randint(0, len(liste_valide)-1)
            liste_instru_secours[i] = liste_valide[indice_aleatoire]



    #on la premiere valeur a 1 car on commance tj du debut

    for robot in range(len(liste_robot)):
        pointeur[robot][0] = "1"


    #BUT : lire en boucle les instruction des robots tant qu'il on de la battery
    # et qu'il peuvent effectuer l'instruction demandé
    i = 0
    #liste_robot = play.liste_robot
    while i < (len(liste_robot)) and len(liste_robot) >= 2 and len(liste_robot) <= 6 :
        # check si robot n'est pas mort
        # dans le cas contraire on arrete de faire ces instructions
        global liste_robot_mort
        #liste_robot = play.liste_robot
        if (liste_robot[i].__get_name__() not in liste_robot_mort ):

            # parcour de la liste pour savoir qu'elle instruction a executé
            # si 1 alors c'est l'instruction correspondant a la position de j
            # dans pointeur[i][j]

            j=0
            while pointeur[i][j] != "1" :
                j+= 1

            #pour verifier que liste poinnteur -> print(pointeur)
            if pointeur[i][j]== "1" :
                application_instru(liste_robot[i],liste_instruction[i][j],map)

                #si on n'a signalé une collision avec une mine
                # REMPLACEMENT par l'instruction de secour
                if signal == 1 :
                    liste_instruction[i][j] = liste_instru_secours[i]

                    #print("REMPLACEMENT !!!!!")

                    #on remet le signal a 0
                    signal = 0


                pointeur[i][j] = "0"
                pointeur[i][(j+1)%len(liste_instruction[i])] = "1"

            i += 1

        # si dans liste instruction précédente non effectuer
        # implique de mettre a jour la liste des robot et des instruction a execute

        else :
            """le robot est dans la liste des mort"""

            """on le suprime de la map le robot"""

            # recup de ces coordonnées
            x = liste_robot[i].__get_pos_x__()
            y = liste_robot[i].__get_pos_y__()
            #del de la pos du rbt dans map
            map.__sup_ele_in_map__(x,y)


            """ on le suprime de la liste des robot"""
            """ qui doivent etre executer"""

            #méthode pop de la classe list pour retirer un élément précis
            #d'une liste. Cette méthode prend en argument l'index de l'élément à
            #retirer et renvoie la valeur de cet élément.

            liste_robot.pop(i)

            """ on suprime sont pointeur d'instruction"""

            pointeur.pop(i)

            liste_instruction.pop(i)

            """on passe au robot suivant"""

        # on attend que on n'a parcourue toute la liste des robot avant de remttre a jour la map
        if i == len(liste_robot) :
            # une fois que toute les instruction ont était faite
            # on met a jour la map
            affiche_mapingame("MapInGame.txt")


            #affiche l'état des robot et reset si les robot était invisible
            #parcourir liste des robot
            for j in range(len(liste_robot)) :
                etat_robot(liste_robot[j])
                liste_robot[j].set_invisible(0)

            #on attend xx secondes avant de faire autre chose
            #ici on attent la suite des instruction

            global time_for_instru
            time.sleep(time_for_instru)

            # on remet a zero on effectue un nouveau cycle
            i = i%len(liste_robot)



    #si on arrive ici c'est que il reste plus aucun ou 1 seul robot sur la map
    #on regarde si il reste un robot sur la map
    if len(liste_robot) == 1 :
        # on recup le robot
        winner = str(liste_robot[0].__get_name__())
        winner = winner.upper()
        print("le robot {",winner,"} a GAGNER !!!")

    #si il en reste pas on regarde la liste des mort
    elif len(liste_robot) == 0 :
        #le dernier ajouter gagne la partit
        winner = str(liste_robot_mort[-1])
        winner = winner.upper()
        print("le robot {",winner,"} a GAGNER !!!")

    #ne jeut jammais etre null car le premier robot a toujour la prio
    # sur son suivant

    # on pourrais régler ce cas avec du multi process
    # ou en regrdant la vie de chaque robot a l'instant t et prédire la prochaine
    # action des robots, si il perde la vie tous les deux alors match nul
    else :
        winner = "tous"
        print("MATCH NUL !!!")



    #fin de la game
    #afficher dans tkinter le vaiqueur
    #si le temps faire un classement
    msgbox = messagebox.showinfo("WINNER","Félicitations,{"+ winner +"} vous avez gagné!")

    return 1
    exit(1)



"""liste les différents fichiers contenus dans un répertoire"""
def lister_fichiers(dossier):
    # On commence par vérifier que le dossier existe bien
    if not os.path.exists(dossier):
        # Si le dossier n'existe pas, on affiche un message d'erreur
        print("Le dossier spécifié n'existe pas")
        return

    # On commence par lister tous les fichiers dans le dossier
    fichiers = os.listdir(dossier)

    # On initialise 1 liste pour stocker les fichiers txt
    fichiers_txt = []

    # On parcourt les fichiers un par un
    for fichier in fichiers:
        # Si le fichier se termine par .txt, on l'ajoute à la liste des fichiers txt
        if fichier.endswith(".txt"):
            fichiers_txt.append(fichier)

    return fichiers_txt



"""INITIALISATION des robot selectioner pour jouer"""
def liste_des_robot_a_init(liste_robot,battery,radar):

    for i in range(len(liste_robot)):

        liste_robot[i] = Robot(str(liste_robot[i]),battery,radar)

    return liste_robot

#######################################################


"""REGLAGE DE MAP"""
def init_map_random():
    # C'EST ICI QUE ON REGLE LES PARAMTETRE DE LA MAP
    """init de la map """
    # map JOUABLE de x*x

    global obstacle
    obstacle = play.obstacle
    maptest = Map(20,30,obstacle)
    maptest.ajouter_obstacle()
    maptest.retire_diagonale()

    return maptest

"""écriture et affichage de la map"""
def ecrire_afficher_map(map) :
    # BUT : simplifier l'init_all

    # ecrie la map dans le fichier pour simplifier la lecture dans terminal
    ecrire_map("MapInGame.txt",map)
    # idem mais l'affiche dans le terminal
    affiche_mapingame("MapInGame.txt")




# pour tester le programme dans terminal
"""init du projet en entier"""
def init_all():

    #recup de toute les var globals
    global battery
    global radar

    global liste_robot
    global liste_robot_mort
    global liste_instru_secours
    global liste_instruction

    global obstacle
    global map

    global time_for_instru


    """init de la map """
    map = init_map_random()

    #print(map)
    ecrire_afficher_map(map)

    """init des robot"""

    liste_robot = ["maxilef","anoupMK3","test"]
    # il faut pouvoir les selectionner dans partit graph
    liste_robot = liste_des_robot_a_init(liste_robot,battery,radar)

    """ajout des robot aléatoirement dans la map"""
    init_robot_in_map_alea(liste_robot,map)



    """ AJOUT DES ROBOT MANUELELEMENT
    ajouter_robot_in_map(map,liste_robot[0],5,3)
    ajouter_robot_in_map(map,liste_robot[2],5,7)
    ajouter_robot_in_map(map,liste_robot[1],5,5)
    """

    nombre_de_rb_init = len(liste_robot)

    """START DE LA GAME"""
    # map au départ des robots
    affiche_mapingame("MapInGame.txt")


    for i in range(len(liste_robot)):
        print(liste_robot[i].__get_name__())


    """lecture des instruction des robot"""
    RUN_robot(liste_robot,map)

    # FIN DE LA PARTIE
    exit(1)



#init_all()


#######################################################
