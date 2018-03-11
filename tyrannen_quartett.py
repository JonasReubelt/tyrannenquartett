#tyrannen quartett
import sys
import pygame
import random

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GRAY = 100, 100, 100
GREEN = 0, 255, 0
RED = 255, 0, 0

IMG_Y_START = 40

FRAME_HEIGHT = 30
FRAME_Y_START = 300
CATEGORY_WIDTH = 200
TEXT_Y_START = FRAME_Y_START + 5
TEXT_X_OFFSET = 5
NAME_Y = 90
CARD_NUMBER_Y = 470

IMG_PIX_X = 179
IMG_PIX_Y = 221

CARD_X_LEFT = WIDTH - IMG_PIX_X * 2 - 70 - 60
CARD_X_RIGHT = WIDTH - IMG_PIX_X - 60

card_xs = {"left": CARD_X_LEFT, "right": CARD_X_RIGHT}




categories = ["Geburtsjahr", "Alter bei Machtübernahme", "Herrschaftsdauer",
              "Todesopfer", "Privatvermögen (US $)"]

def read_card_info(filename, categories):
    cards = {}
    infile = open(filename, "r")
    for line in infile:
        l = line.split(";")
        card = {}
        card["name"] = l[1]
        for i, category in enumerate(categories):
            card[category] = int(l[i+2])
        cards[l[0]] = card
    
    infile.close()
    return cards

cards = read_card_info("card_info.txt", categories)
"""
cards = {"a1": {"name": "Kaiser Wilhelm II.", 
                "Geburtsjahr": 1859,
                "Alter bei Machtübernahme": 29, 
                "Herrschaftsdauer": 30, 
                "Todesopfer": 9000000, 
                "Privatvermögen (US $)": 10000000000}, 
         "b1": {"name": "Adolf Hitler",
                "Geburtsjahr": 1889,
                "Alter bei Machtübernahme": 43,
                "Herrschaftsdauer": 12,
                "Todesopfer": 55000000,
                "Privatvermögen (US $)": 3000000000}}
"""
card_x_positions = {"left": CARD_X_LEFT, "right": CARD_X_RIGHT}

screen = pygame.display.set_mode(SIZE)

myfont = pygame.font.SysFont("arial", 16)
label = myfont.render("Some text!", 1, (255,255,0))
# render text
label = myfont.render("Kaiser Wilhelm II.", 1, (0,0,0))

def draw_blank():
    rect = pygame.Rect(CARD_X_RIGHT, IMG_Y_START, IMG_PIX_X, IMG_PIX_Y)
    pygame.draw.rect(screen, GRAY, rect)
    draw_frame(card_x_positions["right"], IMG_Y_START, IMG_PIX_X, IMG_PIX_Y)

#def draw_

def draw_card(id, pos):
    imgage = pygame.image.load("images/{}.png".format(id))
    screen.blit(imgage, (card_x_positions[pos], IMG_Y_START))
    draw_frame(card_x_positions[pos], IMG_Y_START, IMG_PIX_X, IMG_PIX_Y)
    

def draw_name(id, pos):
    label = myfont.render(cards[id]["name"], 1, BLACK)
    screen.blit(label, (card_x_positions[pos] + TEXT_X_OFFSET, NAME_Y))

def draw_frame(x_0, y_0, width, height):
    rect = pygame.Rect(x_0, y_0, width, height)
    pygame.draw.rect(screen, BLACK, rect, 2)
    
def draw_categories():
    for i, category in enumerate(categories):
        draw_frame(0, 
                   FRAME_Y_START + i*FRAME_HEIGHT,
                   CATEGORY_WIDTH,
                   FRAME_HEIGHT)
        draw_text(TEXT_X_OFFSET, TEXT_Y_START + i*FRAME_HEIGHT, category)

def draw_text(x, y, text):
    label = myfont.render(text, 1, BLACK)
    screen.blit(label, (x, y))

def draw_values(id, pos):
    for i, category in enumerate(categories):
        draw_frame(card_xs[pos],
                   FRAME_Y_START + i*FRAME_HEIGHT,
                   IMG_PIX_X,
                   FRAME_HEIGHT)
        draw_text(card_xs[pos] + TEXT_X_OFFSET,
                  TEXT_Y_START + i*FRAME_HEIGHT,
                  str(cards[id][category]))

def draw_turn(whose_turn):
    draw_text(10, 10, "{} turn".format(whose_turn))

