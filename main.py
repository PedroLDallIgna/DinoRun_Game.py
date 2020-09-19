import pygame   ##importnado o módulo pygame
import random   ##importando módulo de randomização
from math import ceil
# from PIL import Image   ##importando um módulo de imagens
# img = Image.open('nome_arquivo.extensão')
# print(img.size)

def text_objects(text, font):
    textSurface = font.render(text, True, settings.colors['white'])
    return textSurface, textSurface.get_rect()


def message_display(text, font, font_size, x, y):
    Text = pygame.font.Font(font, font_size)
    TextSurf, TextRect = text_objects(text, Text)
    TextRect.center = ((settings.width / x), (settings.height / y))
    app._display_surf.blit(TextSurf, TextRect)


def buttons(img, buttonW, buttonH, x, y, condition, action=None):
    menus.mouse_pos = pygame.mouse.get_pos()
    menus.mouse_isPressed = pygame.mouse.get_pressed()
    position = (x - (buttonW / 2), y - (buttonH / 2))
    app._display_surf.blit(img, position)

    if ((position[0] + buttonW) > menus.mouse_pos[0] > position[0]) and\
        ((position[1] + buttonH) > menus.mouse_pos[1] > position[1]) and\
        menus.mouse_isPressed[0] == 1:
        condition = True
        action()


class App(object):   ##criando a classe principal do jogo

    def __init__(self):
        self.is_Running = False      ##variável do loop principal
        self._display_surf = None    ##inicialmente o display tem valor nulo
        self._title = None           ##o título também é nulo
        self.randomic_choice = None
        self.score = 0               ##variável responsável pela pontuação do jogador

    def on_init(self):               ##função para incializar o pygame
        try:                         ##tentar iniciar o pygame
            pygame.init()
        except:                      ##em caso de excessão haverá o print abaixo
            print("O módulo pygame não funcionou corretamente.")
        self._display_surf = pygame.display.set_mode(settings.size)     ##aqui define-se o tamanho da janela e a superfície
        self._title = pygame.display.set_caption(settings._game_name)   ##e aqui define-se o título da janela, sobrepondo o valor nulo
        self.randomic_choice = [random.choice(obstacle.obstacle_keys) for key in range(3)]

    def on_event(self, event):            ##função que capturará os inputs
        if (event.type == pygame.QUIT):   ##se o usuário clicar no X
            self.on_cleanup()             ##será chamada função on_cleanup()

        if self.is_Running:               ##se a variável do loop for True, os inputs serão tratados
            self.on_runningKeys(event)    ##nesta função da classe App
        elif menus.menu_isActive:         ##se a variável que indica que um menu está ativo for True, os inputs
            menus.on_menuKeys(event)      ##serão tratados nesta função da classe Menus

        return self.is_Running            ##a função retornará se o jogo está rodando

    def on_runningKeys(self, event):                         ##quando a variável do loop é verdadeira, ela entra nesta função
        if (event.type == pygame.KEYDOWN):                   ##que verificará se a tecla foi clicada(key down)
            if (event.key == pygame.K_UP) or\
                (event.key == pygame.K_SPACE):               ##sendo assim, se o usuário pressionar SPACE ou Pg.UP acontecerá:
                pygame.mixer.init()                          ##carregando o método do pygame para sons
                pygame.mixer.music.load("assets/jump.wav")   ##load do efeito sonoro do pulo
                pygame.mixer.music.play()                    ##play do efeito sonoro
                dino.is_Jumping = True                       ##variável que identifica é para entrar na função do pulo

            if (event.key == pygame.K_DOWN):                 ##se o usuário clicar e permanecer clicada a tecla Pg.DOWN
                dino.is_Down = True                          ##variável que identifica que o dino está agachado e muda algumas coisas no loop

        if (event.type == pygame.KEYUP):                     ##quando o usuário soltar a tecla Pg.DOWN
            dino.is_Down = False                             ##a variável se tornará falsa e ele permanece levantado

    def on_render(self):
        pygame.display.update()
        settings.clock.tick(settings.FPS)

    def on_cleanup(self):
        pygame.quit()

    def on_loop(self, condition):
        dino.is_Jumping = False
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
                ground.draw_Ground()
                # ground.ground_pos_x -= settings.speed
                dino.drawDino(run[img][0])
                dino.on_jump()

                dino.on_collision(run[img], self.randomic_choice[0])

                obstacle.drawObstacle(self.randomic_choice)
                for pos in obstacle.obstacle_list_pos:
                    pos -= settings.speed
                if (obstacle.obstacle_list_pos[0] < (0 - obstacle.obstacles_images[self.randomic_choice[0]][1][1])):
                    del self.randomic_choice[0]
                    self.randomic_choice.append(random.choice(obstacle.obstacle_keys))

                score = message_display("score: " + str(int(round(self.score))), 'assets/PressStart2P-Regular.ttf', 15, 1.16, 11)
                if (self.score % 100) == 0 and self.score != 0:
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/checkPoint.wav")
                    pygame.mixer.music.play()
                self.score += 0.125

                self.on_render()

    def on_execute(self):
        self.on_init()

        menus.on_startMenu(menus.menu_isActive)

        self.on_loop(self.is_Running)

    def try_again(self):
        menus.__init__()
        obstacle.__init__()
        ground.__init__()
        cloud.__init__()
        dino.__init__()
        ground.__init__()
        ground.ground_list_pos = [
            [0, ground.ground_pos_y],
            [ground.ground_width, ground.ground_pos_y]
        ]
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
        self.speed = 12
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
            'step_right': [pygame.image.load("assets/dino_up_right.png"), (88, 94)],
            'step_left': [pygame.image.load("assets/dino_up_left.png"), (88, 94)],
            'down_step_right': [pygame.image.load("assets/dino_down_right.png"), (118, 60)],
            'down_step_left': [pygame.image.load("assets/dino_down_left.png"), (118, 60)],
            'died': [pygame.image.load("assets/dino_died.png")],
            'start': [pygame.image.load("assets/start_dino.png")]
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
        dimensions = d_width, d_height = [img[1][0], img[1][1]]
        # if pygame.Rect.colliderect(dino.drawDino(img)):
        if ((self.dino_pos_x + d_width) == obstacle.obst_pos_x)\
            and ((self.dino_pos_y + d_height) >= (244 - obstacle.obstacles_images[random][1][1]))\
            or ((self.dino_pos_y + d_height) >= (244 - obstacle.obstacles_images[random][1][1]))\
            and (self.dino_pos_x <= (obstacle.obst_pos_x + obstacle.obstacles_images[random][1][0])  <= (self.dino_pos_x + d_width)):
            pygame.mixer.init()
            pygame.mixer.music.load("assets/die.wav")
            pygame.mixer.music.play()
            app.is_Running = False
            menus.menu_isActive = True
            menus.on_gameoverMenu(menus.menu_isActive, random)



