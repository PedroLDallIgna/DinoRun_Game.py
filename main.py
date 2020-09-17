import pygame   ##importnado o módulo pygame
import random   ##importando módulo de randomização
from math import ceil
# from PIL import Image   ##importando um módulo de imagens
# img = Image.open('nome_arquivo.extensão')
# print(img.size)

def text_objects(text, font):
    textSurface = font.render(text, True, settings.colors['white'])
    return textSurface, textSurface.get_rect()


def message_display(text, font, font_size, h):
    Text = pygame.font.Font(font, font_size)
    TextSurf, TextRect = text_objects(text, Text)
    TextRect.center = ((settings.width / 2), (settings.height / h))
    app._display_surf.blit(TextSurf, TextRect)


def buttons(img, w, h, buttonW, buttonH):
    menus.mouse_pos = pygame.mouse.get_pos()
    menus.mouse_isPressed = pygame.mouse.get_pressed()
    position = ((w / 2) - (buttonW / 2), (h / 1.5) - (buttonH / 2))
    app._display_surf.blit(pygame.image.load(img), position)

    if ((position[0] + buttonW) > menus.mouse_pos[0] > position[0]) and\
        ((position[1] + buttonH) > menus.mouse_pos[1] > position[1]) and\
        menus.mouse_isPressed[0] == 1:
        app.try_again()


class App(object):   ##criando a classe principal do jogo

    def __init__(self):
        self.is_Running = False
        self._display_surf = None
        self._title = None
        self.randomic_choice = random.choice(['small', 'medium', 'large'])
        self.score = 0
        

    def on_init(self):   ##módulo para incializar o pygame
        try:   ##tentar iniciar o pygame
            pygame.init()
        except:   ##em caso de excessão haverá o print abaixo
            print("O módulo pygame não funcionou corretamente.")
        self._display_surf = pygame.display.set_mode(settings.size)   ##definindo o tamanho da janela e a superfície
        self._title = pygame.display.set_caption(settings._game_name)   ##definindo o título da janela
        settings.mixer_init()

    def on_event(self, event):   ##módulo que capturará os inputs
        if (event.type == pygame.QUIT):
            self.on_cleanup()

        if self.is_Running:
            app.on_runningKeys(event)
        elif menus.menu_isActive:
            menus.on_menuKeys(event)
        
        return self.is_Running

    def on_runningKeys(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_UP) or\
                (event.key == pygame.K_SPACE):
                dino.is_Jumping = True

            if (event.key == pygame.K_DOWN):
                dino.is_Down = True

        if (event.type == pygame.KEYUP):
            dino.is_Down = False

    def on_render(self):
        pygame.display.update()
        settings.clock.tick(settings.FPS)

    def on_cleanup(self):
        pygame.quit()

    def on_loop(self, condition):
        while condition:

            for event in pygame.event.get():
                self.on_event(event)

            run = []
            dino.on_movement(run)
            for img in range(10):
                self._display_surf.fill(settings.colors['black'])
                cloud.draw_Cloud()
                cloud.cloud_pos_x -= cloud.cloud_vel
                if cloud.cloud_pos_x < -100:
                    cloud.cloud_pos_x = random.randint(1500, 4000)
                dino.drawDino(run[img][0])   
                dino.on_jump()

                #dino.on_collision(run[img], self.randomic_choice)
                
                obstacle.drawObstacle(self.randomic_choice)
                obstacle.obst_pos_x -= settings.speed
                if (obstacle.obst_pos_x < (0 - obstacle.obst_dimensions[self.randomic_choice][0])):
                    obstacle.obst_pos_x = 900
                    self.randomic_choice = random.choice(['small', 'medium', 'large'])
                
                score = message_display("score: " + str(int(round(self.score))), 'assets/PressStart2P-Regular.ttf', 15, 4)
                self.score = int(ceil(self.score))
                if (self.score % 100) == 0 and self.score != 0:
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/checkPoint.wav")
                    pygame.mixer.music.play()
                self.score += settings.score_acceleration
                # if self.score % 10 == 0:
                #     settings.score_acceleration += 0.05
                
                self.on_render()
        
    def on_execute(self):
        self.on_init()

        menus.on_startMenu(menus.menu_isActive)
        
        self.on_loop(self.is_Running)


    # def print_score(self):
    #     score = message_display("score: " + str(int(round(self.score))), 'agencyfb', 25, 4)
    #     self.score += settings.score_acceleration
    #     if self.score % 10 == 0:
    #         settings.score_acceleration += 0.05


    def try_again(self):
        menus.__init__()
        obstacle.__init__()
        self.score = 0
        menus.menu_isActive = False
        app.is_Running = True
        self.on_loop(self.is_Running)

