import pygame   ##importnado o módulo pygame
import random   ##importando módulo de randomização


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


##criando a classe principal do jogo
class App(object):   

    ##método para declarar as variáveis que serão utilizadas na classe
    def __init__(self):
        self.is_Running = False         ##variável do loop principal
        self._display_surf = None       ##inicialmente o display tem valor nulo
        self._title = None              ##o título da janela também
        self.randomic_choice = None     ##variável que receberá um obstáculo aleatoriamente
        self.score = 0                  ##variável responsável pela pontuação do jogador

    ##método para incializar a aplicação
    def on_init(self):
        try:                ##tenta iniciar o pygame
            pygame.init()
        except:             ##em caso de excessão haverá o print abaixo
            print("O módulo pygame não funcionou corretamente.")
        self._display_surf = pygame.display.set_mode(settings.size)     ##aqui define-se o tamanho da janela e a superfície
        self._title = pygame.display.set_caption(settings._game_name)   ##e aqui define-se o título da janela, sobrepondo os valores nulo
        self.randomic_choice = random.choice(obstacle.obstacle_keys)    ##escolha aleatória do obstáculo

    ##método que tratará os inputs no teclado
    def on_event(self, event):
        if (event.type == pygame.QUIT):   ##se o usuário clicar no X
            self.on_cleanup()             ##será chamada função on_cleanup()

        if self.is_Running:               ##se a variável do loop for True, os inputs serão tratados
            self.on_runningKeys(event)    ##nesta função da classe App, chamada on_runningKeys, que pega o parâmetro event
        elif menus.menu_isActive:         ##se a variável que indica que um menu está ativo for True, os inputs
            menus.on_menuKeys(event)      ##serão tratados nesta função da classe Menus, chamada on_menuKeys

        return self.is_Running            ##a função retornará a condição do loop principal

    ##método que tratará o input quando a variável do loop é verdadeira
    def on_runningKeys(self, event):
        if (event.type == pygame.KEYDOWN):                   ##verificará se a tecla foi pressionada
            if (event.key == pygame.K_UP) or\
                (event.key == pygame.K_SPACE):               ##sendo assim, se o usuário pressionar SPACE ou Pg.UP acontecerá:
                pygame.mixer.init()                          ##carregando o método do pygame para sons
                pygame.mixer.music.load("assets/jump.wav")   ##load do efeito sonoro do pulo
                pygame.mixer.music.play()                    ##play do efeito sonoro
                dino.is_Jumping = True                       ##variável que identifica se é para entrar na função do pulo

            if (event.key == pygame.K_DOWN):                 ##se o usuário clicar a tecla Pg.DOWN acontecerá:
                dino.is_Down = True                          ##variável que identifica que o dino está agachado ficará verdadeira

        if (event.type == pygame.KEYUP):                     ##quando o usuário soltar a tecla Pg.DOWN
            dino.is_Down = False                             ##a variável se tornará falsa e ele volta ao estado normal

    ##método responsável por renderizar a janela da aplicação
    def on_render(self):
        pygame.display.update()               ##método do pygame que atualizará a tela inteira, se não for passado nenhum parâmetro
        settings.clock.tick(settings.FPS)     ##responsável pelo relógio do jogo, tendo como parâmetro o número de atualizações

    ##método responsável por fechar a aplicação
    def on_cleanup(self):
        pygame.quit()    ##método do pygame que fecha a aplicação

    ##método responsável pelo loop principal do jogo, enquanto ele está rodando
    def on_loop(self, condition):
        while condition:      ##enquanto a condição passada como parâmetro for True, ele permanecerá no laço

            for event in pygame.event.get():     ##laço para capturar os eventos
                self.on_event(event)             ##e levá-los para o módulo que tratará eles

            run = []                 ##lista inicialmente vazia utilizada para armazenar chaves do dicionário de imagens do dinossauro
            dino.on_movement(run)    ##método da classe Dino que receberá como parâmetro a lista vazia e acrescentará as strings de acordo com a condição
            for img in range(10):    ##laço de 10 vezes
                self._display_surf.fill(settings.colors['black'])   ##pintando o background da imagem de preto
                cloud.draw_Cloud()   ##chamando o método da classe Cloud para desenhar a nuvem
                cloud.cloud_pos_x -= cloud.cloud_vel     ##diminuição da posição 'x' da nuvem para dar uma noção de movimento
                if cloud.cloud_pos_x < -100:             ##se a posição 'x' da nuvem for menor do que -100 
                    cloud.cloud_pos_x = random.randint(1500, 4000)    ##será reestabelecido um valor sortido entre 1500(incluso) e 4000(incluso) para a posição 'x'
                    cloud.cloud_vel = random.randint(1, 3)            ##será sorteado um número entre 1(incluso) e 3(incluso) para a velocidade da nuvem 
                ground.draw_Ground()    ##método da classe Ground para desenhar o chão
                dino.drawDino(run[img][0])   ##método da classe Dino para desenhar o dinossauro, tendo como parâmetro a lista run, com índice img(entre 1 e 10(excluso)) na posição 0
                dino.on_jump()    ##método da classe Dino para execução do pulo do dinossauro

                dino.on_collision(run[img], self.randomic_choice, img)   ##método da classe Dino que verifica se houve colisão, recebendo como parâmetro o run no índice img, o obstáculo aleatório e o img

                obstacle.drawObstacle(self.randomic_choice, img)    ##método da classe Obstacle para desenhar o obstáculo, recebendo como parâmtro a obstáculo aleatório e valor img
                obstacle.obst_pos_x -= settings.speed   ##decrescendo a posição 'x' do obstáculo para dar uma sensação de movimento
                
                ##verificação da condição para ver se o obstáculo aleatório é um ptera ou não
                if self.randomic_choice != 'ptera':
                    ##se a posição 'x' mais a largura forem menor que 0
                    if (obstacle.obst_pos_x + obstacle.obstacles_images[self.randomic_choice][1][1] <= 0):
                        self.randomic_choice = random.choice(obstacle.obstacle_keys)   ##será sorteado um novo obstáculo
                        obstacle.obst_pos_x = 1316   ##e a posição 'x' será redefinida
                ##o mesmo acontece aqui
                else: 
                    if (obstacle.obst_pos_x + 100 <= 0):
                        self.randomic_choice = random.choice(obstacle.obstacle_keys)
                        obstacle.obst_pos_x = 1316

                ##função responsável por printar na janela a pontuação do jogador
                ##recebe como parâmetro a mensagem, a fonte, o tamanho da fonte, e dois valores que dividirão a largura e a altura, para posicionar a mensagem
                message_display("score: " + str(int(round(self.score))), 'assets/PressStart2P-Regular.ttf', 15, 1.16, 11)

                if (self.score % 100) == 0 and self.score != 0:    ##verificação para que quando o valor do score tiver resto da divisão por 100 == 0
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/checkPoint.wav")  ##executará o áudio de checkpoint
                    pygame.mixer.music.play()
                self.score += 0.125/2    ##acréscimo no valor do score, de forma constante

                self.on_render()   ##chamada do método da classe App para renderizar a janela

    ##método principal da aplicação
    def on_execute(self):
        self.on_init()   ##executará o método on_init

        menus.on_startMenu(menus.menu_isActive)   ##entrará no método on_startMenu da classe Menus

        self.on_loop(self.is_Running)   ##quando o método acima tiver retorno, entrará no loop, recebendo como parâmetro a condição do laço

    ##método responsável por reinicializar as classes e valores, quando o jogador decidir jogar novamente
    def try_again(self):
        menus.__init__()
        obstacle.__init__()
        ground.__init__()
        cloud.__init__()
        dino.__init__()
        ground.ground_list_pos = [
            [0, ground.ground_pos_y],
            [ground.ground_width, ground.ground_pos_y]
        ]
        self.score = 0
        menus.menu_isActive = False
        app.is_Running = True
        self.randomic_choice = random.choice(obstacle.obstacle_keys)
        self.on_loop(self.is_Running)


