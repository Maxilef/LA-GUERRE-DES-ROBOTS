
class Robot:
    """class for robot."""
    _id = 0
    def __init__(self, nom, nrj, sonar): #image du robot

        self.name       = nom   # init du nom
        self.battery    = nrj   # init battery avec valeur compris entre 500 et 3000
        self.radar      = sonar # init de la porté du radar
        self.ident      = Robot._id #init de l'id du robot
        self.invisible  = 0 #permet de definir si le robot et detectable
        self.x = None
        self.y = None
        print("jouer créé :",nom, "/battery: ", nrj)
        Robot._id += 1


        if self.battery > 3000:
            self.battery = 3000
        elif self.battery < 0:    #A MODIF APRES TESTE 500 de base
            self.battery = 0


    #retoune les différents elements du robot
    def __get_name__(self):
        return self.name

    def __get_battery__(self):
        return self.battery

    def check_battery(self):
        if self.battery <= 0:
            print("Le robot{",self.__get_name__(),"} est mort!")

    def __get_radar__(self):
        return self.radar

    def __get_ident__(self):
        return self.ident

    def __get_invisible__(self):
        return self.invisible


    #retourne position x et y du robot
    def __get_pos_x__(self):
        return self.x

    def __get_pos_y__(self):
        return self.y



    # le robot connais sa position dans la map
    def __set_pos_robot__(self,posx,posy):
        self.x = posx
        self.y = posy


    #fait subir des degats
    def damage(self,damage):
        self.battery -= damage

    #ajouter de la battery
    def set_battery (self,nbajout):
        self.battery += nbajout

    def set_invisible(self,action):
        self.invisible = action

    #pas necessaire
    def attack_robot (self,target_robot):
        if (self.__get_ident__ != target_robot.__get_ident__):
            target_robot.damage(20)
            print(self.__get_name__(), "attaque", target_robot.__get_name__())



    # méthode pour changer l'arme du joueur
    def set_weapon(self, weapon):
        self.weapon = weapon

    #méthode pour verifier si le joueur a une arme
    def has_weapon(self):
        return self.weapon is not None
