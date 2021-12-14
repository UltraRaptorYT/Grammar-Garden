import pygame
import config


class Player:
    def __init__(self, x_postition, y_position):
        super().__init__()
        self.walk_animation = False
        self.sprites_dict = {
            "walking": [],
            "idle": []
        }
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (1).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (2).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (3).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (4).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (5).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (6).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (7).png"))
        self.sprites_dict["walking"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char (8).png"))
        self.sprites_dict["idle"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char9.png"))
        self.sprites_dict["idle"].append(pygame.image.load(
            config.DIR_PATH + "\images\player\Char10.png"))
        self.position = [x_postition, y_position]
        self.current_sprite = 0
        self.image = self.sprites_dict["idle"][self.current_sprite]
        self.direction = "right"

    def update(self, speed):
        if self.walk_animation:
            self.current_sprite += speed + 0.2
            if int(self.current_sprite) >= len(self.sprites_dict["walking"]):
                self.current_sprite = 0
                self.walk_animation = False
            self.image = self.sprites_dict["walking"][int(self.current_sprite)]
        else:
            self.current_sprite += speed - 0.15
            if int(self.current_sprite) >= len(self.sprites_dict["idle"]):
                self.current_sprite = 0
            self.image = self.sprites_dict["idle"][int(self.current_sprite)]

    def update_position(self, new_position, direction):
        self.position[0] = new_position[0]
        self.position[1] = new_position[1]
        self.walk_animation = True
        if direction != "":
            self.direction = direction
        self.check_position()

    def check_position(self, pressed=False):
        if (self.position[0] == 2 or self.position[0] == 3) and self.position[1] == 5:
            if pressed:
                return False, True
            return True, False
        return False, False

    def plant(self, pressed=False):
        print(self.position)
        return self.position

    def update_direction(self, direction):
        if direction != "":
            self.direction = direction

    def render(self, screen, camera):
        self.rect = pygame.Rect(self.position[0] * config.SCALE, self.position[1]
                                * config.SCALE - (camera[1] * config.SCALE), config.SCALE, config.SCALE)
        self.image = pygame.transform.scale(
            self.image, (config.SCALE, config.SCALE))
        if self.direction == "right":
            screen.blit(pygame.transform.flip(
                self.image, True, False), self.rect)
        else:
            screen.blit(self.image, self.rect)