class Obstacle(object):

    def __init__(self):
        self.obstacles_images = {
            'single_small_cactus(1)': [pygame.image.load("assets/single_small_cactus(1).png"), (34, 70)],
            'single_big_cactus(1)': [pygame.image.load("assets/single_big_cactus(1).png"), (50, 100)],
            'single_big_cactus(2)': [pygame.image.load("assets/single_big_cactus(2).png"), (48, 100)],
            'single_big_cactus(3)': [pygame.image.load("assets/single_big_cactus(3).png"), (50, 100)],
            'double_small_cactus(1)': [pygame.image.load("assets/double_small_cactus(1).png"), (68, 70)],
            'double_small_cactus(2)': [pygame.image.load("assets/double_small_cactus(2).png"), (68, 70)],
            'double_small_cactus(3)': [pygame.image.load("assets/double_small_cactus(3).png"), (68, 70)],
            'double_big_cactus(1)': [pygame.image.load("assets/double_big_cactus(1).png"), (98, 100)],
            'double_big_cactus(2)': [pygame.image.load("assets/double_big_cactus(2).png"), (100, 100)],
            'triple_cactus': [pygame.image.load("assets/triple_cactus.png"), (103, 100)]
        }
        self.obst_pos = self.obst_pos_x, self.obst_pos_y = [1316, 244]
        self.obstacle_list_pos = [
            1316,
            1316 + 900,
            1316 + 900 + 1100
        ]
        self.obstacle_keys = []
        for key in self.obstacles_images.keys():
            self.obstacle_keys.append(key)
        self.obstacle_distance = random.randint(700, 1200)

    def drawObstacle(self, randomic_choice):
        if (self.obstacle_list_pos[0] <= (0 + self.obstacles_images[randomic_choice[0]][1][0])):
            del self.obstacle_list_pos[0]
            self.obstacle_distance = random.randint(700, 1200)
            self.obstacles_list_pos.append(self.obstacle_list_pos[-1] + self.obstacle_distance)
        else:
            app._display_surf.blit(self.obstacles_images[randomic_choice[0]][0], (self.obstacle_list_pos[0], (244 - self.obstacles_images[randomic_choice][1][1])))
            app._display_surf.blit(self.obstacles_images[randomic_choice[1]][0], (self.obstacle_list_pos[1], (244 - self.obstacles_images[randomic_choice][1][1])))
            app._display_surf.blit(self.obstacles_images[randomic_choice[2]][0], (self.obstacle_list_pos[2], (244 - self.obstacles_images[randomic_choice][1][1])))
        # pygame.draw.rect(
        #     app._display_surf,\
        #     settings.colors['green'],\
        #     [self.obst_pos_x, self.obst_pos_y, self.obst_dimensions[randomic_choice][0], self.obst_dimensions[randomic_choice][1]]
        #     )


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
            app._display_surf.blit(dino.dino_images['start'][0], (dino.dino_pos_x, dino.dino_pos_y))

            largeText = message_display(settings._game_name, 'assets/PressStart2P-Regular.ttf', 60, 2, 2)
            smallText = message_display('Press SPACE', 'assets/PressStart2P-Regular.ttf', 15, 2, 1.4)

            app.on_render()


    def on_menuKeys(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):
                self.menu_isActive = False
                app.is_Running = True


    def on_gameoverMenu(self, condition, random):
        message_display("GAME OVER", 'assets/PressStart2P-Regular.ttf', 60, 2, 3)
        message_display("score: " + str(int(round(app.score))), 'assets/PressStart2P-Regular.ttf', 15, 2, 2)
        obstacle.drawObstacle(random)
        app._display_surf.blit(dino.dino_images['died'][0], (dino.dino_pos_x, dino.dino_pos_y))


        while condition:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    app.on_cleanup()

            buttons(
                pygame.image.load("assets/button_gameover.png"),
                72, 64, (settings.width / 2), (settings.height/1.4),
                condition,
                app.try_again
            )

            # self.mouse_pos = pygame.mouse.get_pos()
            # self.mouse_isPressed = pygame.mouse.get_pressed()
            # position = ((settings.width / 2) - (72 / 2), (settings.height / 1.5) - (64 / 2))
            # app._display_surf.blit(pygame.image.load("assets/button_gameover.png"), position)

            # if ((position[0] + 72) > menus.mouse_pos[0] > position[0]) and\
            #     ((position[1] + 64) > menus.mouse_pos[1] > position[1]) and\
            #     menus.mouse_isPressed[0] == 1:
            #     condition = True
            #     app.try_again()

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


