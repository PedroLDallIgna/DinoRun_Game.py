import pygame
import random
import math


def text_objects(text, font):
    textSurface = font.render(text, True, settings.colors['BLACK'])
    return textSurface, textSurface.get_rect()


def message_display(text, font, font_size, h):
    Text = pygame.font.SysFont(font, font_size)
    TextSurf, TextRect = text_objects(text, Text)
    TextRect.center = ((settings.width / 2), (settings.height / h))
    app._display_surf.blit(TextSurf, TextRect)


def buttons(img, w, h, buttonW, buttonH, action=None):
    menus.mouse_pos = pygame.mouse.get_pos()
    menus.mouse_isPressed = pygame.mouse.get_pressed()
    position = ((w / 2) - (buttonW / 2), (h / 1.5) - (buttonH / 2))
    app._display_surf.blit(pygame.image.load(img), position)

    # if ((x + w) > menus.mouse_pos[0] > x) and ((y + h) > menus.mouse_pos[1] > y) and menus.mouse_isPressed[0] == 1 and action != None:
    #     action()

    if ((position[0] + buttonW) > menus.mouse_pos[0] > position[0]) and ((position[1] + buttonH) > menus.mouse_pos[1] > position[1]) and menus.mouse_isPressed[0] == 1 and action != None:
        action()

    # smallText = pygame.font.SysFont('agencyfb', 20, 'bold')
    # textSurf, textRect = app.text_objects(msg, smallText)
    # app._display_surf.blit(textSurf, textRect)


class App(object):

    def __init__(self):
        self.isRunning = False
        self._display_surf = None
        self.score = 0
        self.speed = Dino().jumpSpeed

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(settings.size)
        self._game_name = pygame.display.set_caption(settings._game_name)
        if (menus.start_menu() == False):
            return True
            # self.isRunning = True
            # self.on_execute()

    def on_event(self, event):
        if (event.type == pygame.QUIT):
            self.isRunning = False
        
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):    
                dino.isJumping = True
                # if (dino.isJumping == True):
                #     dino.pos[1] += -1 * dino.jumpSpeed

            if (event.key == pygame.K_DOWN):
                dino.isDown = True
        
        if (event.type == pygame.KEYUP):
            dino.isDown = False

    def on_loop(self):
        self._display_surf.fill(settings.colors['WHITE'])
        

    def on_render(self):
        pygame.display.update()
        settings.clock.tick(settings.FPS)
    
    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if (self.on_init() == True):
            self.isRunning = True
        
        while (self.isRunning):

            for event in pygame.event.get():
                self.on_event(event)
            
            run = []
            ptera_fly = ['ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_down', 'ptera_down', 'ptera_down', 'ptera_down', 'ptera_down']

            if dino.isDown:
                [run.append(dino.images['down_step_right']) for i in range(5)]
                [run.append(dino.images['down_step_left']) for i in range(5)]
                #run = [dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_left'], dino.images['down_step_left'], dino.images['down_step_left'], dino.images['down_step_left'], dino.images['down_step_left']]
            elif dino.isJumping:
                run = [dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image']]
            else:
                run = [dino.images['step_right'], dino.images['step_right'], dino.images['step_right'], dino.images['step_right'], dino.images['step_right'], dino.images['step_left'], dino.images['step_left'], dino.images['step_left'], dino.images['step_left'], dino.images['step_left']]


            for img in range(0, 8):
                
                if (dino.isJumping == True):
                    dino.pos[1] -= self.speed
                    self.speed -= settings.gravity

                if (dino.pos[1] == 0.0):
                    settings.gravity += settings.acceleration

                
                if (dino.pos[1] == 150.0):
                    dino.isJumping = False
                    self.speed = dino.jumpSpeed
                    settings.gravity = 1

                self.on_loop()
                dino.draw_dino(run[img][0])

                if ((dino.pos[0] + run[img][1][0]) == obstacles.x) and ((dino.pos[1] + run[img][1][1]) >= obstacles.y_ptera):
                   menus.game_over()
                
                score = message_display("SCORE: " + str(int(round(self.score))), 'agencyfb', 25, 4)
                if (obstacles.randomic_choice == 'ptera'):
                    obstacles.ptera(ptera_fly[img])
                else:
                    obstacles.obstacles()
                obstacles.x -= settings.speed
                self.score += settings.score_acceleration
                if (round(self.score) % 100 == 0):
                    settings.score_acceleration += 0.002
                # pygame.draw.rect(self._display_surf, dino.dino_color, dino.images['main_image'])
                if (obstacles.x <= -100):
                    obstacles.x = 902
                    settings.speed += settings.acceleration
                    obstacles.randomic_choice = random.choice(['small_cactus', 'medium_cactus', 'many_cactus', 'ptera'])
                self.on_render()
        self.on_cleanup()


class Menus(object):

    def __init__(self):
        self.menu_isActive = False
        self.mouse_pos = None
        self.mouse_isPressed = None

    def start_menu(self):
        start = True

        while start:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    app.on_cleanup()
                
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE):
                        return False
            
            # app._display_surf.fill(settings.colors['WHITE'])
            app.on_loop()
            app._display_surf.blit(dino.images['main_image'][0], (dino.pos[0], dino.pos[1]))

            largeText = message_display(settings._game_name, 'agencyfb', 100, 2)
            smallText = message_display('Press SPACE', 'agencyfb', 30, 1.3)
            
            # largeText = pygame.font.SysFont('agencyfb', 80)
            # TextSurf, TextRect = text_objects(settings._game_name, largeText)
            # TextRect.center = ((settings.width / 2), (settings.height / 3))
            # app._display_surf.blit(TextSurf, TextRect)

            # self.buttons("RUN", 400, 145, 100, 50, settings.colors['GREEN'], self.start)

            # buttons("QUIT", 550, 450, 100, 50, RED, BRIGHT_RED, quit_game)

            # pygame.display.update()
            # settings.clock.tick(15)
            app.on_render()


    def game_over(self):
        message_display("GAME OVER", 'agencyfb', 80, 3)

        while True:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    app.on_cleanup()
            
            buttons(
                "assets/button_gameover.png",
                settings.width,
                settings.height,
                72, 64,
                app.on_execute
            )
            app.on_render()


