#tyrannen quartett
import sys
import pygame
import random
from collections import defaultdict
import numpy as np

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

IMG_PIX_X = 181
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

def calc_card_values(cards, categories):
    card_values = defaultdict(list)
    for category in categories:
        for card in cards.values():
            card_values[category].append(card[category])
    return card_values

card_values = calc_card_values(cards, categories)


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

def draw_turn(whose_turn):
    if whose_turn == "player":
        x = CARD_X_LEFT
    else:
        x = CARD_X_RIGHT

    rect = pygame.Rect(x, 0, IMG_PIX_X, IMG_Y_START - 5)
    pygame.draw.rect(screen, GREEN, rect)

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

def number_to_string(number):
    if number < 10000:
        return str(number)
    else:
        string = str(number)[::-1]
        new_string = ""
        for i, s in enumerate(string):
            new_string += s
            if i%3 == 2:
                new_string += "."
        if new_string[-1] == ".":
            return new_string[::-1][1:]
        return new_string[::-1]

def draw_values(id, pos):
    for i, category in enumerate(categories):
        draw_frame(card_xs[pos],
                   FRAME_Y_START + i*FRAME_HEIGHT,
                   IMG_PIX_X,
                   FRAME_HEIGHT)
        draw_text(card_xs[pos] + TEXT_X_OFFSET,
                  TEXT_Y_START + i*FRAME_HEIGHT,
                  number_to_string(cards[id][category]))



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

def ai_category(categories, card_values, ai_card):
    card = cards[ai_card]
    scores = []
    for category in categories:
        card_values_cat = np.array(card_values[category])
        card_value = card[category]
        if category == "Alter bei Machtübernahme":
            scores.append(np.mean(card_values_cat > card_value))
        else:
            scores.append(np.mean(card_values_cat < card_value))   
    return categories[np.argmax(scores)]

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


poss = ["left", "right"]

covered = True

NO_MARK = (False, False, False)

mark = NO_MARK

clock = pygame.time.Clock()

next_card = False

whose_turn = "player"

DIFFICULTIES = ["Anfänger", "Fortgeschrittener", "Profi", "Meister"]

def draw_difficulties(difficulties):
    for i, difficulty in enumerate(difficulties):
        draw_frame(0, 
                   float(i)/len(difficulties)*HEIGHT,
                   WIDTH,
                   HEIGHT/len(difficulties))
        draw_text(5, float(i)/len(difficulties)*HEIGHT + 10, difficulty)

def draw_difficulty(difficulty):
    draw_text(5, 5, "Schwierigkeitsgrad: {}".format(difficulty))

def choose_difficulty(difficulties, pos):
    for i, difficulty in enumerate(difficulties):
        if pos[1] > float(i)/len(difficulties)*HEIGHT and pos[1] < float(i+1)/len(difficulties)*HEIGHT:
            return difficulty

DIFFICULTY = False

while 1:
    screen.fill(WHITE)
    draw_difficulties(DIFFICULTIES)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            DIFFICULTY = choose_difficulty(DIFFICULTIES, mouse_pos)
    if DIFFICULTY:
        break
    pygame.display.flip()
    clock.tick(30)      

while 1:
    screen.fill(WHITE)
    draw_categories()
    draw_turn(whose_turn)
    draw_difficulty(DIFFICULTY)
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
                category = ai_category(categories, card_values, card_ids[1])
                covered = False
                winner = calc_winner(category, card_ids)
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
