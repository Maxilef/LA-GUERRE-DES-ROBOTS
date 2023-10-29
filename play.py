#prend toute les variables globals pour tout le monde
import tkinter as tk
import sys
from PIL import Image, ImageTk


#############################################
#    PARTIT GESTIONS  GAME/AFFICHAGE        #
#############################################

#on gére ici les variables qui vont s'échanger entre
# l'interface et le programme qui gére les robots

#on gére aussi l'affichage tkinter de la partit ici pour éviter
#une importation circulaire


################GLOBAL#######################

#robots
battery = 3000
radar = 4

#liste vide des robot que l'on vas faire jouer
liste_robot = []


#map
obstacle = 0
map = []

#vitesse de la partit
time_for_instru = 0.1

#tkinter
#on stack des label ici pour les états des robots dans tkinter
robot_labels = []

#transmettre le canvas pour reset et affiché la map en boucle
canvasforgame = 0

#definie la taille d'un carré pour l'affichage de la matrice

cote = 25

liste_de_couleur=["blue","magenta","orange","purple","cyan","yellow"]

#############################################

"""partit de la gestion de jeux"""

###########################
# FONCTION AFFICHAGE JEUX #
###########################


#affiche la map dans le canvas a l'aide de sa matrice
def affiche_matrice_in_tkinter(matrice,canvas):

    """but afficher dans le canvas la matrice sous forme de carre/rectangle"""
    if matrice != [] :

        x = 0
        y = 0
        #print(matrice)
        ligne = len(matrice)
        colone = len(matrice[0])


        for i in range(ligne):
            #x = 0
            for j in range(colone):
                #libre
                coul = "white"
                #un mur
                if matrice[i][j] == "#" :
                    coul = "black"

                #mine
                elif isinstance(matrice[i][j], tuple) :
                    coul = "red"

                #un robot
                elif isinstance(matrice[i][j], int):
                    coul = liste_de_couleur[matrice[i][j]]


                #les tirs
                elif matrice[i][j] == "^" :
                    coul = "green"

                elif matrice[i][j] == "v" :
                    coul = "green"

                elif matrice[i][j] == "<" :
                    coul = "green"

                elif matrice[i][j] == ">" :
                    coul = "green"

                creer_rect(canvas,x,y,cote,coul)
                x = (x + cote) % (cote*colone)
            y += cote

"""
imageroche = tk.PhotoImage(file="1rock.png")
#crée des rectangles dans le canvas/ fait la map dans canvas
def creer_rect(canv ,x , y , cote,coul) :
    global imageroche
    if (coul == "black") :

        canv.create_rectangle( x, y, x+cote, y+cote,fill=coul)
        #canv.create_image(x, y, image=image)
        canv.create_image(x, y, anchor="nw", image=imageroche)
    else:
        canv.create_rectangle( x, y, x+cote, y+cote,fill=coul)"""


def creer_rect(canv ,x , y , cote,coul) :
    canv.create_rectangle( x, y, x+cote, y+cote,fill=coul)


#fonction pour actiliser dans tkinter la fenetre de jeux
#lorsque le jeu tourne dans le terminal en meme temps on met a jour la fenetre
#tkinter JEUX
def RUN_GAME(canvasforgame) :

    #on vas reset et affiché le canvas qui crée la map a chaque fois qu'on l'écrie
    #dans le programme principale (MAIN.py)

    #on delete de ce su'il y a dans le canvas

    global map


    canvasforgame.delete(tk.ALL)

    #c'est le fichier que on veut afficher

    #on l'affiche a nouveau et on l'update
    affiche_matrice_in_tkinter(map.matrix,canvasforgame)
    canvasforgame.update()

    #on update aussi la vie des robots
    global liste_robot, robot_labels
    robots_update_bat_tk(liste_robot,robot_labels)


#on vas update tous les robots ne même temps
def robots_update_bat_tk(liste_robot,robot_labels):
    #test est un label

    robots = liste_robot

    for i, robot in enumerate(robots):
        update_labels(robot, robot_labels)


#update la vie d'un robot dans son labels associé
def update_labels(robot,robot_labels):
    for label in robot_labels:
        if label["text"].startswith(f"{robot.__get_name__()}"):
            label.config(text=f"{robot.__get_name__()} / Points de vie: {robot.__get_battery__()}",bg=liste_de_couleur[robot.__get_ident__()])
