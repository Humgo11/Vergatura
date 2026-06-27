import json
import pyxel


from settings import FICHIER_COLL, WIDTH_EDITOR, HEIGHT_EDITOR, TILESIZE
#fait:remove debug mode from main json
#TODO: add differents layers
#TODO: ajouter un apercu en bas
#TODO: ajouter bouton de changement

import pyxel



#de la forme: "name":{"x":int, "y":int, "w":int, "h":int}


#tilemap = *8 comparé à une tile
structure = {"maison": {"u":0,"v":0, "img":0, "w": 72, "h":48, "colkey":2}}#dictionnaire ayant pour clé le nom du batiment et pour valeur un dictionnaire avec x, y, img, u, v, w, h,, colkey = 2


class Map:
    def __init__(self):
        """allow the creation of map/levels for the game
        the map are in json files, at different layers"""

        self.list_collisions = reading_save(FICHIER_COLL)
        self.list_name_obj = ["wall", "invisible_wall", "pnj"]#TODO: automatiser la création dans collision.json
        self.name_obj_collision = "wall"#object we are modifying

        self.cam_x = 0
        self.cam_y = 0



        self.list_texture = {"wall":{"u":0,"v":0, "w":8, "h":8, "layer":0}}


    def add_element(self, position, filename, type_obj='wall'):
        """position: the coordinate of the object
        filename: the name of the filewe want to add element
        type_obj: the name of the object you want to add"""
        # TODO: a modifier pour pouvoir avoir différents walls différents

        if filename == FICHIER_COLL:
            self.list_collisions = reading_save(filename)  # on met à jour tout le fichier de collision



            if type_obj in self.list_collisions.keys():

                if position not in self.list_collisions[type_obj]:
                    self.list_collisions[type_obj].append(position)

                else:
                    self.list_collisions[type_obj].remove(position)
                # elif type_obj == "invisible_wall":
            else:
                self.list_collisions[type_obj] = [position]

            save(FICHIER_COLL, self.list_collisions)  # on sauvegarde les changements


    def update(self):
        # ------------------------------------------------------------------------------------
        # outils de construction de map

        if pyxel.btnp(pyxel.KEY_Q):
            self.cam_x -= TILESIZE
        elif pyxel.btnp(pyxel.KEY_Z):
            self.cam_y -= TILESIZE

        elif pyxel.btnp(pyxel.KEY_S):
            self.cam_y += TILESIZE

        elif pyxel.btnp(pyxel.KEY_D):
            self.cam_x += TILESIZE

        pyxel.blt(pyxel.mouse_x - pyxel.mouse_x % TILESIZE, pyxel.mouse_y - pyxel.mouse_y % TILESIZE, 0, 8, 120,
                  8, 8, colkey=2)


        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.add_element([pyxel.mouse_x - pyxel.mouse_x % TILESIZE - self.cam_x,
                          pyxel.mouse_y - pyxel.mouse_y % TILESIZE - self.cam_y], FICHIER_COLL,
                         self.name_obj_collision)


    def preview_buildings(self, name):

        if name in structure.keys():
            if structure[name]["h"] < HEIGHT_EDITOR//2 and structure[name]["w"] < WIDTH_EDITOR//2:
                pos_x = WIDTH_EDITOR - structure[name]["w"]
                pos_y = HEIGHT_EDITOR - structure[name]["h"]
            else:
                pos_x = WIDTH_EDITOR // 2
                pos_y = HEIGHT_EDITOR // 2

            pyxel.rect(pos_x - 3, pos_y - 3, structure[name]["w"] + 5, structure[name]["h"] + 5, col=2)
            pyxel.bltm(pos_x, pos_y, structure[name]["img"],structure[name]["u"], structure[name]["v"], structure[name]["w"], structure[name]["h"], colkey=structure[name]["colkey"])







    def draw(self):
        pyxel.cls(0)
        for key in self.list_collisions.keys():

            for values in self.list_collisions[key]:

                pyxel.blt(values[0], values[1], 0, self.list_texture[key]["u"], self.list_texture[key]["v"], self.list_texture[key]["w"], self.list_texture[key]["h"], colkey=3)

        self.draw_mouse()

    def draw_mouse(self):
        block = False
        for cle in self.list_collisions.keys():
            if [pyxel.mouse_x - pyxel.mouse_x % TILESIZE, pyxel.mouse_y - pyxel.mouse_y % TILESIZE] in self.list_collisions[cle]:
                block = True


        if block == True:
            pyxel.blt(pyxel.mouse_x - pyxel.mouse_x % TILESIZE, pyxel.mouse_y - pyxel.mouse_y % TILESIZE, 0, 8, 112, 8,
                     8, colkey=2)
        else:

            pyxel.blt(pyxel.mouse_x - pyxel.mouse_x % TILESIZE,pyxel.mouse_y - pyxel.mouse_y % TILESIZE,0,8, 120, 8, 8, colkey=2)

        pyxel.mouse(True)





    def add_layer_between(self, first_value, second_value):
        """add a layer between the first value and the second value
        if the layer is between the first and the second value, we increment by one the numbre of the layer, else we check another part"""
        pass

    def change_name_obj_collision(self, new_name=str):
        """change l'objet que tu rajoutes/enlève de la tilemap"""
        self.name_obj_collision = new_name




def save(name, chose_dump):
    """save chose_dump into the file that begin with name
    name: the name of the save, without the '.json' """
    filename = str(name) + ".json"

    print('sauvegarde en cour')
    with open(filename, "w") as fichier:
        json.dump(chose_dump, fichier)
        return fichier

def reading_save(name):
    """loading of the save"""
    filename = str(name) + ".json"

    try:
        # if there is a save file
        with open(filename, "r") as fichier:

            save = json.load(fichier)
            print(save)
        return save

    except:
        # without save file
        print('no save')
        save(name, {"wall": [[0, 0]]})
        with open(filename, "r") as fichier:
            save = json.load(fichier)

        return save

def update():
    map.update()

def draw():
    map.draw()
    map.preview_buildings("maison")

if __name__ == "__main__":
    pyxel.init(WIDTH_EDITOR, HEIGHT_EDITOR, title="Editor", display_scale=2)
    pyxel.load("2.pyxres")
    map = Map()
    pyxel.run(update, draw)



