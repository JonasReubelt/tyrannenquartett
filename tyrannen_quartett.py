#tyrannen quartett
import sys
import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 340, 220

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 100, 100, 100

IMG_PIX_X = 86
IMG_PIX_Y = 79

CARD_X_LEFT = WIDTH - IMG_PIX_X * 2 - 20
CARD_X_RIGHT = WIDTH - IMG_PIX_X


categories = ["Geburtsjahr", "Alter bei Machtübernahme", "Herrschaftsdauer",
              "Todesopfer", "Privatvermögen (US $)"]

cards = {"a1": {"name": "Kaiser Wilhelm II."}, "b1": {"name": "Adolf Hitler"}}
card_x_positions = {"left": CARD_X_LEFT, "right": CARD_X_RIGHT}

screen = pygame.display.set_mode(SIZE)

myfont = pygame.font.SysFont("arial", 10)
label = myfont.render("Some text!", 1, (255,255,0))
# render text
label = myfont.render("Kaiser Wilhelm II.", 1, (0,0,0))

def draw_blank():
    rect = pygame.Rect(CARD_X_RIGHT, 0, IMG_PIX_X, IMG_PIX_Y)
    pygame.draw.rect(screen, GRAY, rect)
    draw_frame(card_x_positions["right"], 0, IMG_PIX_X, IMG_PIX_Y)

def draw_card(id, pos):
    imgage = pygame.image.load("images/{}.png".format(id))
    screen.blit(imgage, (card_x_positions[pos], 0))
    draw_frame(card_x_positions[pos], 0, IMG_PIX_X, IMG_PIX_Y)

def draw_info(id, kind):
    label = myfont.render(cards[id][kind], 1, (0,0,0))
    screen.blit(label, (card_x_positions[pos]+5, 90))

def draw_frame(x_0, y_0, width, height):
    rect = pygame.Rect(x_0, y_0, width, height)
    pygame.draw.rect(screen, BLACK, rect, 2)
    
def draw_categories():
    for i, category in enumerate(categories):
        draw_frame(0, 115 + i*20, 120, 20)
        draw_text(5, 120 + i*20, category)

def draw_text(x, y, text):
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (x, y))

card_ids = ["a1", "b1"]
poss = ["left", "right"]



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
    screen.fill(WHITE)
    for card_id, pos in zip(card_ids, poss):
    
        draw_card(card_id, pos)
        draw_info(card_id, "name")
    draw_categories()
    draw_blank()
        
    pygame.display.flip()