def draw_number_of_cards(player_cards, ai_cards):
    draw_text(CARD_X_LEFT + TEXT_X_OFFSET,
              5, 
              "Spieler ({} Tyrannen)".format(player_cards))
    draw_text(CARD_X_RIGHT + TEXT_X_OFFSET,
              5,
              "AI ({} Tyrannen)".format(ai_cards))

def chosen_category(mouse_pos):
    x = mouse_pos[0]
    y = mouse_pos[1]
    for i, category in enumerate(categories):
        if x > (CARD_X_LEFT) and x < (CARD_X_LEFT + IMG_PIX_X):
            if y > (FRAME_Y_START + i*FRAME_HEIGHT) and y < (FRAME_Y_START
                                                             + i*FRAME_HEIGHT
                                                             + FRAME_HEIGHT):
                return category

def ai_category(categories):
    c = categories[:]
    random.shuffle(c)
    return c[0]

def mark_category(color, pos, category):
    try:
        index = categories.index(category)
    except:
        return 0
    rect = pygame.Rect(card_x_positions[pos],
                       FRAME_Y_START +index*FRAME_HEIGHT, 
                       IMG_PIX_X, 
                       FRAME_HEIGHT)
    pygame.draw.rect(screen, color, rect)

def calc_winner(category, ids):
    if category == "Alter bei Machtübernahme":
        if cards[ids[0]][category] < cards[ids[1]][category]:
            return ids[0]
        else:
            return ids[1]
    else:
        if cards[ids[0]][category] > cards[ids[1]][category]:
            return ids[0]
        else:
            return ids[1]

def distribute_cards(cards):
    card_list = list(cards.keys())
    random.shuffle(card_list)
    player_cards = card_list[:16]
    ai_cards = card_list[16:]
    return player_cards, ai_cards



player_cards, ai_cards = distribute_cards(cards)

n_player_cards = 16
n_ai_cards = 16

c = list(cards.keys())
random.shuffle(c)

poss = ["left", "right"]

covered = True

NO_MARK = (False, False, False)

mark = NO_MARK

clock = pygame.time.Clock()

next_card = False

whose_turn = "player"

while 1:
    screen.fill(WHITE)
    draw_categories()
    card_ids = (player_cards[0], ai_cards[0])
    draw_number_of_cards(n_player_cards, n_ai_cards)
    #draw_turn(whose_turn)
    if False not in mark:
        mark_category(*mark)

    for card_id, pos in zip(card_ids, poss):
        if covered and pos == "right":
            draw_blank()
            continue
        draw_card(card_id, pos)
        #draw_name(card_id, pos)
        draw_values(card_id, pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_card == True:
                player_cards.pop(0)
                ai_cards.pop(0)
                card_ids = [player_cards[0], ai_cards[0]]
                mark = NO_MARK
                next_card = False
                covered = True
                continue
            if whose_turn == "ai":
                category = ai_category(categories)
                covered = False
                winner = calc_winner(category, card_ids)
                
                #print(category)
                if winner == card_ids[0]:
                    color = GREEN
                    player_cards.append(ai_cards[0])
                    player_cards.append(player_cards[0])
                    n_player_cards += 1
                    n_ai_cards -= 1
                    whose_turn = "player"
                else:
                    color = RED
                    ai_cards.append(player_cards[0])
                    ai_cards.append(ai_cards[0])
                    n_ai_cards += 1
                    n_player_cards -= 1
                    whose_turn = "ai"

                mark = (color, "left", category)
                next_card = True
                #print(player_cards)
                #print(ai_cards)   
                
            else:
                mouse_pos = pygame.mouse.get_pos()
                category = chosen_category(mouse_pos)
                if category not in categories:
                    continue
                covered = False
                winner = calc_winner(category, card_ids)
                
                #print(category)
                if winner == card_ids[0]:
                    color = GREEN
                    player_cards.append(ai_cards[0])
                    player_cards.append(player_cards[0])
                    n_player_cards += 1
                    n_ai_cards -= 1
                    whose_turn = "player"
                else:
                    color = RED
                    ai_cards.append(player_cards[0])
                    ai_cards.append(ai_cards[0])
                    n_ai_cards += 1
                    n_player_cards -= 1
                    whose_turn = "ai"

                mark = (color, "left", category)
                next_card = True
                print(player_cards)
                print(ai_cards)
                
    
    
    
    
        
    pygame.display.flip()
    clock.tick(30)
