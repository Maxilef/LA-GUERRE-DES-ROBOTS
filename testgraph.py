

###################################
##############IMPORT##############
#################################
from modele.map import Map
from modele.robot import Robot
import MAIN
import play
#import du dossier contenant toute les maps
from maps import *
import sys
import os
import shutil


"""from tkinter import """
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


#############################################
#              PARTIT GRAPHIQUE             #
#############################################





################GLOBAL#######################


# par defaut
robot_energy = play.battery
portee_radar = play.radar

map_obstacle = play.obstacle
speedvar = play.time_for_instru
#map par defaut
play.map = Map(1,1,0)

map = play.map

#liste_des_robot_a_init
boutons_coches = []


liste_robot = play.liste_robot

#############################################



###################
# pour LES IMAGES #
###################

"""reinitialiser une fenetre """
def reinitialiser_fenetre():
    global conteneur, canvas1, w, h
    # Supprimer tous les widgets du conteneur
    for widget in conteneur.winfo_children():
        widget.destroy()
    # Créer le bouton Précédent
    bouton_precedent = tk.Button(conteneur, text="Précédent", command=MENU)
    bouton_precedent.pack(side="bottom", anchor="se")

"""redimentionne l'image"""
def resize_image(canvas, image):
    # Récupérer les dimensions de l'objet Canvas
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Mettre à jour les dimensions de l'objet Image
    image.configure(width=canvas_width, height=canvas_height)

"""fenetre du MENU"""

#voulez_vous quiter
def quitter():
    global root
    #Création d'une fenêtre Toplevel de la fenêtre principale
    win = tk.Toplevel(root)
    win.geometry("250x250")

    #Demande confirmation pour quitter
    texteQuit = tk.Label(win, text = "Voulez-vous quitter ?")
    texteQuit.pack()

    #Boutons de choix
    buttonOui = tk.Button(win, text = "OUI, je quitte le jeu",command = root.destroy)
    buttonOui.pack()

    buttonNo = tk.Button(win, text = "NON",command = win.destroy)
    buttonNo.pack()

    win.mainloop()

#pour retourner sur la page du menu
def retour_MENU():
    global root
    root.destroy()
    MENU()


##########################################
#   FENETRE DE MENU                      #
##########################################
def MENU():

    global root
    root = tk.Tk() #Création fenêtre principale
    root.geometry("1000x500")
    root.title("LA GUERRE DES ROBOTS")


    #adapte la fenêtre au max de l'écran
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))


    # Rendre la fenêtre redimensionnable horizontalement et verticalement
    root.resizable(True, True)


    # Ajout d'une image sur toute la fenêtre
    bg = tk.PhotoImage(file = "robot1.png") #Fond d'écran d'accueil
    canvas1 = tk.Canvas(root, width = w,height = h)
    canvas1.create_image( 0, 0, image = bg,anchor = "nw")

    canvas1.pack(expand = 1, side = "top", fill = "both")


    # Utiliser la méthode bind pour exécuter la fonction resize_image chaque fois que la fenêtre est redimensionnée
    canvas1.bind("<Configure>", lambda event: resize_image(canvas1, bg))

    # Utiliser la variable MENU pour créer le widget Frame
    conteneur = tk.Frame(root)
    conteneur.pack(expand=True, fill="both",side="top")

    #impossible de mettre le fond d'un label transparent ?

    #création du titre
    # Création du label et ajout du texte "Mon texte"
    label = tk.Label(root, text="LA GUERRE DES ROBOTS", font=("Arial", 36), fg="orange", borderwidth=0,relief="flat",highlightthickness = 0,bg="#0073e6" )
    # Positionner le label en haut à droite du canvas
    label_canvas = canvas1.create_window(w/2, 10, anchor="n", window=label)

    #bouton play
    buttonPlay = tk.Button(root, text="PLAY",width = 25, height=3,command = selection_des_map ,bg = "orange")#Création du bouton PLAY
    buttonPlay.pack()
    buttonPlay_canvas = canvas1.create_window( 75, 175,anchor = "nw",window = buttonPlay)

    #bouton options
    buttonOptions = tk.Button(root, text="OPTIONS",width = 25, height=3,command = options,bg = "orange")#Création du bouton OPTIONS
    buttonOptions.pack()
    buttonOptions_canvas = canvas1.create_window( 75, 275,anchor = "nw",window = buttonOptions)

    #bouton exit
    buttonQuit = tk.Button(root, text="QUITTER",width = 25, height=3,command = quitter,bg = "orange")#Création du bouton QUITTER
    buttonQuit.pack()
    buttonQuit_canvas = canvas1.create_window( 75, 375,anchor = "nw",window = buttonQuit)



    canvas1.pack(expand = 1, side = "top", fill = "both")
    global ok
    ok = 0
    root.mainloop()



