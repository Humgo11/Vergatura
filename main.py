# -*- coding: utf-8 -*-
"""
Created on 12/02/2026

@author: Hugo
"""

import json
import pyxel
from settings import WIDTH, HEIGHT, FICHIER_COLL, TILESIZE

# TODO: reglage colision

pyxel.init(WIDTH, HEIGHT, fps=30,title="Vergatura and the forgotten Library")
#possibilité de rajouté un dézoom 
# ,display_scale=5
pyxel.load("2.pyxres")

liste_state_game = ["InGame"]


class Game:
    def __init__(self):
        self.state_game = "InGame"
        self.pause = False
        self.debug = False
        self.centred = True
        self.list_collisions = self.reading_save(FICHIER_COLL)
        self.text_to_draw = []
        
        
        
        self.origin_point = [0,0]#TODO: réparer pb de collision
        self.modification_map = False
        
    def update(self):
        #Pause
        if pyxel.btnp(pyxel.KEY_P):
            if self.pause == False:
                self.pause = True
            else:
                self.pause = False
                
        #outils de construction de map        
        if pyxel.btnp(pyxel.KEY_M):
            if self.modification_map ==False:
                pyxel.mouse(True)
                self.modification_map = True
            else:
               pyxel.mouse(False)
               self.modification_map = False 
               
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.modification_map:
            if self.centred == True:
                self.add_element([pyxel.mouse_x-pyxel.mouse_x%TILESIZE-player.cam_x , pyxel.mouse_y - pyxel.mouse_y%TILESIZE -player.cam_y], FICHIER_COLL)
            else:
                self.add_element([pyxel.mouse_x-player.cam_x,pyxel.mouse_y-player.cam_y], FICHIER_COLL)
        
   
    
    def draw(self):
        #affiche les différents éléments ayant une collision
        for tab in self.list_collisions["wall"]:
            if self.debug == True:
                pyxel.rectb(tab[0]+player.cam_x, tab[1]+player.cam_y, TILESIZE,TILESIZE, 2)
            else:
                pyxel.blt(tab[0]+player.cam_x, tab[1]+player.cam_y, 0, 72, 104, 8, 8, colkey=2)
            
        if self.modification_map==True:
            pyxel.blt(pyxel.mouse_x-pyxel.mouse_x % TILESIZE, pyxel.mouse_y - pyxel.mouse_y % TILESIZE, 0, 8, 120, 8, 8, colkey=2)
            
        
    def draw_text(self):
        # TODO: ajouter une tête qui montre qui parle
        if len(self.text_to_draw) != 0:
            pyxel.text(10, 100, str(self.text_to_draw[0]), 7)
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.text_to_draw = self.text_to_draw[1:]
            
    def add_text(self, text):
        assert text == str
        self.text_to_draw.append(text)
        print("add of text")
        
            
    
    def add_element(self, position, filename, type_obj="wall"):
        """position: la position de l'élément à placer"""
     # TODO: a modifier pour pouvoir avoir différents walls différents  
        
        if filename == FICHIER_COLL:
            self.list_collisions = self.reading_save(filename)#on met à jour tout le fichier de collision
            
            
            if type_obj =="wall":
                if position not in self.list_collisions["wall"]:
                    self.list_collisions["wall"].append(position)
                
                else:
                    self.list_collisions["wall"].remove(position)
                    
            
            self.save(FICHIER_COLL, self.list_collisions)#on sauvegarde les changements
            
    
    
    def save(self, name, chose_dump):
        """cree fichier a partir de rien"""
        filename = str(name)+".json"
        
        print('save en cour')
        with open(filename ,"w") as fichier:
            json.dump(chose_dump, fichier)
            return fichier
            

    def reading_save(self, name):
        """chargement de la sauvegarde"""
        filename = str(name)+".json"
        
        try:
            # si save
            with open(filename,"r") as fichier:
                
                sauvegarde = json.load(fichier)
                print(sauvegarde)
                return sauvegarde
            
        except:
            # sans save
            print('no save')
            self.save(name, {"wall":[[0,0]]})
            with open(filename ,"r") as fichier:
                sauvegarde = json.load(fichier)
                
                return sauvegarde
            
    
    def print_text(self, text, spliting_object=""):
        """ 
        -text: text you want to print type:str
        -splitting_object: str of the caracter that allow the return 
        split the text receive multiple version, split by the '~' 
        and print it on the terminal"""
        # TODO: rajouter des sécurités
        lines = []
        new_repere = 0
        for i in range(len(text)):
            if text[i] == spliting_object and i != 0:
                lines.append(text[new_repere:i])
                new_repere = i +1
        
        for elem in lines:
            print(str(elem))
        
        return lines
            
    

    def choice(self, question, option, response):
        # TODO: allow more liberty into the chat section
        print("-------------------------------------------------")
        print("")
        print(str(question))
        print("What is your answer:")
        for i in range(len(option)):
            print(f"[ {i} ]", option[i])
            
        option_chosen = int(input("What is your response ? "))
        
        
        if option_chosen not in option.keys():
            option_chosen = None
            print('LOL, I have seen you coming ^_^')
        else:
            print(response[option_chosen])
        
        
        print("")
        print("-------------------------------------------------")
        return response            
    
    
        