##classe que contém algumas configurações da janela e da aplicação
class Settings():

    def __init__(self):
        self.size = self.width, self.height = (900, 270)   ##tupla da largura e altura da janela
        self._game_name = "T-Rex Run"   ##variável com o nome do jogo
        self.FPS = 60    ##variável com o valor de atualizações do relógio do jogo
        self.clock = pygame.time.Clock()   ##variável que incorpora o método Clock do módulo pygame
        ##variável com algumas cores
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
        }
        self.speed = 12    ##variável da velocidade dos obstáculos
        self.gravity = 5    ##variável que será utilizada no método do pulo, que representa a gravidade
        self.acceleration = 2.5   ##variável que será utilizada no método do pulo, que representa a aceleração


##classe referente ao dinossauro e seus métodos
class Dino(object):

    def __init__(self):
        ##dicionário em que carregamos as imagens utilizados e colocamos suas dimensões
        self.dino_images = {
            'main_image': [pygame.image.load("assets/dino.png"), (88, 94)],
            'step_right': [pygame.image.load("assets/dino_up_right.png"), (88, 94)],
            'step_left': [pygame.image.load("assets/dino_up_left.png"), (88, 94)],
            'down_step_right': [pygame.image.load("assets/dino_down_right.png"), (118, 60)],
            'down_step_left': [pygame.image.load("assets/dino_down_left.png"), (118, 60)],
            'died': [pygame.image.load("assets/dino_died.png")],
            'start': [pygame.image.load("assets/start_dino.png")]
        }
        self.dino_pos = self.dino_pos_x, self.dino_pos_y = [100, 150]   ##varoável com as posições 'x' e 'y' da imagem do dinossauro (a princípio)
        self.is_Jumping = False    ##variável com valor booleano que identifica se o dinossauro está pulando
        self.is_Down = False    ##variável com valor booleando que indica se o dinossauro está agachado
        self.jump_speed = 30    ##variável com a velocidade do pulo do dicionário

    ##método responsável por desenhar o dinossauro na superfície da janela, recebendo como parâmetro img
    def drawDino(self, img):
        ##verificação se o dinossauro está agachado, para haver um acréscimo na posição 'y'
        if (img == self.dino_images['down_step_right'][0]) or (img == self.dino_images['down_step_left'][0]):
            app._display_surf.blit(img, (self.dino_pos_x, self.dino_pos_y + 34))
        ##se não os valores permanecem inalterados
        else:
            app._display_surf.blit(img, (self.dino_pos_x, self.dino_pos_y))

    ##método responsável pela execução do pulo
    def on_jump(self):
        if (self.is_Jumping):    ##se for verdadeira
            self.dino_pos_y -= dino.jump_speed    ##decrescerá a posição 'y' do dinossauro com o valor de jump_speed, fazendo com que ele suba
            self.jump_speed -= settings.acceleration   ##diminui-se também o valor de jump_speed

        if (self.dino_pos_y == 150.0):  ##se a posição 'y' chegar a 150
            self.is_Jumping = False     ##condição torna-se falsa
            self.jump_speed = 30        ##retorna-se ao valor inicial de jump_speed
            # settings.gravity = 5        ##retorna-se ao valor inicial 

        return self.is_Jumping   ##ao final da execução retorna a variável que representa se ele está pulando

    ##método que recebe a lista run, e constrói a movimentação do dinossauro
    def on_movement(self, run):
        if self.is_Down:   ##se ele está abaixado
            [run.append(self.dino_images['down_step_right']) for i in range(5)]   ##cinco vezes abaixado pata direira
            [run.append(self.dino_images['down_step_left']) for i in range(5)]   ##cinco vezes abaixado pata esquerda
        elif self.is_Jumping:   ##se ele estiver pulando
            [run.append(self.dino_images['main_image']) for i in range(10)]   ##dez vezes a imagem principal
        else:   ##se não
            [run.append(self.dino_images['step_right']) for i in range(5)]   ##cinco vezes levantado pata direita
            [run.append(self.dino_images['step_left']) for i in range(5)]   ##cinco vezes levantado pata esquerda

        return run    ##retorna a lista construída

    ##método que verifica se ouve uma colisão, recebendo como parâmetro a imagem para saber as dimensões, o obstáculo aleatório para saber as dimensões e um valor que representa o índice
    def on_collision(self, img, random, index):
        dimensions = d_width, d_height = [img[1][0], img[1][1]]
        if random != 'ptera':  ##se for diferente de um ptera
            ##executa uma condição
            if ((self.dino_pos_x + d_width) == obstacle.obst_pos_x) and ((self.dino_pos_y + d_height) >= (244 - obstacle.obstacles_images[random][1][1]))\
                or ((self.dino_pos_y + d_height) >= (244 - obstacle.obstacles_images[random][1][1])) and (self.dino_pos_x <= (obstacle.obst_pos_x + obstacle.obstacles_images[random][1][0]) <= (self.dino_pos_x + d_width)):
                pygame.mixer.init()
                pygame.mixer.music.load("assets/die.wav")  ##emite o som de morte
                pygame.mixer.music.play()
                app.is_Running = False   ##muda a variável do loop para falsa
                menus.menu_isActive = True   ##muda a variável condicional do menu para verdadeira
                menus.on_gameoverMenu(menus.menu_isActive, random, index)   ##chama o método da classe Menus responsável pelo game over, recebendo a condicional de menu, o obstáculo, e o índice
        else:  ##as execuções se repetem para as outras se a condição for verdadeira
            if obstacle.ptera_fly[index] == "ptera_down":
                if ((self.dino_pos_x + d_width) == obstacle.obst_pos_x) and (self.dino_pos_y <= (obstacle.ptera_pos_y + obstacle.ptera_images["ptera_down"][1][1])):
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/die.wav")
                    pygame.mixer.music.play()
                    app.is_Running = False
                    menus.menu_isActive = True
                    menus.on_gameoverMenu(menus.menu_isActive, random, index)
            else: 
                if ((self.dino_pos_x + d_width) == obstacle.obst_pos_x) and (self.dino_pos_y <= (obstacle.ptera_pos_y + obstacle.ptera_images["ptera_up"][1][1])):
                    pygame.mixer.init()
                    pygame.mixer.music.load("assets/die.wav")
                    pygame.mixer.music.play()
                    app.is_Running = False
                    menus.menu_isActive = True
                    menus.on_gameoverMenu(menus.menu_isActive, random, index)