"""partit MAP tkinter"""

################################################################################
#           AFFICHAGE D'UNE MAP IN TKINTER                                     #
################################################################################

#retourne le nom de la map cliquer
def donne_la_map(nom_map,canvas,framecanv):

    #et crée la matrice correspondant a la maps
    matrice_map_prev = create_matrix_from_txt(str(nom_map)+".txt")

    #il faut maintenant instancier l'objet map
    # avec sa nouvelle matrice
    global map
    map.new_matrice(matrice_map_prev)
    play.map = map


    #puis on l'affiche dans le canvas
    canvas.delete(tk.ALL)
    play.affiche_matrice_in_tkinter(map.matrix,canvas)
    canvas.update()

#liste tous les fichier de la map dans canvas / pour selection de la map
def liste_fichiers_map(repertoire, frame,canvas,framecanv):
    # Récupérer la liste des fichiers dans le répertoire
    fichiers = os.listdir(repertoire)

    # Pour chaque fichier, créer une case à cocher et l'ajouter à la frame
    for fichier in fichiers:

        if fichier != "MapInGame.txt" :

            # Créer une case à cocher pour le fichier
            button = tk.Button(frame, text=fichier[:-4])
            button.pack(side="top",anchor="w",pady=3)
            button.config(command=lambda nom=button['text']: donne_la_map(nom,canvas,framecanv))


##########################################
#   fonction pour gérer selection MAP    #
##########################################
#crée une matrice a partit d'un fichier texte
def create_matrix_from_txt(txt_file):
  # ouvrir le fichier en mode lecture
  with open("./maps/"+str(txt_file), 'r') as f:
    # lire toutes les lignes du fichier dans une liste
    lines = f.readlines()

  # créer une liste vide pour stocker la matrice
  matrix = []

  # pour chaque ligne dans le fichier
  for line in lines:
    # supprimer les caractères de fin de ligne
    line = line.strip()
    # ajouter chaque caractère de la ligne à la matrice
    matrix.append([c for c in line])

  # retourner la matrice
  return matrix

#définie le nombre d'obstacle dans la game (si RANDOM)
def init_obstacle(event,canvas1):
    global map_obstacle, valeur_scale_obstacle
    play.obstacle = valeur_scale_obstacle.get()
    map_obstacle = play.obstacle

    print("la map a maintenant",map_obstacle,"d'obstacle")
    #une fois la valeur des obstacle def il faut affiché la preview de la map
    #on crée donc notre nouvelle maps

    global map
    map = creer_map_random()

    play.map = map
    #on l'affiche dans le canvas

    play.affiche_matrice_in_tkinter(map.matrix,canvas1)

#commande pour enlever le contenue du bouton libre
def clique(canvas,scrollbar,frame,canvasprev):
    #on enleve quoi qu'il arrive le canvas de la preview
    canvasprev.pack_forget()

    # Si le canvas est affiché, le cacher
    if canvas.winfo_ismapped() and canvasprev.winfo_ismapped():
        canvas.pack_forget()
        scrollbar.pack_forget()
        canvasprev.pack_forget()

    # Sinon, l'afficher
    else:
        #il faut enlever la frame avec la scale obstacle
        frame.pack_forget()

        # Ajout de la barre de défilement au canvas
        scrollbar.pack(side="left", fill="y")

        # Ajout du canvas à la fenêtre principale frame_map
        canvas.pack(side="left",fill="both")

        # Ajout du canvas à la fenêtre principale frame_map
        canvasprev.pack(side="right",expand=1,fill="both")

        #on affiche map a x obstacle
        global map
        map = creer_map_random()
        play.map = map
        play.affiche_matrice_in_tkinter(map.matrix,canvasprev)

