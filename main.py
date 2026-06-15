# -*- coding: utf-8 -*-
"""
Created on 12/02/2026

@author: Hugo
"""

import json
import pyxel
from settings import WIDTH, HEIGHT, FICHIER_COLL, TILESIZE
#from tilemap import player_skin



pyxel.init(WIDTH, HEIGHT, fps=30,title="Vergatura and the forgotten Library")#,display_scale=5 #possibilité de rajouté un dézoom 


pyxel.load("2.pyxres")

liste_state_game = ["InGame", "Backpack"]


class Game:
    def __init__(self, player):
        """Classe qui gère comment le jeu fonctionne"""
        self.state_game = "InGame"
        self.pause = False
        self.debug = False
        self.centred = True
        self.list_name_obj = ["wall", "invisible_wall"]
        self.name_obj_collision = "wall"

        #initialisation du player
        self.player = player
        
        self.list_collisions = self.reading_save(FICHIER_COLL)

        self.id_option = 0
        
        self.text_to_draw = []

        self.origin_point = [0,0]
        self.modification_map = False
    
    
    def choice_option(self, option:dict):
        """affiche les options des menus parmi la liste 'option'
        option: un dictionnaire contenant l'ensemble des réponses possibles"""
        assert type(option) == dict, "erreur d'option"
        for i in range(len(option)):
            pyxel.text(20, 20+10*(i+1), option[i], 6)
        
        pyxel.text(10, 20+10*(self.id_option+1), "->", 8)
        
        if self.update_menu(option):
            if self.id_option == 0:
                self.pause = False
            elif self.id_option ==1:
                pass
            elif self.id_option ==2:
                print(self.player.numero_skin)
                self.player.change_skin()
                print(self.player.numero_skin)




            
    def update_menu(self, option):
        """update l'id de l'option à choisir
        permet de choisir quelle option choisir avec les touches haut bas
        option: dictionnaire des options possibles
        OUT: True si entrée pressée et False sinon """
        
        if pyxel.btnp(pyxel.KEY_UP):
            if self.id_option -1 < 0:
                self.id_option = len(option)-1
            else:
                self.id_option -= 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            if self.id_option >= len(option)-1:
                self.id_option = 0
            else:
                self.id_option +=1
                
        if pyxel.btnp(pyxel.KEY_RETURN):
            return True
        else:
            return False


    def draw_menu_pause(self):
        """dessine le menu pause"""
        option = {0:"Continuer" ,1:"Aide", 2:"Changer skin"}
        self.choice_option(option)
        
        
    def update(self):
        """ update de la classe Game
        gère la pause
        le sac à dos,
        la modif de map
        TODO:la carte du jeu
        """
        if pyxel.btnp(pyxel.KEY_P):
            if self.pause == False:
                self.pause = True
            else:
                self.pause = False
                
        if pyxel.btnp(pyxel.KEY_TAB):
            #TODO: activation of the backpack
            if not self.pause and self.state_game == "InGame":
                self.state_game = "Backpack"
            else:
                self.state_game = 'InGame'
        #------------------------------------------------------------------------------------
        #outils de construction de map
        if pyxel.btnp(pyxel.KEY_M):
            if self.modification_map ==False:
                pyxel.mouse(True)
                self.debug = True
                self.modification_map = True
            else:
               pyxel.mouse(False)
               self.debug = False
               self.modification_map = False 


        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.modification_map:
            i=0
            stop = False
            while i < len(self.list_name_obj) and stop == False:
                if self.list_name_obj[i] == self.name_obj_collision:
                    if len(self.list_name_obj) > i+1:
                        self.name_obj_collision = self.list_name_obj[i+1]
                        
                    else:
                        self.name_obj_collision = self.list_name_obj[0]
                    stop = True
                i+=1
            print(self.name_obj_collision)

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.modification_map:
            if self.centred == True:
                self.add_element([pyxel.mouse_x-pyxel.mouse_x%TILESIZE-player.cam_x , pyxel.mouse_y - pyxel.mouse_y%TILESIZE -player.cam_y], FICHIER_COLL,self.name_obj_collision)
            else:
                self.add_element([pyxel.mouse_x-player.cam_x,pyxel.mouse_y-player.cam_y], FICHIER_COLL,self.name_obj_collision)
        
   

    def draw(self):
        """méthode draw de la class Game
        affiche:
            les murs normaux
            les murs invisibles

        """
        #affiche les différents éléments ayant une collision
        for tab in self.list_collisions["wall"]:
            if self.debug == True:
                pyxel.rectb(tab[0]+player.cam_x, tab[1]+player.cam_y, TILESIZE,TILESIZE, 2)
            else:
                pyxel.blt(tab[0]+player.cam_x, tab[1]+player.cam_y, 0, 72, 104, 8, 8, colkey=2)
        
        for tab in self.list_collisions["invisible_wall"]:
            if self.debug == True:
                pyxel.rectb(tab[0]+player.cam_x, tab[1]+player.cam_y, TILESIZE,TILESIZE, 7)
            # else:
            #     pyxel.blt(tab[0]+player.cam_x, tab[1]+player.cam_y, 0, 72, 104, 8, 8, colkey=2)
        
        
        if self.modification_map==True:
            pyxel.blt(pyxel.mouse_x-pyxel.mouse_x % TILESIZE, pyxel.mouse_y - pyxel.mouse_y % TILESIZE, 0, 8, 120, 8, 8, colkey=2)
            
        
    def draw_text(self):
        """affiche le texte contenu"""
        # TODO: ajouter une tête qui montre qui parle
        
        if len(self.text_to_draw) != 0:
            pyxel.text(10, 100, str(self.text_to_draw[0]), 7)
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.text_to_draw = self.text_to_draw[1:]
                
    def add_text(self, text=str, spliting_object="~"):
        """ 
        -text: text you want to print type:str
        -splitting_object: str of the caracter that allow the return 
        split the text receive multiple version, split by the '~' 
        and print it on the terminal"""
        # TODO: rajouter des sécurités pour éviter de mettre n'importe quoi
        #TODO: synthétiser
        assert type(text) == str, "le type de l'objet n'est pas str"
        lines = []
        new_repere = 0
        for i in range(len(text)):
            if text[i] == spliting_object and i != 0:
                lines.append(text[new_repere:i])
                new_repere = i +1

        for elem in lines:
            self.text_to_draw.append(elem)

        return lines
            
    
        
    def change_name_obj_collision(self, new_name=str):
        """change l'objet que tu rajoutes/enlève de la tilemap"""
        self.name_obj_collision = new_name
            
    
    def add_element(self, position, filename, type_obj='wall'):
        """position: the coordinate of the object
        filename: the name of the filewe want to add element
        type_obj: the name of the object you want to add"""
     # TODO: a modifier pour pouvoir avoir différents walls différents  
        
        if filename == FICHIER_COLL:
            self.list_collisions = self.reading_save(filename)#on met à jour tout le fichier de collision
            
            if type_obj in self.list_collisions.keys():

                if position not in self.list_collisions[type_obj]:
                    self.list_collisions[type_obj].append(position)

                else:
                    self.list_collisions[type_obj].remove(position)
                # elif type_obj == "invisible_wall":
            else:
                self.list_collisions[type_obj] = [position]

                
            
                    
            
            self.save(FICHIER_COLL, self.list_collisions)#on sauvegarde les changements
            
    
    
    def save(self, name, chose_dump):
        """save chose_dump into the file that begin with name
        name: the name of the save, without the '.json' """
        filename = str(name)+".json"
        
        print('sauvegarde en cour')
        with open(filename ,"w") as fichier:
            json.dump(chose_dump, fichier)
            return fichier
            

    def reading_save(self, name):
        """loading of the save"""
        filename = str(name)+".json"
        
        try:
            # if there is a save file
            with open(filename,"r") as fichier:
                
                save = json.load(fichier)
                print(save)
                return save
            
        except:
            # without save file
            print('no save')
            self.save(name, {self.name_obj_collision:[[0,0]]})
            with open(filename ,"r") as fichier:
                save = json.load(fichier)
                
                return save
            
    
