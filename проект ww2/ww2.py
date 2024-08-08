import arcade
import random
import tkinter as tk
import time
a = False
dif = 0
windows = tk.Tk()
windows.title('WW2 Menu')
windows.geometry('700x700')
windows.resizable(width=False, height=False)
windows.configure(bg="black")


bg_image = tk.PhotoImage(file="./Images/menu_bg.png")

canvas = tk.Canvas(windows, width=bg_image.width(), height=bg_image.height())
canvas.pack()
canvas.config(scrollregion=(250, 250, bg_image.width(), bg_image.height()))
canvas.create_image(0, 0, image=bg_image, anchor=tk.NW)
def start_game1():
    global a
    global dif
    windows.destroy()
    a   = True
    dif = "easy"
def start_game2():
    global a
    global dif
    windows.destroy()
    a = True
    dif = "medium"
def start_game3():
    global a
    global dif
    windows.destroy()
    a   = True
    dif = "hard"
    
def start():
    menu_button.destroy()

    button_easy = tk.Button(windows,width=20,height=4, text="Easy",background='silver',command=start_game1,font=20)
    button_easy.place(x=700/2.5,y=220)

    button_medium = tk.Button(windows,width=20,height=4, text="Medium",background='silver',command=start_game2,font=20)
    button_medium.place(x=700/2.5,y=340)

    button_hard = tk.Button(windows,width=20,height=4, text="Hard",background='silver',command=start_game3,font=20)
    button_hard.place(x=700/2.5,y=460)
menu_button = tk.Button(windows,width=20,height=5,background='silver',command=start,text='Старт',font=20,)
menu_button.place(x=700/2.5,y=700/2.5)


windows.mainloop()
SPEED = 2
TIME = 2
SPEED_VRAG = 0.5
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 950
START_ANGLE = 90
SCREEN_TITLE = "ww2 war"

base_hp = 10
what = False

def new_bullet(y, x, list, speed, scale, damage,angle):
    if damage == True:
        bullet = Bullet("./images/pripas.png", scale, True)
    elif damage == False:
        bullet = Bullet("./images/pripas.png", scale, False)
    bullet.center_y = y
    bullet.center_x = x
    bullet.change_y = speed
    bullet.angle = angle
    list.append(bullet)

def exp_(exp_list,x,y,scale):
    exp = GifSprite("./Images/frames/0.gif",scale)
    exp.center_x = x
    exp.center_y = y
    for i in range(17):
        exp.append_texture(arcade.load_texture(f"./images/frames/{i}.gif"))
    exp_list.append(exp)

class start_gif(arcade.Sprite):
        i = 0
        exp_time = 0
        def update_animation(self, delta_time):
            self.exp_time += delta_time
            if self.exp_time >= 0.06:
                self.exp_time = 0 
                self.i += 1
            if self.i == len(self.textures)-1:
                self.remove_from_sprite_lists()
            
            self.set_texture(self.i)

                
            
