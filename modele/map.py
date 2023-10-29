from modele import robot
import random

class Map :
    """
    class de la map avec comme attribut le nom de la map, le nombre de colones et de lignes
    """
    def __init__(self, ligne , colone,obstacle): #carte par defaut 30*20 #max obstacle = 20 %

        # on ajoute 2 à la taille de la carte pour ajouter des murs tout autour
        ligne = ligne +2
        colone = colone +2

        self.l = ligne
        self.c = colone
        self.pourcentage_obstacles = obstacle

        #map de 20*30 donc on s'assure de ne jamais etre au dessu + les mur
        if self.l > 22 :
            self.l = 22
        if self.c > 32 :
            self.c = 32

        # on s'assure que le pourcentage d'obstacles est valide
        if self.pourcentage_obstacles > 20:
            self.pourcentage_obstacles = 20
        elif self.pourcentage_obstacles < 0:
            self.pourcentage_obstacles = 0

        # on calcule le nombre maximal d'obstacles possible
        self.nb_obstacles_max = self.l * self.c * (self.pourcentage_obstacles / 100)

        # on initialise la carte avec aucun obstacle
        mat=[]
        for i in range(ligne):
            col = []
            # empli une ligne
            for j in range(colone):
                # pour la premiere et la derniere ligne que des # (MUR)
                if i == 0 or i == ligne-1:
                    col.append('#')

                #colone
                elif j == 0 or j== colone-1:
                    col.append('#')

                else :
                    col.append('_')
            mat.append(col)
        self.matrix=mat
    """"""

    """changer la matrice de la map par une autre"""
    def new_matrice(self,new_mat):
        self.matrix = new_mat

    """ajouter obstacle alea"""
    def ajouter_obstacle(self):

        # on vérifie qu'il reste des obstacles à ajouter
        while self.nb_obstacles_max > 0:
            # on génère des coordonnées aléatoires pour l'obstacle
            x = random.randint(1, self.l - 2)
            y = random.randint(1, self.c - 2)

            # on ajoute l'obstacle à la carte
            self.matrix[x][y] = "#"
            self.nb_obstacles_max -= 1


    """retourne si il y a une diagonal dans map"""
    def est_diagonale(self, x, y):
        """
        avec x, y la position en haut à gauche
        renvoie True si:
            |#_| ou |_#|
            |_#|    |#_|
        """
        symboles = str(self.matrix[x][y]) + str(self.matrix[x][y+1]) + str(self.matrix[x+1][y]) + str(self.matrix[x+1][y+1])
        return (symboles == '#__#') or (symboles == '_##_')


    """charche si diagonal"""
    def retire_diagonale(self):

        """
        il faut interdir le motif :
         _#         ou #_
         #_            _#
        """

        X = self.l -1
        Y = self.c -1

        continuer = True
        while(continuer):
            continuer = False
            for x in range(X-1):
                for y in range(Y-1):

                    if self.est_diagonale(x, y):
                        continuer = True
                        self.correction(x, y)


    """on modifie la map si on trouve une diagonal"""
    def correction(self, x, y):
        #cas :
        # |#_|
        # |_#|

        #si # alors on choisi soit d'en ajouter un en haut ou en bas ex : |##|
        #                                                                 |_#|
        if self.matrix[x][y] == '#':
            if random.randrange(2)%2:
                # on ajoute un mur
                if random.randrange(2)%2:
                    # en haut
                    self.matrix[x][y+1] = '#'
                else:
                    # en bas
                    self.matrix[x+1][y] = '#'

            #l'inverse
            else:
                # on retire un mur
                if random.randrange(2)%2:
                    # en haut
                    self.matrix[x][y] = '_'
                else:
                    # en bas
                    self.matrix[x+1][y+1] = '_'

        # |_#|
        # |#_|
        else:
            if random.randrange(2)%2:
                # on ajoute un mur
                if random.randrange(2)%2:
                    # en haut
                    self.matrix[x][y] = '#'
                else:
                    # en bas
                    self.matrix[x+1][y+1] = '#'
            else:
                # on retire un mur
                if random.randrange(2)%2:
                    # en haut
                    self.matrix[x][y+1] = '_'
                else:
                    # en bas
                    self.matrix[x+1][y] = '_'


    """recupere ce qu'il y a dans une case donné"""
    def __get_position__(self,x,y):
        return self.matrix[x][y]


    """permet de mettre un robot sur la map"""
    def __set_robot_in_map__(self,robot,x,y) :
        if self.__get_position__(x,y) == '_' :
            self.matrix[x][y] = (robot.__get_ident__())
        else :
            print ("ERROR: place deja occupé \n\t-Impossible de mette a jour le robot {",robot.__get_name__(),"}")


    """suprimer un robot"""
    def __sup_ele_in_map__(self,x,y) :
        self.matrix[x][y] = '_'


    """ajouter une mine sur la map"""
    def __set_mine_in_map__(self,robot,x,y) :
        if self.__get_position__(x,y) == '_' :
            ajout = ("X",robot.__get_ident__())
            self.matrix[x][y] = ajout

        """#si il y a un robot on l'ajoute pas mais le robot perd de la battery
        elif self.__get_position__(x,y) == int:

            #metre des dommage a robot
            #trouver soution pour savoir a quel robot on met des degats """

    def __set_tir_in_map__ (self,tir,x,y) :
        if self.__get_position__(x,y) == '_' :
            ajout = tir
            self.matrix[x][y] = str(ajout)