class Settings():

    def __init__(self):
        self.size = self.width, self.height = (900, 270)
        self._game_name = "Dino Run"
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'green': (0, 255, 0)
        }
        self.speed = 8
        self.gravity = 5
        self.acceleration = 2.5
        self.score_acceleration = 0.0001

    def mixer_init(self):
        pygame.mixer.init()


    def correct_Position(self):
        pass


class Dino(object):

    def __init__(self):
        self.dino_images = {
            'main_image': [pygame.image.load("assets/dino.png"), (88, 94)],
            # 'down_image': pygame.image.load("assets/dino_down_right.png"),
            'step_right': [pygame.image.load("assets/dino_up_right.png"), (88, 94)],
            'step_left': [pygame.image.load("assets/dino_up_left.png"), (88, 94)],
            'down_step_right': [pygame.image.load("assets/dino_down_right.png"), (118, 60)],
            'down_step_left': [pygame.image.load("assets/dino_down_left.png"), (118, 60)]
            # 'died': ["assets/dino_died.png", (00, 00)]
        }
        self.dino_pos = self.dino_pos_x, self.dino_pos_y = [100, 150]
        self.is_Jumping = False
        self.is_Down = False
        self.jump_speed = 30
        self.dino_dimensions = None
        # self.jump_sound = pygame.mixer.music.load("assets/jump.wav")
        # self.die_sound = pygame.mixer.music.load("assets/die.wav")

    def drawDino(self, img):
        if (img == self.dino_images['down_step_right'][0]) or (img == self.dino_images['down_step_left'][0]):
            app._display_surf.blit(img, (self.dino_pos_x, self.dino_pos_y + 34))
        else:
            app._display_surf.blit(img, (self.dino_pos_x, self.dino_pos_y))
        '''pygame.draw.rect(
            app._display_surf, \
            settings.colors['black'], \
            [self.dino_pos_x, self.dino_pos_y, self.dino_width, self.dino_height]
            )'''

    def on_jump(self):
        if (self.is_Jumping):
            self.dino_pos_y -= dino.jump_speed
            self.jump_speed -= settings.acceleration
      
        if (self.dino_pos_y == 150.0):
            self.is_Jumping = False
            self.jump_speed = 30
            settings.gravity = 5

        return self.is_Jumping

    def on_movement(self, run):
        #ptera_fly = ['ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_down', 'ptera_down', 'ptera_down', 'ptera_down', 'ptera_down']

        if self.is_Down:
            [run.append(self.dino_images['down_step_right']) for i in range(5)]
            [run.append(self.dino_images['down_step_left']) for i in range(5)]
            #run = [dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_right'], dino.images['down_step_left'], dino.images['down_step_left'], dino.images['down_step_left'], dino.images['down_step_left'], dino.images['down_step_left']]
        elif self.is_Jumping:
            [run.append(self.dino_images['main_image']) for i in range(10)]
            #run = [dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image'], dino.images['main_image']]
        else:
            [run.append(self.dino_images['step_right']) for i in range(5)]
            [run.append(self.dino_images['step_left']) for i in range(5)]
            #run = [dino.images['step_right'], dino.images['step_right'], dino.images['step_right'], dino.images['step_right'], dino.images['step_right'], dino.images['step_left'], dino.images['step_left'], dino.images['step_left'], dino.images['step_left'], dino.images['step_left']]

        return run

    def on_collision(self, img, random):
        self.dino_dimensions = self.dino_width, self.dino_height = [img[1][0], img[1][1]]
        # if pygame.Rect.colliderect(dino.drawDino(img)):
        if ((self.dino_pos_x + self.dino_width) == obstacle.obst_pos_x)\
            and ((self.dino_pos_y + self.dino_height) >= obstacle.obst_pos_y)\
            or ((self.dino_pos_y + self.dino_height) == obstacle.obst_pos_y) and\
            (self.dino_pos_x + self.dino_width >= obstacle.obst_pos_x):
            app.is_Running = False
            menus.menu_isActive = True
            menus.on_gameoverMenu(menus.menu_isActive, random)
        