class Wall:
    def __init__(self):
        pass


    def update(self):
        pass



class Player:
    def __init__(self):
        #perso centré au centre du jeu
        self.x = 64
        self.y = 64
        self.sens = "E" #NSOE Nord Sud Est Ouest

        #position de la camera
        #on bouge la caméra au lieu du personnage
        self.cam_x = 0
        self.cam_y = 0
        
        self.job = "Student"#a besoin d'aller à la bibliothèque pour ramener des livres
        
        self.numero_skin = 2
        #self.id_skin = 0
        self.dict_skin = {0:{"N":[144, 40, 8, 8],"S":[144, 32, 8, 8], "E":[144, 32, 8, 8],"O":[144, 32, -8, 8]},
                          1: {"N":[144, 56, 8, 8],"S":[144, 48, 8, 8], "E":[144, 48, 8, 8],"O":[144, 48, -8, 8]},
                          2: {"N":[144, 72, 8, 8],"S":[144, 64, 8, 8], "E":[144, 64, 8, 8],"O":[144, 64, -8, 8]}}

        self.animation = False#if the player is walking -> no other direction
        self.direction_x = 0
        self.direction_y = 0

    def change_skin(self):

        if self.numero_skin <len(self.dict_skin)-1:
            self.add_num_skin(1)

        else:
            self.add_num_skin(0)


    def add_num_skin(self, num):
        if num == 0:
            self.numero_skin = 0
        elif num ==1:
            self.numero_skin +=1


    def update(self):
        #make move the tilemap
        x=0
        y=0
        if self.direction_x ==0 and self.direction_y == 0:
            self.animation = False
        if pyxel.btn(pyxel.KEY_Q):
            x =-TILESIZE
            

        elif pyxel.btn(pyxel.KEY_D):
            x= TILESIZE
            
        elif pyxel.btn(pyxel.KEY_S):
            y = TILESIZE
            
        
        elif pyxel.btn(pyxel.KEY_Z):
            y = -TILESIZE

        if self.animation == False:
            if not self.check_collision(x, y):
                self.direction_x = x
                self.direction_y = y

                
                self.update_sens(x, y)
                self.animation = True
            else:
                print('collision')

        elif self.animation == True:
            rapidite = 2#ne mettre que des divieseurs de 8
            if self.direction_x > 0:
                self.direction_x -= rapidite
                self.cam_x -= rapidite
            if self.direction_y > 0:
                self.cam_y -= rapidite
                self.direction_y -= rapidite

            if self.direction_x < 0:
                self.direction_x += rapidite
                self.cam_x += rapidite
            if self.direction_y < 0:
                self.cam_y += rapidite
                self.direction_y += rapidite
                
    def check_collision(self, x, y):
        # TODO: faire ca pour les collision pas centrées
        """
        Verifie que le personnage ne va pas rentrer en collision avec un objet
        return true si collision est vraie et false si coll est false
        """
        if not game.debug:
            for coll in game.list_collisions['wall'] :#check seulement des walls
                
                if self.x - self.cam_x +x== coll[0]  and coll[1] == self.y - self.cam_y + y:
                    return True
            for coll in game.list_collisions['invisible_wall'] :#check seulement des walls
                
                if self.x - self.cam_x +x== coll[0]  and coll[1] == self.y - self.cam_y + y:
                    return True
        return False
        
    def update_sens(self, x, y):
        #origine dans l'angle en haut à gauche
        if x > 0:
            self.sens = "E"
            
        elif x <0:
            self.sens = "O"
        
        elif y < 0:
            self.sens = "N"
        
        elif y > 0:
            self.sens = "S"
            
        assert self.sens in ["N", "S", "O", "E"]
        
            
        
    
    def draw(self):
        # pyxel.rect(player.x, player.y, 8, 8, 1)debug

        pyxel.blt(self.x, self.y, 0,self.dict_skin[self.numero_skin][self.sens][0], self.dict_skin[self.numero_skin][self.sens][1],
                  self.dict_skin[self.numero_skin][self.sens][2], self.dict_skin[self.numero_skin][self.sens][3], colkey=2)


        




def update():
    if game.pause == False and len(game.text_to_draw) == 0 :
        player.update()
  
    game.update()
    
    

    
def draw():
    pyxel.cls(0)
    if game.state_game == "InGame" and game.pause == False:
    
        pyxel.bltm(player.cam_x,player.cam_y, 0, 0, 0, 128, 128)
        # pyxel.bltm(0,0, 0, 0, 0, 128, 128)
        player.draw()
        game.draw()

        # if text to draw:
        if len(game.text_to_draw) != 0:
            pyxel.bltm(0, 95, 0, 256, 0, 128, 64)
            game.draw_text()
        
        
    if game.pause == True:
        
        pyxel.bltm(0, 0, 1, 128, 0, 128, 128)
        game.draw_menu_pause()

    elif game.state_game == "Backpack":
        pyxel.text(0,0,"Backpack",6)
        

        
#----------------------------------------------------------- 




player = Player()
game = Game(player)
#game.add_text("Hello~My name is Hugo~Welcome to my world~")

if __name__ == "__main__":    
    pyxel.run(update, draw)
    