class Player:
    def __init__(self):
        self.x = 64
        self.y = 64
        self.sens = "E" #NSOE
        
        #position de la camera
        self.cam_x = 0
        self.cam_y = 0
        
        self.job = "Etudiant"#a besoin d'aller à la bibliothèque pour ramener des livres
        
        self.num_skin = 2
        self.dict_skin = {0:{"N":[152, 24, 8, 8],"S":[144, 16, 8, 8], "E":[144, 16, 8, 8],"O":[144, 16, -8, 8]},
                          1: {"N":[144, 48, 8, 8],"S":[144, 40, 8, 8], "E":[144, 40, 8, 8],"O":[144, 40, -8, 8]},
                          2: {"N":[144, 64, 8, 8],"S":[144, 56, 8, 8], "E":[144, 56, 8, 8],"O":[144, 56, -8, 8]}}
        
        
        
    def update(self):
        #fait bouger la tilemap
        x=0
        y=0
        if pyxel.btnp(pyxel.KEY_Q):
            x =-TILESIZE
            
            
        elif pyxel.btnp(pyxel.KEY_D):
            x= TILESIZE
            
        elif pyxel.btnp(pyxel.KEY_S):
            y = TILESIZE
            
        
        elif pyxel.btnp(pyxel.KEY_Z):
            y = -TILESIZE

        if not self.check_collision(x, y):
            self.cam_x -= x
            self.cam_y -= y
    
        self.update_sens(x, y)
    
    def check_collision(self, x, y):
        # TODO: faire ca pour les collision pas centrées
        """
        Verifie que le personnage ne va pas rentrer en collision avec un objet
        return true si collision est vraie et false si coll est false
        """
        for coll in game.list_collisions["wall"] :#check seulement des walls
            
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
        
        pyxel.blt(self.x, self.y, 0, self.dict_skin[self.num_skin][self.sens][0],
                  self.dict_skin[self.num_skin][self.sens][1], self.dict_skin[self.num_skin][self.sens][2],
                  self.dict_skin[self.num_skin][self.sens][3], colkey=2)
        
        


def choice_option(option):
    """affiche les options des menus"""
    for i in range(len(option)):
        pyxel.text(20, 20+10*(i+1), option[i], 6)
        
    
        
    


def draw_menu_pause():
    option = {0:"Continuer" ,1:"Aide"}
    choice_option(option)

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
        
        if len(game.text_to_draw) != 0:
            pyxel.bltm(0, 95, 0, 256, 0, 128, 64)
            game.draw_text()
        
        
    if game.pause == True:
        
        pyxel.bltm(0, 0, 1, 128, 0, 128, 128)
        draw_menu_pause()
        

        
#----------------------------------------------------------- 



game = Game()
player = Player()

if __name__ == "__main__":    
    pyxel.run(update, draw)
    