##classe responsável pelos obstáculos
class Obstacle(object):

    def __init__(self):
        ##dicionário com as imagens dos cactus e suas dimensões
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
            'triple_cactus': [pygame.image.load("assets/triple_cactus.png"), (103, 100)],
            'ptera': []
        }
        ##posição 'x' e 'y' dos obstáculos
        self.obst_pos = self.obst_pos_x, self.obst_pos_y = [1316, 244]
        ##dicionário com as imagens do ptera e suas dimensões
        self.ptera_images = {
            'ptera_up': [pygame.image.load("assets/ptera_up.png"), (92, 60)],
            'ptera_down': [pygame.image.load("assets/ptera_down.png"), (92, 68)]
        }
        ##posição 'y' do ptera
        self.ptera_pos_y = 105
        ##lista com 10 elementos para a movimentação do ptera
        self.ptera_fly = ['ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_up', 'ptera_down', 'ptera_down', 'ptera_down', 'ptera_down']
        ##lista vazia que representará os obstáculos a serem sorteados
        self.obstacle_keys = []
        ##adiocinando as chaves do dicionários de obstáculos à lista vazia
        for key in self.obstacles_images.keys():
            self.obstacle_keys.append(key)

    ##método responsável por desenhar o obstáculo na tela, recebendo como parâmetro o obstáculo aleatório e o índice img
    def drawObstacle(self, randomic_choice, img):
        ##se a escolha aleatória for um ptera
        if randomic_choice == 'ptera':
            ##se a condição do índice img na lista ptera_fly for igual a ptera_up:
            if self.ptera_fly[img] == 'ptera_up':
                app._display_surf.blit(self.ptera_images['ptera_up'][0], (self.obst_pos_x, self.ptera_pos_y))
            ##se não -- pois deverá ter uma acréscimo no valor 'y'
            else:
                app._display_surf.blit(self.ptera_images['ptera_down'][0], (self.obst_pos_x, self.ptera_pos_y + 10))
        ##se a escolha aleatória não for um ptera será um cactus
        else:
            app._display_surf.blit(self.obstacles_images[randomic_choice][0], (self.obst_pos_x, (244 - self.obstacles_images[randomic_choice][1][1])))


