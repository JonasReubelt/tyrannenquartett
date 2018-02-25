#tyrannen quartett
import sys
import pygame

pygame.init()

size = width, height = 320, 240

white = 255, 255, 255

cards = {"a1": {"name": "Kaiser Wilhelm II."}, "b1": {"name": "Adolf Hitler"}}
card_x_positions = {"left": 30, "right": 200}

screen = pygame.display.set_mode(size)

myfont = pygame.font.SysFont("arial", 10)
label = myfont.render("Some text!", 1, (255,255,0))
# render text
label = myfont.render("Kaiser Wilhelm II.", 1, (0,0,0))

def draw_card(id, pos):
    imgage = pygame.image.load("images/{}.png".format(id))
    screen.blit(imgage, (card_x_positions[pos], 0))

def draw_info(id):
    label = myfont.render(cards[id]["name"], 1, (0,0,0))
    screen.blit(label, (card_x_positions[pos], 100))

card_ids = ["a1", "b1"]
poss = ["left", "right"]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(white)
    for card_id, pos in zip(card_ids, poss):
    
        draw_card(card_id, pos)
        draw_info(card_id)
    
    pygame.display.flip()
