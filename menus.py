import pygame
import app

class Menus(object):

    def __init__(self):
        self.menu_isActive = False
        self.mouse_pos = None
        self.mouse_isPressed = None

    def buttons(self, msg, x, y, w, h, ic, ac, action=None):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_isPressed = pygame.mouse.get_pressed()

        if ((x + w) > self.mouse_pos[0] > x) and ((y + h) > self.mouse_pos[1] > y):
            pygame.draw.rect(app.App._display_surf, ac, (x, y, w, h))

            if self.mouse_isPressed[0] == 1 and action != None:
                action()
        else: 
            pygame.draw.rect(app.App._display_surf, ic, (x, y, w, h))

        smallText = pygame.font.SysFont('comicsansms', 20)
        textSurf, textRect = app.App.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        app.App._display_surf.blit(textSurf, textRect)

    def start_menu(self):
        while (app.App.isRunning == False):
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_SPACE):
                        return app.App.isRunning == True