#commande pour enlever le contenue du bouton random
def clique_for_random(frame,canvas,canvprev,map_obstacle_scale):


    # Si le frame est affiché, la cacher
    if frame.winfo_ismapped() and canvprev.winfo_ismapped():
        # on cache la frame la scale et la preview
        frame.pack_forget()
        map_obstacle_scale.pack_forget()
        canvprev.pack_forget()

    # Sinon, l'afficher
    else:

        #il faut enlever le canv des liste des maps
        canvas.pack_forget()

        # Ajout de la frame
        frame.pack(side = "left",padx=10)

        # Ajout de la barre de défilement au canvas
        map_obstacle_scale.pack(side = "top")

        # Ajout du canvas preview à la fenêtre principale frame_map
        canvprev.pack(side="right",expand=1,fill="both")

        #on affiche map a x obstacle
        global map
        map = creer_map_random()
        play.map = map
        play.affiche_matrice_in_tkinter(map.matrix,canvprev)

#crée une map random
def creer_map_random():
    global map_obstacle
    play.obstacle = map_obstacle

    #on initialise notre objet map de la class map
    global map
    map = MAIN.init_map_random()
    play.map = map
    #on l'affiche dans le terminal
    MAIN.ecrire_afficher_map(map)

    return map


##########################################
#   FENETRE DE LA Map                    #
##########################################
#page tkinter pour selection des map
def selection_des_map():

        global root

        #delete l'anciene fenetre
        root.destroy()

        #Création fenêtre pour map
        root = tk.Tk()
        root.title("CHOIX DE LA MAP")

        #adapte la fenêtre au max de l'écran
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d" % (w, h))

        root.configure(bg="#4851de")

        #ajustement de la map automatique
        if h > 1000 :
            play.cote = 35
        else :
            play.cote = 25



        """création de la frame pour le titre"""

        frame = tk.Frame(root,bg="#4851de")
        frame.pack(side="top",fill= "x")

        # Créer un label dans la frame
        label = tk.Label(frame, text="CHOIX DE LA MAP", font=("Arial", 26,"bold"), fg="orange", borderwidth=0,relief="groove",bg="#4851de")
        label.pack()


        """FRAME EN HAUT pour les boutons """
        #création de la frame_pour les btn
        frame_btn = tk.Frame(root,bg="#4851de")
        frame_btn.pack(side="top")

        # Créer un label au début de la frame de gauche
        labelbtn = tk.Label(frame_btn, text="choisissez un mode :",bg="#4851de",font=("Arial", 14))
        labelbtn.pack(side="top", anchor="w",expand = 1,fill ="x")



        """FRAME AU MILLIEU frame principale"""

        frame_map = tk.Frame(root,bg="#4851de")
        frame_map.pack(expand = 1,side = "top",fill= "both")




        # Création du canvas et de la barre de défilement

        canvas = tk.Canvas(frame_map,bg="#4851de")
        scrollbar = tk.Scrollbar(frame_map, orient="vertical", command=canvas.yview)

        # Configuration de la barre de défilement
        canvas.configure(yscrollcommand=scrollbar.set,bg="#4851de")

        # Création de la frame à faire défiler
        frame_liste = tk.Frame(canvas,bg="#4851de")

        # Créer un label au début de la frame de gauche
        labelmap = tk.Label(frame_liste, text="liste des maps disponibles :",bg="#4851de")
        labelmap.pack(side="top", anchor="n",expand = 1,fill ="x")



        # Ajout de la frame au canvas
        canvas.create_window((0,0), window=frame_liste, anchor="nw")

        """creation du canvas1 pour frame RANDOM"""
        #crée le canv de droite
        canvas1 = tk.Canvas(frame_map,bg="#4851de")


        # Création de plusieurs boutons de sélection dans la frame
        liste_fichiers_map("./maps", frame_liste,canvas1,frame_map)


        # Mise à jour de la vue du canvas
        frame_liste.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


        """afficher la map dans le canv de droite"""

        #si on a pas Appuyer sur random_x

        #crée une frame a droite pour mettre scale pourcentage obstacles
        frame_scale = tk.Frame(frame_map,bg="#4851de",width= w/2, height= h/1.5)


        #scale pour obstacle d'est qu'il est relaché map->canvas
        """scale obstacle"""
        global map_obstacle
        map_obstacle_scale = tk.Scale(frame_scale, orient='horizontal', from_=0, to=20, #Scale pour choisir l'énergie des robots
          resolution=1, tickinterval=2,bg="#4851de",troughcolor="orange", length = w/3,label="choisissez un pourcentage d'obstacle dans la map:")


        # Créez une variable Tkinter qui stockera la valeur de la barre de défilement
        global valeur_scale_obstacle
        valeur_scale_obstacle = tk.IntVar()


        # Liez la variable Tkinter à la barre de défilement
        map_obstacle_scale.config(variable= valeur_scale_obstacle)

        # Liez la fonction pour init obstacle à la barre de défilement
        map_obstacle_scale.bind("<ButtonRelease-1>", lambda event: init_obstacle(event,canvas1))

        # Creation des bouton LIBRE ET RAMDOM
        button_libre = tk.Button(frame_btn, text="LIBRE",width=10,bg="orange", height=1,command= lambda : clique(canvas,scrollbar,frame_scale,canvas1))
        button_random = tk.Button(frame_btn, text="RANDOM",width=10,bg="orange", height=1,command= lambda : clique_for_random(frame_scale,canvas,canvas1,map_obstacle_scale))

        # Pack des bouton dans FRAME en dessou le titre
        button_libre.pack(side="left", padx=40,pady=15,anchor="n")
        button_random.pack(side="left", padx=40,pady=15,anchor="n")



        """ FRAME EN BAS"""
        #création de la frame_pour les btn prev et suiv
        frame_btn_back = tk.Frame(root,bg="#4851de")
        frame_btn_back.pack(side = "bottom",fill= "x")

        # Creation des bouton retour et suivant
        button_prev = tk.Button(frame_btn_back, text="< précédent",width=10, height=1,command = retour_MENU,bg="red",fg="white")
        button_next = tk.Button(frame_btn_back, text="suivant >",width=10, height=1,command = selection_des_robots,bg="green",fg="white")

        # Pack the buttons in the frame
        button_prev.pack(side="left",anchor="w")
        button_next.pack(side="right",anchor="e")

        root.mainloop()