class Obstacle(object):

    def __init__(self):
        self.obst_dimensions = {
            'small': [10, 20],
            'medium': [20, 30],
            'large': [30, 40]
        }
        self.obst_pos = self.obst_pos_x, self.obst_pos_y = [900, 200]

    def drawObstacle(self, randomic_choice):
        pygame.draw.rect(
            app._display_surf,\
            settings.colors['green'],\
            [self.obst_pos_x, self.obst_pos_y, self.obst_dimensions[randomic_choice][0], self.obst_dimensions[randomic_choice][1]]
            )


class Menus(object):

    def __init__(self):
        self.menu_isActive = True
        self.mouse_pos = None
        self.mouse_isPressed = None

    def on_startMenu(self, condition):
        while condition:

            for event in pygame.event.get():
                app.on_event(event)

            if app.is_Running == True:
                return app.is_Running

            app._display_surf.fill(settings.colors['black'])
            app._display_surf.blit(dino.dino_images['main_image'][0], (dino.dino_pos_x, dino.dino_pos_y))
            
            largeText = message_display(settings._game_name, 'assets/PressStart2P-Regular.ttf', 60, 2)
            smallText = message_display('Press SPACE', 'assets/PressStart2P-Regular.ttf', 15, 1.4)
 
            app.on_render()

    
    def on_menuKeys(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                self.menu_isActive = False
                app.is_Running = True

    
    def on_gameoverMenu(self, condition, random):
        message_display("GAME OVER", 'assets/PressStart2P-Regular.ttf', 60, 3)
        final_score = message_display("score: " + str(int(round(app.score))), 'assets/PressStart2P-Regular.ttf', 15, 2)
        obstacle.drawObstacle(random)


        while condition:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    app.on_cleanup()
            
            self.mouse_pos = pygame.mouse.get_pos()
            self.mouse_isPressed = pygame.mouse.get_pressed()
            position = ((settings.width / 2) - (72 / 2), (settings.height / 1.5) - (64 / 2))
            app._display_surf.blit(pygame.image.load("assets/button_gameover.png"), position)

            if ((position[0] + 72) > menus.mouse_pos[0] > position[0]) and\
                ((position[1] + 64) > menus.mouse_pos[1] > position[1]) and\
                menus.mouse_isPressed[0] == 1:
                condition = True
                app.try_again()
            
            app.on_render()


class blockTexts(object):

    def __init__(self):
        pass


class Cloud(object):

    def __init__(self):
        self.cloud_image = pygame.image.load('assets/cloud.png')
        self.cloud_pos = self.cloud_pos_x, self.cloud_pos_y = [random.randint(1500, 4000), 100]
        self.cloud_vel = random.randint(1, 3)
    
    def draw_Cloud(self):
        app._display_surf.blit(self.cloud_image, (self.cloud_pos_x, self.cloud_pos_y))


app = App()
settings = Settings()
dino = Dino()
obstacle = Obstacle()
menus = Menus()
texts = blockTexts()
cloud = Cloud()

if __name__ == "__main__":
    app.on_execute()

##ARRUMAR AS VELOCIDADES PARA ACERTAR OS OBSTÁCULOS
##CONSERTAR AS DIMENSÕES DOS OBSTÁCULOS PARA DAR CERTO
##FAZER UMA LISTA PARA OS OBSTÁCULOS