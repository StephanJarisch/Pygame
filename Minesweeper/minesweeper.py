import numpy as np
import pygame
import time
import random
import sys
sys.setrecursionlimit(1000)

fps_counter_timer = time.time()
def fps_counter():
    global fps_counter_timer
    fps = int(1/(time.time()-fps_counter_timer + 0.000001))
    fps_counter_timer = time.time()
    return fps

class object2D():
    def __init__(self, object_name):
        self.object_name = object_name
        self.hidden = True
        self.bomb = False

        self.bomb_neighbours = 0
        self.flag = False
        self.not_flag = False #if it actually is not a flag

        self.y_pos = 0
        self.x_pos = 0

        self.pic = None
        self.pic_not_hidden = None



class minesweeperGame():
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 700

        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Minesweeper")
        pygame.init()
        pygame.font.init()
        self.FONT = pygame.font.SysFont('comicsans', 30)
        self.END_FONT = pygame.font.SysFont('comicsans', 60)

        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.runWIN = True
        self.end_won = False
        self.end_lost = False
        self.first_move = True

        icon = pygame.image.load("images/bomb.png")
        pygame.display.set_icon(icon)

        #objects2D - IMAGES
        self.stone = pygame.image.load("images/stone.png")
        self.flag = pygame.image.load("images/flag.png")
        self.not_flag = pygame.image.load("images/not_flag.png")
        self.num_1 = pygame.image.load("images/1.png")
        self.num_2 = pygame.image.load("images/2.png")
        self.num_3 = pygame.image.load("images/3.png")
        self.num_4 = pygame.image.load("images/4.png")
        self.num_5 = pygame.image.load("images/5.png")
        self.num_6 = pygame.image.load("images/6.png")
        self.num_7 = pygame.image.load("images/7.png")
        self.bomb = pygame.image.load("images/bomb.png")
        self.bomb_exp = pygame.image.load("images/bomb_exp.png")
        self.nothing = pygame.image.load("images/nothing.png")
        self.smiley = pygame.image.load("images/smiley.png")
        self.lost_smiley = pygame.image.load("images/lost.png")

        self.size_imgs = (30, 30)
        self.stone = pygame.transform.scale(self.stone, self.size_imgs)
        self.flag = pygame.transform.scale(self.flag, self.size_imgs)
        self.not_flag = pygame.transform.scale(self.not_flag, self.size_imgs)
        self.num_1 = pygame.transform.scale(self.num_1, self.size_imgs)
        self.num_2 = pygame.transform.scale(self.num_2, self.size_imgs)
        self.num_3 = pygame.transform.scale(self.num_3, self.size_imgs)
        self.num_4 = pygame.transform.scale(self.num_4, self.size_imgs)
        self.num_5 = pygame.transform.scale(self.num_5, self.size_imgs)
        self.num_6 = pygame.transform.scale(self.num_6, self.size_imgs)
        self.num_7 = pygame.transform.scale(self.num_7, self.size_imgs)
        self.bomb = pygame.transform.scale(self.bomb, self.size_imgs)
        self.bomb_exp = pygame.transform.scale(self.bomb_exp, self.size_imgs)
        self.nothing = pygame.transform.scale(self.nothing, self.size_imgs)
        self.smiley = pygame.transform.scale(self.smiley, (int(self.size_imgs[0] * 1.5), int(self.size_imgs[1] * 1.5)))
        self.lost_smiley = pygame.transform.scale(self.lost_smiley, (int(self.size_imgs[0] * 1.5), int(self.size_imgs[1] * 1.5)))


        #colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.RED = (255, 0, 0)

        #offset for grid
        self.y_offset = 100

        self.objects = []
        self.field_x, self.field_y = 20, 20

        for elem in range(self.field_x * self.field_y):
            self.objects.append(object2D("nothing"))

        self.number_of_bombs = self.field_x * self.field_y // 10
        random_indices = random.sample(range(0, len(self.objects)), self.number_of_bombs)

        for index in random_indices:
            self.objects[index].bomb = True
            self.objects[index].object_name = "bomb"

        for index, object in enumerate(self.objects):
            if not object.bomb:
                nb_indexes = self.get_neighbours(object, index)

                num_bombs = 0
                for nb_index in nb_indexes:
                    if self.objects[nb_index].bomb == True:
                        num_bombs += 1

                self.objects[index].bomb_neighbours = num_bombs

                object.pic = self.stone

                if num_bombs == 0:
                    object.pic_not_hidden = self.nothing
                elif  num_bombs == 1:
                    object.pic_not_hidden = self.num_1
                    object.object_name = "neighbour"
                elif  num_bombs == 2:
                    object.pic_not_hidden = self.num_2
                    object.object_name = "neighbour"
                elif  num_bombs == 3:
                    object.pic_not_hidden = self.num_3
                    object.object_name = "neighbour"
                elif  num_bombs == 4:
                    object.pic_not_hidden = self.num_4
                    object.object_name = "neighbour"
                elif  num_bombs == 5:
                    object.pic_not_hidden = self.num_5
                    object.object_name = "neighbour"
                elif  num_bombs == 6:
                    object.pic_not_hidden = self.num_6
                    object.object_name = "neighbour"
                elif  num_bombs == 7:
                    object.pic_not_hidden = self.num_7
                    object.object_name = "neighbour"

    def run(self):
        while self.runWIN:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.runWIN = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        print("new Game")
                        self.__init__()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos

                    if event.button == 1 and not self.end_won and not self.end_lost:
                        self.collision_detection_with_objects(x, y, "left")

                    elif event.button == 3 and not self.end_won and not self.end_lost:
                        self.collision_detection_with_objects(x, y, "right")


            self.draw()
            if self.check_for_win():
                self.end_won = True


    def draw(self):
        fps = fps_counter()

        remaining_bombs = self.number_of_bombs - self.count_flags()
        self.WIN.fill(self.GRAY)
        fps_text = self.FONT.render("FPS: " + str(fps), 1, self.WHITE)
        bomb_text = self.FONT.render("Remaining Bombs: " + str(remaining_bombs), 1, self.WHITE)


        lost_text = self.END_FONT.render("YOU LOST!", 1, self.RED)
        won_text = self.END_FONT.render("YOU WON!", 1, self.RED)

        for index, object in enumerate(self.objects):
            y_pos = (index // self.field_x) * self.size_imgs[0] + self.y_offset
            x_pos = (index % self.field_x) * self.size_imgs[1]

            if object.hidden == True:
                if object.flag == False:
                    pic = self.stone
                else:
                    if object.not_flag:
                        pic = self.not_flag
                    else:
                        pic = self.flag
            else: # not hidden
                if object.bomb == True:
                    pic = self.bomb
                else:
                    pic = object.pic_not_hidden

            #for collision detection
            object.y_pos = y_pos
            object.x_pos = x_pos
            object.y_pos_2 = y_pos + self.size_imgs[0]
            object.x_pos_2 = x_pos + self.size_imgs[1]

            self.WIN.blit(pic, (x_pos, y_pos))

        #self.WIN.blit(fps_text, (10, 10))

        if self.end_won:
            self.WIN.blit(won_text, (10, 45))
        elif self.end_lost:
            self.WIN.blit(lost_text, (10, 45))
            self.WIN.blit(self.lost_smiley, (self.WIDTH // 2 - 20, 0))
        else:
            self.WIN.blit(self.smiley, (int((self.WIDTH // 2) - 20), 0))

        self.WIN.blit(bomb_text, (10, 10))
        pygame.display.update()

    def collision_detection_with_objects(self, x, y, mouse_click):
        if mouse_click == "left":
            for index, object in enumerate(self.objects):
                if object.y_pos < y and object.y_pos_2 > y and object.x_pos < x and object.x_pos_2 > x:
                    if object.bomb:
                        object.hidden = False
                        object.pic = self.bomb_exp
                        self.you_lost()

                    if not object.flag:
                        object.hidden = False
                        self.check_if_nothing(object, index)


        else:
            for object in self.objects:
                if object.y_pos < y and object.y_pos_2 > y and object.x_pos < x and object.x_pos_2 > x:
                    if object.flag:
                        object.flag = False
                    else:
                        object.flag = True


    def check_if_nothing(self, object, index):
        if object.object_name == "nothing":
            object.hidden = False

            #check neighbours
            nb_indexes = self.get_neighbours(object, index)

            new_objects = []
            for nb_index in nb_indexes:
                #all neighbours also not hidden
                if self.objects[nb_index].hidden:
                    self.check_if_nothing(self.objects[nb_index], nb_index)

        else:
            object.hidden = False

    def get_neighbours(self, object, index):
        y_pos = index // self.field_x
        x_pos = (index % self.field_y)

        if x_pos == 0:
            nb_indexes = np.array([-self.field_x, -self.field_x+1, +1, self.field_x, self.field_x+1])+ index
        elif x_pos == self.field_y - 1:
            nb_indexes = np.array([-self.field_x-1, -self.field_x, -1, +self.field_x-1, self.field_x,]) + index
        else:
            nb_indexes = np.array([-self.field_x-1, -self.field_x, -self.field_x+1, -1, +1, +self.field_x-1, self.field_x, self.field_x+1]) + index

        nb_indexes = nb_indexes[nb_indexes>=0]
        nb_indexes = nb_indexes[nb_indexes<len(self.objects)]

        return nb_indexes

    def count_flags(self):
        count_flags = 0
        for object in self.objects:
            if object.flag:
                count_flags += 1
        return count_flags

    def count_hidden_objects(self):
        count_elem = 0
        for object in self.objects:
            if object.hidden:
                count_elem += 1
        return count_elem


    def check_for_win(self):
        #if flags equals hidden elements
        if self.count_flags() == self.count_hidden_objects():
            won = True
            for object in self.objects:
                if object.flag and not object.bomb:
                    won = False
                    object.pic = self.not_flag

            return won

        else:
            pass

    def you_lost(self):
        for object in self.objects:
            if object.flag and not object.bomb:
                object.pic = self.not_flag
                object.not_flag = True

            if object.hidden:
                if not object.flag and object.bomb:
                    object.hidden = False
                if object.flag and not object.bomb:
                    object.pic = self.not_flag
        self.end_lost = True


if __name__ == "__main__":
    game = minesweeperGame()
    game.run()
