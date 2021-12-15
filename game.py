import pygame
import config
import math
from player import Player
from game_state import GameState
import json


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE
        self.map = []
        self.camera = [0, 0]
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.click = False
        self.menu = False
        self.question = False
        self.active = False
        f = open(config.DIR_PATH + '/storage.json', "r")
        data = json.load(f)
        self.days = data["days"]
        self.coins = data["coins"]
        self.showText = False
        f.close()

    def set_up(self):
        player = Player(3, 5)
        self.player = player
        self.objects.append(player)
        self.game_state = GameState.RUNNING
        self.load_map("map")

    def update(self):
        if not self.active:
            self.screen.fill(config.BLACK)
            self.handle_events()
            self.player.update(0.25)
            self.render_map(self.screen)
            show, check = self.player.check_position()
            if show:
                self.load_text("Press E to enter house",
                               config.BLACK, self.screen, config.SCREEN_WIDTH/2, 50)
            if self.question:
                self.question_popup()
            for object in self.objects:
                object.render(self.screen, self.camera)
            if self.showText:
                self.load_text("Press P to plant potato",
                               config.BLACK, self.screen, config.SCREEN_WIDTH/2, 50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            #     handle key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.ENDED
                elif event.key == pygame.K_w:  # up
                    self.move_unit(self.player, [0, -1])
                elif event.key == pygame.K_s:  # down
                    self.move_unit(self.player, [0, 1])
                elif event.key == pygame.K_a:  # up
                    self.move_unit(self.player, [-1, 0])
                elif event.key == pygame.K_d:  # up
                    self.move_unit(self.player, [1, 0])
                elif event.key == pygame.K_e:
                    show, check = self.player.check_position(True)
                    if check:
                        self.question = True
                elif event.key == pygame.K_p:
                    if self.showText:
                        print("Planting Seed")

    def load_map(self, file_name):
        with open('maps/' + file_name + ".txt") as map_file:
            for line in map_file:
                tiles = []
                for i in line.split():
                    tiles.append(i)
                self.map.append(tiles)

    def render_map(self, screen):
        self.determine_camera()

        y_pos = 0
        for line in self.map:
            x_pos = 0
            for tile in line:
                image = map_tile_image[tile]
                rect = pygame.Rect(x_pos * config.SCALE, y_pos * config.SCALE -
                                   (self.camera[1] * config.SCALE), config.SCALE, config.SCALE)
                screen.blit(image, rect)
                x_pos = x_pos + 1
            y_pos = y_pos + 1

    def move_unit(self, unit, position_change):
        new_position = [unit.position[0] + position_change[0],
                        unit.position[1] + position_change[1]]
        direction = ""
        if position_change[0] == -1:
            direction = "left"
        if position_change[0] == 1:
            direction = "right"
        unit.update_direction(direction)
        noncollide = ["W", "H17", "H18", "H19",
                      "H20", "H16", "H12", "H7", "H6", "H9", "H13"]
        if new_position[0] < 0 or new_position[0] > (len(self.map[0]) - 1):
            return

        if new_position[1] < 0 or new_position[1] > (len(self.map) - 1):
            return
        if self.map[new_position[1]][new_position[0]] in noncollide:
            return
        unit.update_position(new_position, direction)
        stand_map = self.map[new_position[1]][new_position[0]]
        if stand_map == "6" or "P" in stand_map:
            if stand_map == "6":
                self.showText = True
            unit.plant()
        else:
            self.showText = False

    def determine_camera(self):
        max_y_position = len(self.map) - config.SCREEN_HEIGHT / config.SCALE
        y_position = self.player.position[1] - \
            math.ceil(round(config.SCREEN_HEIGHT / config.SCALE / 2))

        if y_position <= max_y_position and y_position >= 0:
            self.camera[1] = y_position
        elif y_position < 0:
            self.camera[1] = 0
        else:
            self.camera[1] = max_y_position

    def question_popup(self):
        base_font = pygame.font.Font(None, 32)
        user_text = ''
        # create rectangle
        input_rect = pygame.Rect(200, 200, 140, 32)
        color_passive = pygame.Color('chartreuse4')
        color = color_passive
        self.active = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

                # Unicode standard is used for string
                # formation
                elif event.key == pygame.K_KP_ENTER:
                    self.answer = user_text
                else:
                    user_text += event.unicode
        pygame.draw.rect(self.screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        self.screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

    def load_text(self, text, color, surface, x, y):
        font = self.font
        textObj = font.render(text, 1, color)
        textRect = textObj.get_rect()
        textRect.centerx = x
        textRect.centery = y
        surface.blit(textObj, textRect)


map_tile_image = {
    "1": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape1.png"), (config.SCALE, config.SCALE)),
    "2": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape2.png"), (config.SCALE, config.SCALE)),
    "3": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape3.png"), (config.SCALE, config.SCALE)),
    "4": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape4.png"), (config.SCALE, config.SCALE)),
    "5": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape5.png"), (config.SCALE, config.SCALE)),
    "6": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape6.png"), (config.SCALE, config.SCALE)),
    "A": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape13.png"), (config.SCALE, config.SCALE)),
    "B": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape14.png"), (config.SCALE, config.SCALE)),
    "C": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape25.png"), (config.SCALE, config.SCALE)),
    "D": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape26.png"), (config.SCALE, config.SCALE)),
    "E": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape27.png"), (config.SCALE, config.SCALE)),
    "F": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape15.png"), (config.SCALE, config.SCALE)),
    "P1": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\potato\potato1.png"), (config.SCALE, config.SCALE)),
    "P2": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\potato\potato2.png"), (config.SCALE, config.SCALE)),
    "P3": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\potato\potato3.png"), (config.SCALE, config.SCALE)),
    "P4": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\potato\potato4.png"), (config.SCALE, config.SCALE)),
    "P5": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\potato\potato5.png"), (config.SCALE, config.SCALE)),
    "H1": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House1.png"), (config.SCALE, config.SCALE)),
    "H2": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House2.png"), (config.SCALE, config.SCALE)),
    "H3": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House3.png"), (config.SCALE, config.SCALE)),
    "H4": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House4.png"), (config.SCALE, config.SCALE)),
    "H5": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House5.png"), (config.SCALE, config.SCALE)),
    "H6": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House6.png"), (config.SCALE, config.SCALE)),
    "H7": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House7.png"), (config.SCALE, config.SCALE)),
    "H8": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House8.png"), (config.SCALE, config.SCALE)),
    "H9": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House9.png"), (config.SCALE, config.SCALE)),
    "H10": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House10.png"), (config.SCALE, config.SCALE)),
    "H11": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House11.png"), (config.SCALE, config.SCALE)),
    "H12": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House12.png"), (config.SCALE, config.SCALE)),
    "H13": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House13.png"), (config.SCALE, config.SCALE)),
    "H14": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House14.png"), (config.SCALE, config.SCALE)),
    "H15": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House15.png"), (config.SCALE, config.SCALE)),
    "H16": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House16.png"), (config.SCALE, config.SCALE)),
    "H17": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House17.png"), (config.SCALE, config.SCALE)),
    "H18": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House18.png"), (config.SCALE, config.SCALE)),
    "H19": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House19.png"), (config.SCALE, config.SCALE)),
    "H20": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\house\House20.png"), (config.SCALE, config.SCALE)),
    "G": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscape.png"), (config.SCALE, config.SCALE)),
    "G2": pygame.transform.scale(pygame.image.load(config.DIR_PATH + "\images\landscape\landscapeG.png"), (config.SCALE, config.SCALE)),
}