class Settings(object):

    def __init__(self):
        self.colors = {
            'BLACK': (0, 0, 0),
            'WHITE': (255, 255, 255),
            'GREEN': (0, 200, 0),
            'BLUE': (0, 0, 200),
            'RED': (200, 0, 0)
        }
        self._game_name = "Dino Run Game"
        self.size = self.width, self.height = (900, 270)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.speed = 8
        self.score_acceleration = 0.025
        self.acceleration = 0.1
        self.gravity = 1


class Dino(object):

    def __init__(self):
        self.settings = Settings()
        self.images = {
            'main_image': [pygame.image.load("assets/dino.png"), (88, 94)],
            # 'down_image': pygame.image.load("assets/dino_down_right.png"),
            'step_right': [pygame.image.load("assets/dino_up_right.png"), (88, 94)],
            'step_left': [pygame.image.load("assets/dino_up_left.png"), (88, 94)],
            'down_step_right': [pygame.image.load("assets/dino_down_right.png"), (118, 60)],
            'down_step_left': [pygame.image.load("assets/dino_down_left.png"), (118, 60)]
            # 'died': ["assets/dino_died.png", (00, 00)]
        }
        self.pos = [100, 150]
        self.dino_size = None
        self.dino_color = self.settings.colors['BLACK']
        self.isJumping = False
        self.ascend = False
        self.descend = False
        self.isDown = False
        self.isUp = False
        self.jumpSpeed = 16

    # def change_image(self):
    #     if (self.app.dino_isStopped == True):
    #         self.app.dino_image = "assets/DinoIMG.png"
    #         self.dino_size = self.images[self.app.dino_image][1]
        
    #     elif (self.app.dino_isRunning == True):
    #         self.app.dino_image = "assets/dino_up_right.png" if (self.app.dino_image == "assets/dino_up_left.png") or \
    #             (self.app.dino_image == "assets/DinoIMG.png") else "assets/dino_up_left.png"
    #         self.dino_size = self.images[self.app.dino_image][1]
        
    #     elif (self.app.dino_isDowned == True):
    #         self.app.dino_image = "assets/dino_down_right.png" if (self.app.dino_image == "assets/dino_down_left.png") or \
    #             (self.app.dino_image == "assets/DinoIMG.png") else "assets/dino_down_left.png"
    #         self.dino_size = self.images[self.app.dino_image][1]

    #     elif (self.app.dino_isDied == True):
    #         self.app.dino_image = "assets/dino_died.png"

    def on_jump(self):
        if (self.isJumping == True) and (self.pos[1] > -30):
            self.pos[1] -= app.speed
            app.speed -= 0.4
        else:
            self.ascend = False
                
        if (self.pos[1] < 150) and (self.ascend == False):
            if (self.pos[1] % 1 != 0):
                math.floor(self.pos[1])
            self.pos[1] += settings.gravity
            settings.gravity += settings.acceleration
            self.descend = True
        
        yield self.pos
                    
        if not self.ascend:
            self.isJumping = False
            app.speed = dino.jumpSpeed
                
        if (self.pos[1] == 150):
            self.descend = False
            settings.gravity = 1


    def draw_dino(self, img):
        if (img == self.images['down_step_right'][0]) or (img == self.images['down_step_left'][0]):
            app._display_surf.blit(img, (self.pos[0], self.pos[1] + 34))
        else:
            app._display_surf.blit(img, (self.pos[0], self.pos[1]))


class Obstacles(object):

    def __init__(self):
        self.obst = {
            'small_cactus': (30, 15, 205),
            'medium_cactus': (38, 23, 197),
            'many_cactus': (45, 38, 190),
            'ptera_up': [pygame.image.load("assets/ptera_up.png"), (96, 60)],
            'ptera_down': [pygame.image.load('assets/ptera_down.png'), (92, 68)]
        }
        self.x = 905
        self.y_ptera = 116
        self.randomic_choice = random.choice(['small_cactus', 'medium_cactus', 'many_cactus', 'ptera'])

    
    def ptera(self, ptera):
        if (ptera == 'ptera_up'):
            app._display_surf.blit(self.obst[ptera][0], (self.x, self.y_ptera))
        else:
            app._display_surf.blit(self.obst[ptera][0], (self.x, self.y_ptera + 20))

    # def cactus(self, cactus):


    def obstacles(self):
        # if (self.randomic_choice == 'ptera'):
        #     for thing in ['ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_down', 'ptera_down', 'ptera_down', 'ptera_down']:
        #     # else:
        #     #     app._display_surf.blit(self.obst['ptera_down'][0], (self.x, self.y_ptera))
        #     # app._display_surf.blit(self.obst['ptera_up'], (self.x, self.y_ptera))
        #     # pygame.draw.rect(app._display_surf, color, [self.x, self.y_ptera, self.obst[self.randomic_choice][1], self.obst[self.randomic_choice][0]])
        # else:
        pygame.draw.rect(app._display_surf, settings.colors['BLACK'], [self.x, self.obst[self.randomic_choice][2], self.obst[self.randomic_choice][1], self.obst[self.randomic_choice][0]])


app = App()
menus = Menus()
settings = Settings()
dino = Dino()
obstacles = Obstacles()

if __name__ == "__main__":
    app.on_execute()