"""partit robot tkinter"""
#######################
# INIT PARAMETRE ROBOT#
#######################
def init_nrj(event):
    global robot_energy, valeur_scale_nrj
    robot_energy = valeur_scale_nrj.get()
    play.battery = robot_energy
    print("les robot on maintenant",robot_energy,"d'énergie")

def init_radar(event):
    global portee_radar,valeur_scale_radar
    portee_radar = valeur_scale_radar.get()
    play.radar = portee_radar
    print("les robot on maintenant",portee_radar,"de porté avec leur radar")

##########################################
#   fonction pour gérer selection robot  #
##########################################
# Créer une fonction de callback pour le clic sur un bouton
def callback(nom_bouton):
    # Ajouter le nom du bouton à la liste des boutons cochés
    global boutons_coches
    if nom_bouton not in boutons_coches:
        if len(boutons_coches)<6:
            boutons_coches.append(nom_bouton)

        else :
            print("La limite de sélection est atteinte.")
    elif nom_bouton in boutons_coches:
        boutons_coches.remove(nom_bouton)

    #print(boutons_coches)

#liste tous les fichier du repertoire ou sont stocké les robots
def liste_fichiers(repertoire, frame):
    # Récupérer la liste des fichiers dans le répertoire
    fichiers = os.listdir(repertoire)

    # Pour chaque fichier, créer une case à cocher et l'ajouter à la frame
    for fichier in fichiers:

        #recup seulement le nom des robtos
        nom_robot = fichier[:-4]

        # Créer une case à cocher pour le fichier
        checkbutton = tk.Checkbutton(frame, text=nom_robot,bg="orange")
        checkbutton.pack(side="top",anchor="w",pady=3)
        checkbutton.config(command=lambda nom=checkbutton['text']: callback(nom))
        checkbutton.configure(font=("Arial", 16), pady=4)


