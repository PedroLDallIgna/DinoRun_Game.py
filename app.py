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


def buttons(msg, x, y, w, h, color, action=None):
    menus.mouse_pos = pygame.mouse.get_pos()
    menus.mouse_isPressed = pygame.mouse.get_pressed()

    if ((x + w) > menus.mouse_pos[0] > x) and ((y + h) > menus.mouse_pos[1] > y):
        pygame.draw.rect(app._display_surf, color, (x, y, w, h))

        if menus.mouse_isPressed[0] == 1 and action != None:
            action()
    else: 
        pygame.draw.rect(app._display_surf, color, (x, y, w, h))

    smallText = pygame.font.SysFont('agencyfb', 20, 'bold')
    textSurf, textRect = app.text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    app._display_surf.blit(textSurf, textRect)


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
            if dino.isDown:
                run = [dino.block_dimensions['down_step_right'], dino.block_dimensions['down_step_right'], dino.block_dimensions['down_step_right'], dino.block_dimensions['down_step_right'], dino.block_dimensions['down_step_left'], dino.block_dimensions['down_step_left'], dino.block_dimensions['down_step_left'], dino.block_dimensions['down_step_left']]
            elif dino.ascend or dino.descend:
                run = [dino.block_dimensions['main_image']]
            else:
                run = [dino.block_dimensions['step_right'], dino.block_dimensions['step_right'], dino.block_dimensions['step_right'], dino.block_dimensions['step_right'], dino.block_dimensions['step_left'], dino.block_dimensions['step_left'], dino.block_dimensions['step_left'], dino.block_dimensions['step_left']]


            for img in run:
                
                if (dino.isJumping == True) and (dino.pos[1] > -30):
                    dino.pos[1] -= self.speed
                    self.speed -= 0.4
                    dino.ascend = True
                else:
                    dino.ascend = False
                
                if (dino.pos[1] < 150) and (dino.ascend == False):
                    if (dino.pos[1] % 1 != 0):
                        math.floor(dino.pos[1])
                    dino.pos[1] += settings.gravity
                    settings.gravity += settings.acceleration
                    dino.descend = True
                    # dino.isJumping = False
                    # if (dino.pos[1] > 50) and (dino.isJumping == False):
                    #     dino.pos[1] = 150

                if not dino.ascend:
                    dino.isJumping = False
                    self.speed = dino.jumpSpeed
                
                if (dino.pos[1] > 149) and (dino.pos[1] < 151):
                    dino.descend = False
                    dino.pos[1] = 150
                    settings.gravity = 1

                self.on_loop()
                dino.draw_dino(img)
                score = message_display("SCORE: " + str(math.floor(self.score)), 'agencyfb', 25, 4)
                obstacles.obstacles(settings.colors['BLACK'])
                obstacles.x -= settings.speed
                self.score += settings.score_acceleration
                settings.score_acceleration += 0.0001
                # pygame.draw.rect(self._display_surf, dino.dino_color, dino.images['main_image'])
                if (obstacles.x <= -200):
                    obstacles.x = 1100
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
            app._display_surf.blit(dino.block_dimensions['main_image'], (dino.pos[0], dino.pos[1]))

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
        self.score_acceleration = 0.001
        self.acceleration = 0.25
        self.gravity = 1


class Dino(object):

    def __init__(self):
        self.settings = Settings()
        self.block_dimensions = {
            'main_image': pygame.image.load("assets/dino.png"),#(50, 80)
            # 'down_image': pygame.image.load("assets/dino_down_right.png"),
            'step_right': pygame.image.load("assets/dino_up_right.png"),
            'step_left': pygame.image.load("assets/dino_up_left.png"),
            'down_step_right': pygame.image.load("assets/dino_down_right.png"),
            'down_step_left': pygame.image.load("assets/dino_down_left.png"),
            'died': ["assets/dino_died.png", (00, 00)]
        }
        self.pos = [100, 150]
        self.dino_size = None
        self.dino_color = self.settings.colors['BLACK']
        self.isJumping = False
        self.ascend = False
        self.descend = False
        self.isDown = False
        self.isUp = False
        self.jumpSpeed = 12

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
        if (img == self.block_dimensions['down_step_right']) or (img == self.block_dimensions['down_step_left']):
            app._display_surf.blit(img, (self.pos[0], self.pos[1] + 34))
        else:
            app._display_surf.blit(img, (self.pos[0], self.pos[1]))


class Obstacles(object):

    def __init__(self):
        self.obst = {
            'small_cactus': (30, 15, 205),
            'medium_cactus': (38, 23, 197),
            'many_cactus': (45, 38, 190),
            'ptera': (27, 30)
        }
        self.x = 905
        self.y_ptera = 150
        self.randomic_choice = random.choice(['small_cactus', 'medium_cactus', 'many_cactus', 'ptera'])

    def obstacles(self, color):
        if (self.randomic_choice == 'ptera'):
            pygame.draw.rect(app._display_surf, color, [self.x, self.y_ptera, self.obst[self.randomic_choice][1], self.obst[self.randomic_choice][0]])
        else:
            pygame.draw.rect(app._display_surf, color, [self.x, self.obst[self.randomic_choice][2], self.obst[self.randomic_choice][1], self.obst[self.randomic_choice][0]])


app = App()
menus = Menus()
settings = Settings()
dino = Dino()
obstacles = Obstacles()

if __name__ == "__main__":
    app.on_execute()