class Ground(object):

    def __init__(self):
        self.ground_image = pygame.image.load('assets/ground.png')
        self.ground_pos = self.ground_pos_x, self.ground_pos_y = [0, 218]
        self.ground_dimensions = self.ground_width, self.ground_height = (2404, 27)
        self.ground_list_pos = [
            [100, self.ground_pos_y],
            [100 + self.ground_width, self.ground_pos_y]
        ]

    def draw_Ground(self):
        if self.ground_list_pos[0][0] + self.ground_width < -1:
            del self.ground_list_pos[0]
            self.ground_list_pos.append([self.ground_width - 4, self.ground_pos_y])
        app._display_surf.blit(self.ground_image, (self.ground_list_pos[0][0], self.ground_list_pos[0][1]))
        app._display_surf.blit(self.ground_image, (self.ground_list_pos[1][0], self.ground_list_pos[1][1]))
        self.ground_list_pos[0][0] -= settings.speed
        self.ground_list_pos[1][0] -= settings.speed



app = App()
settings = Settings()
dino = Dino()
obstacle = Obstacle()
menus = Menus()
texts = blockTexts()
cloud = Cloud()
ground = Ground()

if __name__ == "__main__":
    app.on_execute()

##ARRUMAR AS VELOCIDADES PARA ACERTAR OS OBSTÁCULOS
##CONSERTAR AS DIMENSÕES DOS OBSTÁCULOS PARA DAR CERTO
##FAZER UMA LISTA PARA OS OBSTÁCULOS