####################################
#la FENETRE de selection des robots#
####################################
def selection_des_robots():

        #mettre a zero liste des robots
        global boutons_coches
        boutons_coches = []

        global root
        #delete l'anciene fenetre

        root.destroy()

        #Création fenêtre pour map
        root = tk.Tk()
        root.geometry("1000x500")
        root.title("CHOIX DES ROBOTS")

        #adapte la fenêtre au max de l'écran
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d" % (w, h))

        root.configure(bg="#4851de")


        """création de la frame pour le titre"""

        frame = tk.Frame(root,bg="#4851de")
        frame.pack(side="top",fill= "x")

        # Créer un label dans la frame
        label = tk.Label(frame, text="CHOIX DES ROBOTS", font=("Arial", 26,"bold"), fg="orange", borderwidth=0,relief="groove",highlightthickness = 0,bg="#4851de")
        label.pack()


        """FRAME AU MILLIEU"""
        frame_rbt = tk.Frame(root,bg="#4851de")
        frame_rbt.pack(expand = 1,side = "top",fill= "both")

        #creer un bouton pour validé et récuperer la liste des robot select




        """frame dans canvas a gauche pour afficher la liste des robots """

        # Création du canvas et de la barre de défilement
        canvas = tk.Canvas(frame_rbt,bg="#4851de")
        scrollbar = tk.Scrollbar(frame_rbt, orient="vertical", command=canvas.yview)

        # Configuration de la barre de défilement
        canvas.configure(yscrollcommand=scrollbar.set)


        # Ajout de la barre de défilement au canvas
        scrollbar.pack(side="left", fill="y")


        # Ajout du canvas à la fenêtre principale frame_rbt
        canvas.pack(side="left",fill="both")


        # Création de la frame à faire défiler
        frame_liste = tk.Frame(canvas,bg="#4851de")

        # Créer un label au début de la frame de gauche
        labelrobot = tk.Label(frame_liste, text="liste des robots disponibles :",bg="#4851de",font=("Arial", 16))
        labelrobot.pack(side="top", anchor="n",expand = 1,fill ="x")


        # Ajout de la frame au canvas
        canvas.create_window((0,0), window=frame_liste, anchor="nw")


        # Création de plusieurs boutons de sélection dans la frame
        liste_fichiers("./progRobot", frame_liste)


        # Mise à jour de la vue du canvas
        frame_liste.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))




        """frame a droite pour les parametre des robots"""

        frame_scale = tk.Frame(frame_rbt,bg="#4851de",width= w/2, height= h/2)
        frame_scale.pack(side = "right",padx=10,anchor="n")

        # Créez les barres de défilement dans la frame

        """scale nrj rbt"""
        global robot_energy
        robot_energy_scale = tk.Scale(frame_scale, orient='horizontal', from_=500, to=3000, #Scale pour choisir l'énergie des robots
          resolution=1, tickinterval=500, length = w/2,label="Energie des robots :",bg="#4851de",troughcolor="orange")
        robot_energy_scale.pack(side = "top",anchor="n",pady=50,padx="150")

        # Créez une variable Tkinter qui stockera la valeur de la barre de défilement
        global valeur_scale_nrj
        valeur_scale_nrj = tk.IntVar()

        # Liez la variable Tkinter à la barre de défilement
        robot_energy_scale.config(variable= valeur_scale_nrj)

        # Liez la fonction pour init l'nrj des robots à la barre de défilement
        robot_energy_scale.bind("<ButtonRelease-1>", init_nrj)


        """scale radar rbt"""
        global portee_radar
        portee_radar_scale = tk.Scale(frame_scale, orient='horizontal', from_=2, to=6,        #Scale pour choisir l'énergie des robots
          resolution=1, tickinterval=1, length = w/2,label="porté du radar :",bg="#4851de",troughcolor="orange")
        portee_radar_scale.pack(side = "top",anchor="n",pady=35,padx="150")

        # Créez une variable Tkinter qui stockera la valeur de la barre de défilement
        global valeur_scale_radar
        valeur_scale_radar = tk.IntVar()

        # Liez la variable Tkinter à la barre de défilement
        portee_radar_scale.config(variable= valeur_scale_radar)

        # Liez la fonction pour init l'nrj des robots à la barre de défilement
        portee_radar_scale.bind("<ButtonRelease-1>", init_radar)


        """ FRAME EN BAS"""
        #création de la frame_pour les btn prev et suiv
        frame_btn_back = tk.Frame(root,bg="#4851de")
        frame_btn_back.pack(side = "bottom",fill= "x")

        # Create the buttons
        button_prev = tk.Button(frame_btn_back, text="< précédent",bg="red",fg="white",width=10, height=1,command = selection_des_map)
        button_next = tk.Button(frame_btn_back, text="suivant >",width=10, height=1,bg="green",fg="white",command = init_for_play)

        # Pack the buttons in the frame
        button_prev.pack(side="left",anchor="w")
        button_next.pack(side="right",anchor="e")



        root.mainloop()