class Game(arcade.Window):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game = True
        self.bg = arcade.load_texture('./images/bg.png')
        self.game_over = arcade.load_texture('./images/game over.jpg')
        self.win_bg = arcade.load_texture('./images/win.png')
        self.vrag_bulletlist = arcade.SpriteList()
        self.enemyaviators = arcade.SpriteList()
        self.bulletlist = arcade.SpriteList()
        self.enemylist = arcade.SpriteList()
        self.timer = 0
        self.pulemet_timer = 0
        self.pulemetbullet = arcade.SpriteList()
        self.delta_time = 0.016666666666666666
        self.vrag_timer = 0
        self.is_firing = False
        self.wingg = False
        self.start = False
        self.current_frame = 0
        self.current_gif = 0
        self.exp_list = arcade.SpriteList()
        global base_hp
        self.fire = arcade.load_sound("./images/tankovyiy-vyistrel.wav")
        self.musika = arcade.load_sound("./Images/muzika.mp3")
        self.over_music = arcade.load_sound("./Images/over_music.mp3")
        self.dead = arcade.load_sound("./images/bah.mp3")
        self.hite = arcade.load_sound("./images/hite.mp3")
        self.music = arcade.load_sound("./Images/muzika.mp3")
        self.win = arcade.load_sound("./Images/win.mp3")
        self.bomb_exp = arcade.load_sound("./Images/bomb_exp.mp3")
        self.star_mus = True
        self.flybomb = arcade.load_sound("./Images/Flybomb.mp3")
        self.my_tank = MyTank("./images/tanksssr.png", 0.3, self.vrag_bulletlist, self.fire, self.bulletlist, self.hite)
    # _______________________________________________________________________
    def setup(self):
        global dif
        self.game_music = arcade.play_sound(self.music, looping=True, volume=1.5)
        self.my_tank.center_x = SCREEN_WIDTH / 2
        self.my_tank.center_y = 100
        self.my_tank.angle = START_ANGLE
        if dif == "easy":
            self.tank = 2
            self.PTO = 1
            self.time_samolet = 12
            self.big_tank = 0
            self.human = 5
            self.mashinka = 3
            self.min_samolet = 9
            self.max_samolet = 20
        elif dif == "medium":
            self.tank = 3
            self.PTO = 2
            self.time_samolet = 8
            self.big_tank = 1
            self.human = 4
            self.mashinka = 4
            self.min_samolet = 6
            self.max_samolet = 14
        elif dif == "hard":
            self.tank = 4
            self.PTO = 3
            self.time_samolet = 9
            self.big_tank = 1
            self.mashinka = 5
            self.human = 7
            self.min_samolet = 7
            self.max_samolet = 11

        for i in range(self.tank):
            self.enemy_tank = VragTank("./images/tankvrag.png", 0.25, self.vrag_timer, self.vrag_bulletlist, self.fire,
                                       self.bulletlist, self.hite, self.pulemetbullet,self.exp_list,self.dead)
            self.enemylist.append(self.enemy_tank)
            self.enemy_tank.center_x = random.randint(50, 850)
            self.enemy_tank.center_y = random.randint(1100,1700+i * 825)
            self.enemy_tank.angle = START_ANGLE
        for i in range(self.big_tank):
            self.maus = Maus("./images/maus.png", 0.5, self.vrag_timer, self.vrag_bulletlist, self.fire,
                             self.bulletlist, self.hite, self.pulemetbullet,self.exp_list,self.dead)
            self.enemylist.append(self.maus)
            self.maus.center_x = random.randint(50, 850)
            self.maus.center_y = 1600
            self.maus.angle = START_ANGLE - 180
        for i in range(self.PTO):
            self.enemy_PTO = PTO("./images/PTO.png", 0.25, self.vrag_timer, self.vrag_bulletlist, self.fire,
                                 self.bulletlist, self.hite, self.pulemetbullet,self.exp_list,self.dead)
            self.enemylist.append(self.enemy_PTO)
            self.enemy_PTO.center_x = random.randint(50, 850)
            self.enemy_PTO.center_y = random.randint(1100,1300+i * 540)
            self.enemy_PTO.angle = START_ANGLE
        for i in range(self.human):
            self.solder = Solder("./images/solder.png", 0.15, self.bulletlist, self.pulemetbullet)
            self.enemylist.append(self.solder)
            self.solder.center_x = random.randint(50, 850)
            self.solder.center_y = random.randint(1000, 3000)
            self.solder.angle = START_ANGLE + 180
        for i in range(self.mashinka):
            self.mashinka = Mashinka("./images/mashinka.png", 0.37, self.bulletlist, self.pulemetbullet)
            self.enemylist.append(self.mashinka)
            self.mashinka.center_x = random.randint(50, 850)
            self.mashinka.center_y = random.randint(1200, 4000)
            self.mashinka.angle = START_ANGLE - 360
        # ----------------------------------------------

    def update(self, delta_time):
        global what
        if self.my_tank.hp < 1 or base_hp < 1:
            self.game = False
        if len(self.enemylist) == 0:
            self.game = False
            self.wingg = True
        if self.game == True:
            self.my_tank.update()
            self.enemylist.update()
            self.bulletlist.update()
            self.vrag_bulletlist.update()
            self.exp_list.update_animation()
            self.pulemetbullet.update()
            self.enemyaviators.update()
            if self.is_firing and self.pulemet_timer < 0.1 and self.my_tank.angle == START_ANGLE:
                new_bullet(self.my_tank.top - 25, self.my_tank.center_x - 15, self.pulemetbullet, 5, 0.05, False,0)
                arcade.play_sound(self.fire, 0.5)
                self.pulemet_timer += 0.13

            if self.timer > 0:
                self.timer -= delta_time
            if self.pulemet_timer > 0:
                self.pulemet_timer -= delta_time
            if self.time_samolet > 0:
                self.time_samolet -= self.delta_time
            if self.time_samolet < 0.1:
                self.enemy_samolet = Samolet("./images/Bombardir.png", 0.15, self.vrag_timer, self.vrag_bulletlist, self.fire,
                                                                                                                     self.bulletlist, self.hite, self.pulemetbullet,self.exp_list,self.dead)
                self.enemyaviators.append(self.enemy_samolet)
                self.enemy_samolet.center_x = random.randint(50, 850)
                self.enemy_samolet.center_y = 1000
                self.enemy_samolet.angle = START_ANGLE+90
                self.time_samolet = random.randint(self.min_samolet,self.max_samolet)

    def on_key_press(self, key, modifiers):
        if self.game == True:
            if key == arcade.key.A:
                self.my_tank.change_x = -SPEED
                self.my_tank.angle = START_ANGLE + 20
            if key == arcade.key.D:
                self.my_tank.change_x = SPEED
                self.my_tank.angle = START_ANGLE - 20
            if key == arcade.key.SPACE and self.timer < 0.1 and self.my_tank.angle == START_ANGLE:
                new_bullet(self.my_tank.top, self.my_tank.center_x, self.bulletlist, 5, 0.1, False,0)
                arcade.play_sound(self.fire, 1)
                self.timer = 2
            if key == arcade.key.F and self.pulemet_timer < 0.1 and self.my_tank.angle == START_ANGLE:
                self.is_firing = True

    def on_key_release(self, key, modifiers):
        if self.game == True:
            if key == arcade.key.A or key == arcade.key.D:
                self.my_tank.change_x = 0
                self.my_tank.angle = START_ANGLE
            if key == arcade.key.F:
                self.is_firing = False

    def on_draw(self):
        global base_hp
        global what
        self.clear()
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.my_tank.draw()
        self.enemyaviators.draw()
        self.enemylist.draw()
        self.pulemetbullet.draw()
        self.bulletlist.draw()
        self.vrag_bulletlist.draw()
        arcade.draw_text(f'Base HP : {base_hp}', 30, 900, arcade.color.BLACK, 30,bold=True)
        arcade.draw_text(f'Enemies left : {len(self.enemylist)}', 30, 850, arcade.color.BLACK, 30,bold=True)
        self.exp_list.draw()
        if self.game == False and self.wingg == False:
            arcade.stop_sound(self.game_music)
            self.clear()
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.game_over)
            if self.star_mus == True and self.game == False:
                arcade.play_sound(self.over_music, 1)
                self.star_mus = False
        elif self.game == False and self.wingg == True:
            arcade.stop_sound(self.game_music)
            self.clear()
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.win_bg)
            if self.star_mus == True and self.game == False:
                arcade.play_sound(self.win, 1)
                self.star_mus = False



