from pygame.locals import *
import pygame
import config
from game_state import GameState
from game import Game
import sys
import numpy as np
import sgnlpmodel
import json

mainClock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(
    (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

pygame.display.set_caption("Grammar Garden")
icon = pygame.image.load(config.DIR_PATH + "\images\icon.png")
pygame.display.set_icon(icon)

title_font = pygame.font.SysFont("freesansbold.ttf", 64)
font = pygame.font.SysFont("freesansbold.ttf", 32)


def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.centerx = x
    textRect.centery = y
    surface.blit(textObj, textRect)


click = False


def main_menu():
    global click
    while True:
        screen.fill((0, 0, 0))
        bg = pygame.image.load(config.DIR_PATH + "/images/background.png")
        screen.blit(bg, (0, 0))
        draw_text('Grammar Garden', title_font, config.BLACK,
                  screen, config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 75)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect((config.SCREEN_WIDTH - 200)/2,
                               config.SCREEN_HEIGHT/2 - 25, 200, 50)
        button_2 = pygame.Rect((config.SCREEN_WIDTH - 200)/2,
                               config.SCREEN_HEIGHT/2 + 50, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                runGame()
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (3, 172, 19), button_1)
        pygame.draw.rect(screen, (3, 172, 19), button_2)
        draw_text("Start", font, (255, 255, 255), screen, (config.SCREEN_WIDTH)/2,
                  config.SCREEN_HEIGHT/2)
        draw_text("Quit", font, (255, 255, 255), screen, (config.SCREEN_WIDTH)/2,
                  config.SCREEN_HEIGHT/2+75)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def runGame():
    game = Game(screen)
    game.set_up()
    while game.game_state == GameState.RUNNING:
        mainClock.tick(60)
        game.update()
        pygame.display.flip()
        if game.question:
            question(game)


def question(game):
    with open(config.DIR_PATH + "/level.txt") as question_file:
        levelArr = list(question_file)
        randomIndex = np.random.randint(0, len(levelArr), 1)[0]
        question_text = levelArr[randomIndex].replace("\s", " ")
    running = True
    base_font = pygame.font.Font(None, 32)

    user_text = ""
    width = 140
    height = 32
    # create rectangle
    input_rect = pygame.Rect((config.SCREEN_WIDTH-width)/2,
                             (config.SCREEN_HEIGHT-height)/2, width, height)

    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')

    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    color = color_passive

    active = False
    batch_source_ids, batch_context_ids = sgnlpmodel.preprocessor([
        question_text])
    predicted_ids = sgnlpmodel.model.decode(
        batch_source_ids, batch_context_ids)
    predicted_texts = sgnlpmodel.postprocessor(predicted_ids)
    while running:
        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    predictArr = predicted_texts[0].split()
                    questionArr = question_text.split()
                    diff = list(set(predictArr) - set(questionArr))[0]
                    if diff == user_text:
                        print("Congrats")
                        game.days += 1
                        game.coins += 10
                        print(game.map)
                        fRead = open(config.DIR_PATH + '/storage.json', "r")
                        data = json.load(fRead)
                        data["days"] = game.days
                        fRead.close()
                        fWrite = open(config.DIR_PATH + '/storage.json', "w")
                        json.dump(data, fWrite)
                        fWrite.close()
                    else:
                        print("Sorry")
                        running = False
                    runGame()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    runGame()
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode

        # it will set background color of screen
        screen.fill(config.BLACK)
        bg = pygame.image.load(config.DIR_PATH + "/images/background.png")
        screen.blit(bg, (0, 0))
        if active:
            color = color_active
        else:
            color = color_passive
        draw_text(f"{question_text[:-1]}", font, config.BLACK, screen,
                  config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT/2 - 50)
        draw_text("Type out the wrong word from the sentence", font, config.BLACK, screen,
                  config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT/2 - 150)
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, config.BLACK)

        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        pygame.display.update()
        mainClock.tick(60)


main_menu()