##classe referente aos menus da aplicação
class Menus(object):

    def __init__(self):
        self.menu_isActive = True   ##se o menu está ativo -- começa True pois está no menu incial
        self.mouse_pos = None   ##a posição do menu começa nula
        self.mouse_isPressed = None   ##assim como se ele está pressionado

    ##método do menu inicial, que recebe como parâmetro uma condição
    def on_startMenu(self, condition):
        while condition:  ##enquanto a condição for verdadeira

            for event in pygame.event.get():   ##caputura dos eventos 
                app.on_event(event)   ##e tratamento deles

            if app.is_Running == True:    ##se os eventos retornarem app.is_Running == True
                return app.is_Running     ##o método retornará ela

            app._display_surf.fill(settings.colors['black'])   ##background preto
            app._display_surf.blit(dino.dino_images['start'][0], (dino.dino_pos_x, dino.dino_pos_y))   ##desenho do dinossauro

            ##textos que aparecem no início
            largeText = message_display(settings._game_name, 'assets/PressStart2P-Regular.ttf', 60, 2, 2)
            smallText = message_display('Press SPACE', 'assets/PressStart2P-Regular.ttf', 15, 2, 1.4)

            ##chamado do método de renderização
            app.on_render()

    ##método que verifica os eventos ocorridos dentro de um menu, que recebe como parâmtro event
    def on_menuKeys(self, event):
        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_SPACE):  ##se o usuário pressionar a tecla SPACE
                self.menu_isActive = False   ##variável que indica se um menu está ativo fica falsa
                app.is_Running = True    ##e a variável que indica que o jogo está rodando fica verdadeira

    ##método do menu do game over, que recebe como parâmetro uma condição, o obstáulo aleatório e img
    def on_gameoverMenu(self, condition, random, img):
        ##textps
        message_display("GAME OVER", 'assets/PressStart2P-Regular.ttf', 60, 2, 3)
        message_display("score: " + str(int(round(app.score))), 'assets/PressStart2P-Regular.ttf', 15, 2, 2)
        ##desenho do obstáculo
        obstacle.drawObstacle(random, img)
        ##desenho do dinossauro
        app._display_surf.blit(dino.dino_images['died'][0], (dino.dino_pos_x, dino.dino_pos_y))

        while condition:   ##enquanto a condição for verdadeira
            
            ##captura e tratamento dos eventos
            for event in pygame.event.get():  
                if (event.type == pygame.QUIT):
                    app.on_cleanup()

            ##função botão, com a imagem, as dimensões, a posição, uma condição e uma função
            ##quando o usuário clicar no botão a função será executada
            buttons(
                pygame.image.load("assets/button_gameover.png"),
                72, 64, (settings.width / 2), (settings.height/1.4),
                condition,
                app.try_again
            )

            ##renderização da tela da aplicação
            app.on_render()