class VragTank(arcade.Sprite):
    def __init__(self, image_file, scale, vrag_timer, vrag_bulletlist, fire, bulletlist, hite, pulemetbullet,exp_list,dead):
        super().__init__(image_file, scale)
        self.hp = 3
        self.dead = dead
        self.exp_list = exp_list
        self.pulemetbullet = pulemetbullet
        self.vrag_timer = vrag_timer
        self.bulletlist = bulletlist
        self.vrag_bulletlist = vrag_bulletlist
        self.fire = fire
        self.bullet = Bullet("./images/pripas.png", scale, True)
        self.hite = hite
        self.delta_time = 0.016666666666666666
        self.damage = False
    def update(self):
        if self.center_y > 500:
            self.center_y -= SPEED_VRAG
        else:
            self.damage = True
        if self.vrag_timer > 0:
            self.vrag_timer -= self.delta_time
        if self.vrag_timer < 0.1 and self.hp > 0 and self.center_y < 900:
            new_bullet(self.bottom, self.center_x, self.vrag_bulletlist, -6, 0.15, self.damage,180)
            self.bullet.change_y = -6
            self.vrag_timer = 4
            arcade.play_sound(self.fire, 1)
        spisok = arcade.check_for_collision_with_list(self, self.bulletlist)
        if self.hp > 0:
            for bullet in spisok:
                bullet.remove_from_sprite_lists()
                self.hp -= 1
                arcade.play_sound(self.hite, 1)
                if self.hp <= 0:
                    self.remove_from_sprite_lists()
                    exp_(self.exp_list,self.center_x,self.center_y,1)
                    arcade.play_sound(self.dead, 2)
        spisok = arcade.check_for_collision_with_list(self, self.pulemetbullet)
        for bullet in spisok:
            bullet.remove_from_sprite_lists()