"""intermediaire entre selection robot et jeux"""
def init_for_play():
    #on recup se qu'on a besoin pour init les robots
    global boutons_coches

    global robot_energy
    global portee_radar
    global map

    #on instancie les objet robot
    play.liste_robot = MAIN.liste_des_robot_a_init(boutons_coches,robot_energy,portee_radar)

    """ajout des robot aléatoirement dans la map"""
    MAIN.init_robot_in_map_alea(play.liste_robot,map)

    #on ouvre la fenetre PLAY
    JEUX()


"""partit JEUX"""



####################################
#la FENETRE de JEUX                #
####################################
def JEUX():

    global map
    global liste_robot
    liste_robot = play.liste_robot
    map = play.map
    global root
    #delete l'anciene fenetre

    root.destroy()

    #Création fenêtre pour map
    root = tk.Tk()
    root.title("JEUX")

    #adapte la fenêtre au max de l'écran
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))

    root.configure(bg="#4851de")
    """création de la frame pour le titre"""

    frame = tk.Frame(root,bg="#4851de")
    frame.pack(side="top",fill= "x")

    # Créer un label dans la frame
    label = tk.Label(frame, text="JEUX !", font=("Arial", 26,"bold"), fg="orange", borderwidth=0,relief="groove",highlightthickness = 0,bg="#4851de")
    label.pack()



    #frame au MILLIEU geante pour prendre tous les widget

    frame_h = tk.Frame(root,bg="#4851de",height= h/1.5)
    frame_h.pack(side="top",fill= "both",expand = 1 )



    #faire une frame a gauche pour historique de la partit

    frame_gauche = tk.Frame(frame_h,bg="white",width= w/2.5)
    frame_gauche.pack(side="left",fill="y",expand = 1,anchor = "w",padx=20,pady=5)

    # Créer un label au début de la frame de gauche
    history_label = tk.Label(frame_gauche, text="Historique des actions :",bg="white")
    history_label.pack(side="top", anchor="n",expand = 1,fill ="x")

    #création d'une frame pour mettres les états des robots dans la frame de gauche
    test = tk.Frame(frame_gauche,bg="#4851de")
    test.pack(side="bottom")


    #on crée les label pour afficher vie des robots
    robots = play.liste_robot

    #on va mainteant crée pour chaque robot un label
    play.robot_labels = []
    for robot in robots:
        label = tk.Label(test, text=f"{robot.__get_name__()} / Points de vie: {robot.__get_battery__()}",bg="orange")
        label.pack(pady=3,anchor="w")
        play.robot_labels.append(label)


    # Créer un canvas dans la frame
    map_canvas = tk.Canvas(frame_h, bg="#4851de", width= w/1.5, height=  h/1.5 )
    map_canvas.pack(side="right", fill="both",padx = 20,pady= 5)
    play.canvasforgame = map_canvas

    #affiche la map dans le canvas avec init des robots aléatoir pour le moment

    play.affiche_matrice_in_tkinter(map.matrix,map_canvas)

    #faire un bouton START
    start_button = tk.Button(frame_gauche, text="Start",bg="green",fg="white",command= lambda : MAIN.RUN_robot(liste_robot,map))
    start_button.pack(side="top",pady=10)

    frame_b = tk.Frame(root,bg="green")
    frame_b.pack(side="bottom",fill= "x")


    """ FRAME EN BAS"""
    #création de la frame_pour les btn prev et suiv
    frame_btn_back = tk.Frame(root,bg="#4851de")
    frame_btn_back.pack(side = "bottom",fill= "x")


    # Create the buttons
    button_prev = tk.Button(frame_btn_back, text="< précédent",bg="red",fg="white",width=10, height=1,command = selection_des_robots)

    #remetre a zero la liste des robot initilaiser
    #il faut les enlever de la map


    # Pack the buttons in the frame
    button_prev.pack(side="left",anchor="w")


    root.mainloop()