##classe para a nuvem
class Cloud(object):

    def __init__(self):
        self.cloud_image = pygame.image.load('assets/cloud.png')   ##imagem da nuvem
        self.cloud_pos = self.cloud_pos_x, self.cloud_pos_y = [random.randint(1500, 4000), 100]   ##posição aleatória do 'x' e 100 para 'y'
        self.cloud_vel = random.randint(1, 3)   ##velocidadde aleatória

    ##método para desenhar a nuvem
    def draw_Cloud(self):
        app._display_surf.blit(self.cloud_image, (self.cloud_pos_x, self.cloud_pos_y))


##classe para o chão
class Ground(object):

    def __init__(self):
        self.ground_image = pygame.image.load('assets/ground.png')   ##imagem do chão
        self.ground_pos = self.ground_pos_x, self.ground_pos_y = [0, 218]   ##posição do chão
        self.ground_dimensions = self.ground_width, self.ground_height = (2404, 27)    ##dimensões da imagem
        ##lista com dua listas, com as posições 'x' e 'y' para printar o chão
        self.ground_list_pos = [
            [100, self.ground_pos_y],
            [100 + self.ground_width, self.ground_pos_y]
        ]

    ##método para desenhar o chão
    def draw_Ground(self):
        ##se o primeiro elemento da lista mais sua largura for menor do que -1
        if self.ground_list_pos[0][0] + self.ground_width < -1:
            del self.ground_list_pos[0]   ##deleta o primeiro elemento 
            self.ground_list_pos.append([self.ground_width - 4, self.ground_pos_y])   ##e cria um outro com o valor de 'x' = a largura da que estava por segundo e agora está por primeiro
        ##desenhando as duas imagens do chão, uma ao lado da outra
        app._display_surf.blit(self.ground_image, (self.ground_list_pos[0][0], self.ground_list_pos[0][1]))
        app._display_surf.blit(self.ground_image, (self.ground_list_pos[1][0], self.ground_list_pos[1][1]))
        ##decrescimento de suas posições 'x'
        self.ground_list_pos[0][0] -= settings.speed
        self.ground_list_pos[1][0] -= settings.speed


##criando instâncias das classes
app = App()
settings = Settings()
dino = Dino()
obstacle = Obstacle()
menus = Menus()
cloud = Cloud()
ground = Ground()

if __name__ == "__main__":   ##se for True
    app.on_execute()   ##chama o método app.on_execute