class PTO(arcade.Sprite):
    def __init__(self, image_file, scale, vrag_timer, vrag_bulletlist, fire, bulletlist, hite, pulemetbullet,exp_list,dead):
        super().__init__(image_file, scale)
        self.hp = 1
        self.dead = dead
        self.pulemetbullet = pulemetbullet
        self.vrag_timer = vrag_timer
        self.vrag_bulletlist = vrag_bulletlist
        self.fire = fire
        self.bulletlist = bulletlist
        self.hite = hite
        self.delta_time = 0.016666666666666666
        self.damage = False
        self.exp_list = exp_list
        self.a = True
    def update(self):
        if self.center_y > 750:
            self.center_y -= SPEED_VRAG / 2
        else:
            self.damage = True
        if self.vrag_timer > 0:
            self.vrag_timer -= self.delta_time
        if self.vrag_timer < 0.1 and self.hp > 0 and self.center_y < 900:
            new_bullet(self.bottom, self.center_x, self.vrag_bulletlist, -6, 0.20, self.damage,180)
            self.vrag_timer = 3.5
            arcade.play_sound(self.fire, 1)
        spisok = arcade.check_for_collision_with_list(self, self.bulletlist)
        if self.hp > 0:
            for bullet in spisok:
                bullet.remove_from_sprite_lists()
                self.hp -= 1
                arcade.play_sound(self.hite, 1)
                if self.hp <= 0:
                    self.remove_from_sprite_lists()
                    arcade.play_sound(self.dead, 1.5)
                    exp_(self.exp_list,self.center_x,self.center_y,0.5)
                    
                    
        spisok = arcade.check_for_collision_with_list(self, self.pulemetbullet)
        for bullet in spisok:
            bullet.remove_from_sprite_lists()
        

class Maus(arcade.Sprite):
    def __init__(self, image_file, scale, vrag_timer, vrag_bulletlist, fire, bulletlist, hite, pulemetbullet,exp_list,dead):
        super().__init__(image_file, scale)
        self.hp = 5
        self.dead = dead
        self.pulemetbullet = pulemetbullet
        self.vrag_timer = vrag_timer
        self.vrag_bulletlist = vrag_bulletlist
        self.exp_list = exp_list
        self.fire = fire
        self.bulletlist = bulletlist
        self.hite = hite
        self.delta_time = 0.016666666666666666
        self.damage = False

    def update(self):
        if self.center_y > 700:
            self.center_y -= SPEED_VRAG / 3
        else:
            self.damage = True
        if self.vrag_timer > 0:
            self.vrag_timer -= self.delta_time
        if self.vrag_timer < 0.1 and self.hp > 0 and self.center_y < 900:
            new_bullet(self.bottom, self.center_x, self.vrag_bulletlist, -7, 0.2, self.damage,180)
            self.vrag_timer = 4.5
            arcade.play_sound(self.fire, 1)
        spisok = arcade.check_for_collision_with_list(self, self.bulletlist)
        if self.hp > 0:
            for bullet in spisok:
                bullet.remove_from_sprite_lists()
                self.hp -= 1
                arcade.play_sound(self.hite, 1)
                if self.hp <= 0:
                    self.remove_from_sprite_lists()
                    exp_(self.exp_list,self.center_x,self.center_y,1.2)
                    arcade.play_sound(self.dead, 3)
        spisok = arcade.check_for_collision_with_list(self, self.pulemetbullet)
        for bullet in spisok:
            bullet.remove_from_sprite_lists()


class Solder(arcade.Sprite):
    def __init__(self, image_file, scale, bulletlist, pulemetbullet):
        super().__init__(image_file, scale)
        self.hp = 1
        self.pulemetbullet = pulemetbullet
        self.bulletlist = bulletlist

    def update(self):
        global base_hp
        if self.center_y > -10:
            self.center_y -= SPEED_VRAG
        else:
            base_hp = 0
        spisok = arcade.check_for_collision_with_list(self, self.bulletlist)
        if self.hp > 0:
            for bullet in spisok:
                self.hp -= 1
                if self.hp <= 0:
                    self.remove_from_sprite_lists()
        spisok = arcade.check_for_collision_with_list(self, self.pulemetbullet)
        for bullet in spisok:
            bullet.remove_from_sprite_lists()
            self.hp -= 1
            if self.hp <= 0:
                self.remove_from_sprite_lists()