"""partit OPTIONS"""

#################
# INIT VITESSE GAME
#################
#met a jour la vitesse d'une partit
def init_speed(event):

    global speedvar, valeur_vitesse_game
    speedvar = valeur_vitesse_game.get()
    play.time_for_instru = speedvar
    print("La vitesse de la partie est de :",speedvar,"secondes")
#################
#permet d'importer une map
def import_map():
    global map_file
    #On récupère le chemin de la map
    map_file = tk.filedialog.asksaveasfilename(initialdir="/",title="Choisir un fichier")
    #On déplace le fichier de la map dans le répertoire ./maps
    shutil.move(map_file,"./maps")

#permet d'importer un robot
def import_robot():
    global robot_file
    #On récupère le chemin de la map
    robot_file = tk.filedialog.asksaveasfilename(initialdir="/",title="Choisir un fichier")
    #On déplace le fichier de la map dans le répertoire ./maps
    shutil.move(map_file,"./progRobot")

####################################
#la FENETRE des options            #
####################################
def options():
    """Fonction si on clique sur les options"""
    global root

    #On détruit l'ancienne fenêtre
    root.destroy()
    #On crée une nouvelle fenêtre
    root = tk.Tk()
    root.title("OPTIONS")


    #adapte la fenêtre au max de l'écran
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))

    root.configure(bg="#4851de")


    """création de la frame pour le titre"""
    frame = tk.Frame(root,bg="#4851de")
    frame.pack(side="top",fill= "x")

    # Créer un label dans la frame
    label = tk.Label(frame, text="OPTIONS ", font=("Arial", 26,"bold"), fg="orange", borderwidth=0,relief="groove",highlightthickness = 0,bg="#4851de")
    label.pack()



    """scale radar rbt"""
    global speedvar
    #Scale pour choisir l'énergie des robots
    vitesse_game_scale = tk.Scale(frame, orient='horizontal', from_=0, to=2,
      resolution=0.01, tickinterval=0.2, length = w/2,label="choix vitesse de la game :",bg="#4851de",troughcolor="orange")
    vitesse_game_scale.pack(side = "left",anchor="n",pady=35,padx="150")

    # Créez une variable Tkinter qui stockera la valeur de la barre de défilement
    global valeur_vitesse_game
    valeur_vitesse_game = tk.IntVar()

    # Liez la variable Tkinter à la barre de défilement
    vitesse_game_scale.config(variable= valeur_vitesse_game)

    # Liez la fonction pour init l'nrj des robots à la barre de défilement
    vitesse_game_scale.bind("<ButtonRelease-1>", init_speed)

    button_import_map = tk.Button(root, text="+ Import map",width=10, height=1,command = import_map ,bg="blue",fg="white")#Bouton pour importer une map
    button_import_map.pack(side = "left",anchor="nw")

    button_import_robot = tk.Button(root, text="+ Import robot",width=10, height=1,command = import_robot ,bg="blue",fg="white")#Bouton pour importer une map
    button_import_robot.pack(side = "left",anchor="nw")



    """ FRAME EN BAS"""
    #création de la frame_pour les btn prev et suiv
    frame_btn_back = tk.Frame(root,bg="#4851de")
    frame_btn_back.pack(side = "bottom",fill= "x")

    # Create the buttons
    button_prev = tk.Button(frame_btn_back, text="< précédent",width=10, height=1,command = retour_MENU,bg="red",fg="white")


    # Pack the buttons in the frame
    button_prev.pack(side="bottom",anchor="w")

    root.mainloop()





ok = 1
if ok == 1 :
    MENU()