class MyTank(arcade.Sprite):
    def __init__(self, image_file, scale, vrag_bulletlist, fire, bulletlist, hite):
        super().__init__(image_file, scale)
        self.hp = 1
        self.bulletlist = bulletlist
        self.vrag_bulletlist = vrag_bulletlist
        self.fire = fire
        self.hite = hite
        self.delta_time = 0.016666666666666666

    def update(self):
        self.center_x += self.change_x
        if base_hp == 0:
            self.hp = 0
        if self.center_x > SCREEN_WIDTH - 50:
            self.center_x = SCREEN_WIDTH - 50
        if self.center_x < SCREEN_WIDTH - 850:
            self.center_x = SCREEN_WIDTH - 850
        spisok = arcade.check_for_collision_with_list(self, self.vrag_bulletlist)
        if self.hp > 0:
            for bullet in spisok:
                bullet.remove_from_sprite_lists()
                self.hp -= 1
                arcade.play_sound(self.hite, 1)
        else:
            self.remove_from_sprite_lists()
        spisok2 = arcade.check_for_collision_with_list(self, window.exp_list)
        if len(spisok2) > 0:
            self.hp = 0
class Bullet(arcade.Sprite):
    def __init__(self, image_file, scale, damage):
        super().__init__(image_file, scale)
        self.damage = damage
        
    def update(self):
        global base_hp

        self.center_y += self.change_y
        if self.top > SCREEN_HEIGHT:
            self.remove_from_sprite_lists()
        elif self.top < SCREEN_HEIGHT - 870 and self.damage == False:
            self.remove_from_sprite_lists()
        elif self.top < 0 and self.damage == True:
            base_hp -= 1
            self.remove_from_sprite_lists()

class GifSprite(start_gif):
    pass
    
class Mashinka(arcade.Sprite):
    def __init__(self, image_file, scale, bulletlist, pulemetbullet):
        super().__init__(image_file, scale)
        self.hp = 5
        self.pulemetbullet = pulemetbullet
        self.bulletlist = bulletlist

    def update(self):
        global base_hp
        if self.center_y > -10:
            self.center_y -= SPEED_VRAG*1.3
        else:
            base_hp = 0
        spisok = arcade.check_for_collision_with_list(self, self.bulletlist)
        if self.hp > 0:
            for bullet in spisok:
                self.hp -= 5
                if self.hp <= 0:
                    exp_(window.exp_list,self.center_x,self.center_y,0.5)
                    arcade.play_sound(window.dead, 3)
                    self.remove_from_sprite_lists()
        spisok2 = arcade.check_for_collision_with_list(self, self.pulemetbullet)
        for bullet2 in spisok2:
            bullet2.remove_from_sprite_lists()
            self.hp -= 1
            if self.hp <= 0:
                exp_(window.exp_list,self.center_x,self.center_y,0.5)
                arcade.play_sound(window.dead, 3)
                self.remove_from_sprite_lists()
class Samolet(arcade.Sprite):
    def __init__(self, image_file, scale, vrag_timer, vrag_bulletlist, fire, bulletlist, hite, pulemetbullet,exp_list,dead):
        super().__init__(image_file, scale)
        self.vrag_timer = vrag_timer
        self.vrag_bulletlist = vrag_bulletlist
        self.exp_list = exp_list
        self.fire = fire
        self.bulletlist = bulletlist
        self.delta_time = 0.016666666666666666
        self.damage = False
        self.a = True
        self.b = True
        self.bomb_timer = 0
    def update(self):
        if self.center_y < -200:
            self.kill()
        else:
            self.center_y -= SPEED_VRAG*1.5
        if self.center_y < 120 and self.a == True:
            if self.bomb_timer == 0:
                self.bomb_timer = time.time()
            if time.time() - self.bomb_timer >= 0.5 and self.b:
                self.b = False
                arcade.play_sound(window.flybomb, 1)
                self.x = self.center_x
                self.y = self.center_y
            if time.time() - self.bomb_timer >= 4 and self.a:
                exp_(self.exp_list,self.x,self.y,1)
                arcade.play_sound(window.bomb_exp, 1)
                self.a = False
if a == True:
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()