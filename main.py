from pygame.locals import *
import math
import random
import tamagotchi
import os
import pickle
import time
import fontdisplay
import pygame
import sys
import threading


def load():
    all_files = os.listdir("./")
    possible_files = [i for i in all_files if i[-4:] == ".bin"]
    opened = False
    for p in possible_files:
        try:
            with open(p, "rb") as f:
                data = pickle.load(f)
                opened = True

                break
        except:
            pass
    if not opened:
        return tamagotchi.Tamagotchi()
    else:
        return data


def save(data):
    with open(f"save.bin", "wb") as f:
        pickle.dump(data, f)


running = True
pygame.font.init()
my_font = pygame.font.SysFont('./Roboto-Regular.ttf', 30)

programIcon = pygame.image.load('icon.png')

pygame.display.set_icon(programIcon)
reload_waiting = True
pygame.init()
current_state = "idle"
surface = pygame.display.set_mode((450, 520))

LCD_BACKGROUND = (207, 241, 69)
PIXEL_SIZE = 5
display_delay = 0

static_image_overwritten = True


def clear_lcd():
    pygame.draw.rect(surface, LCD_BACKGROUND, (25, 25, 400, 400))


def lcd_matrix(matrix, x=0, y=0, pixel_size=10, pixel_colour=(53, 78, 0), xy_override=[]):
    global static_image_overwritten
    static_image_overwritten = True
    x = 25 + x * pixel_size
    y = 25 + y * pixel_size
    if len(xy_override) == 2:
        x = xy_override[0]
        y = xy_override[1]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "1":
                pygame.draw.rect(surface, pixel_colour,
                                 (x + j * pixel_size, y + i * pixel_size, pixel_size, pixel_size))
                pygame.display.flip()
                time.sleep(display_delay)


class PyGameButton:

    def __init__(self, x, y, width, height, colour, text=""):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.text = text

    def draw(self):

        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))
        for j in self.text:
            start_x = self.x + self.width / 2 - 2.5 * PIXEL_SIZE
            start_y = self.y + self.height / 2 - 2.5 * PIXEL_SIZE
            lcd_matrix(fontdisplay.letters[j[0]], pixel_colour=(0, 0, 0), xy_override=[start_x, start_y],
                       pixel_size=PIXEL_SIZE)

    def is_pressed(self, mouse):
        if self.x < mouse[0] < self.x + self.width:
            if self.y < mouse[1] < self.y + self.height:
                return True
        return False


BUTTON_COLOUR = (127, 127, 127)

back = PyGameButton(0, 460, 147, 60, BUTTON_COLOUR, "<")
select = PyGameButton(152, 460, 147, 60, BUTTON_COLOUR, "~")
next = PyGameButton(304, 460, 147, 60, BUTTON_COLOUR, ">")

buttons = [next, select, back]

[button.draw() for button in buttons]


def lcd_text(text, x, y):
    print("painted")
    threshold = int(400 / (PIXEL_SIZE * len(fontdisplay.letters[text[0]][0]))) - 3
    if len(text) <= threshold:
        start_x = 0
        for char in text:
            char_glyph = fontdisplay.letters[char]
            lcd_matrix(char_glyph, x + start_x, y, PIXEL_SIZE)
            start_x += len(char_glyph[0]) + 1

    else:
        start_x = 0

        for char in text[0:(threshold - 1)]:
            char_glyph = fontdisplay.letters[char]
            lcd_matrix(char_glyph, x + start_x, y, PIXEL_SIZE)
            start_x += len(char_glyph[0]) + 1
        lcd_text(text[(threshold - 1):], x, y + len(char_glyph[0]) + 1)


pygame.display.flip()
running = True


def stats():
    timeout = time.time()
    global current_state
    current_state = "menu"
    print("Enter Menu")
    clear_lcd()
    menuitems = ["HEALTH", "HAPPINESS", "ENERGY", "HYGIENE", "AGE", "WEIGHT", "INTELLIGENCE"]
    current_item = 0
    txt = " "

    match menuitems[current_item]:
        case "HEALTH":
            txt = str(current_tamagotchi.get_health())
        case "HAPPINESS":
            txt = str(current_tamagotchi.get_happiness())
        case "ENERGY":
            txt = str(current_tamagotchi.get_energy())
        case "HYGIENE":
            txt = str(current_tamagotchi.get_hygiene())
        case "AGE":
            txt = str(current_tamagotchi.get_age())
        case "WEIGHT":
            txt = str(current_tamagotchi.get_weight())
        case "INTELLIGENCE":
            txt = str(current_tamagotchi.get_intelligence())
    txt = txt[0:8]
    print(txt)
    lcd_text(txt, 2, 40)
    lcd_text(menuitems[current_item], 2, 5)
    in_menu = True
    global running
    while in_menu and running:

        if current_state == "menu":
            run_tamagotchi()
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, buttonID in zip(buttons, ["next", "select", "back"]):
                    if button.is_pressed(mouse):
                        timeout = time.time()

                        if buttonID == "next":

                            if current_item == len(menuitems) - 1:
                                current_item = 0
                            else:
                                current_item += 1

                            clear_lcd()
                            lcd_text(menuitems[current_item], 2, 5)
                            txt = " "

                            match menuitems[current_item]:
                                case "HEALTH":
                                    txt = str(current_tamagotchi.get_health())
                                case "HAPPINESS":
                                    txt = str(current_tamagotchi.get_happiness())
                                case "ENERGY":
                                    txt = str(current_tamagotchi.get_energy())
                                case "HYGIENE":
                                    txt = str(current_tamagotchi.get_hygiene())
                                case "AGE":
                                    txt = str(current_tamagotchi.get_age())
                                case "WEIGHT":
                                    txt = str(current_tamagotchi.get_weight())
                                case "INTELLIGENCE":
                                    txt = str(current_tamagotchi.get_intelligence())
                            txt = txt[0:8]
                            print(txt)
                            lcd_text(txt, 2, 40)

                        if buttonID == "select":
                            in_menu = False

                        if buttonID == "back":
                            if current_item == 0:
                                current_item = len(menuitems) - 1
                            else:
                                current_item -= 1

                            clear_lcd()
                            lcd_text(menuitems[current_item], 2, 5)
                            txt = " "

                            match menuitems[current_item]:
                                case "HEALTH":
                                    txt = str(current_tamagotchi.get_health())
                                case "HAPPINESS":
                                    txt = str(current_tamagotchi.get_happiness())
                                case "ENERGY":
                                    txt = str(current_tamagotchi.get_energy())
                                case "HYGIENE":
                                    txt = str(current_tamagotchi.get_hygiene())
                                case "AGE":
                                    txt = str(current_tamagotchi.get_age())
                                case "WEIGHT":
                                    txt = str(current_tamagotchi.get_weight())
                                case "INTELLIGENCE":
                                    txt = str(current_tamagotchi.get_intelligence())
                            txt = txt[0:8]
                            print(txt)
                            lcd_text(txt, 2, 40)
    print("Menu quit")
    current_state = "idle"


def lcd_menu():
    timeout = time.time()
    global display_delay
    global current_state
    current_state = "menu"
    global current_tamagotchi
    global reload_waiting
    print("Enter Menu")
    menuitems = ["STATS", "SLEEP/UNSLEEP", "FEED", "PLAY", "MEDICINE", "SAVE", "BACK", "RESET AND EXIT"]
    current_item = 0
    clear_lcd()
    lcd_text(menuitems[current_item], 2, 5)
    in_menu = True
    global running

    while time.time() - timeout < 10 and in_menu:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button, buttonID in zip(buttons, ["next", "select", "back"]):
                    if button.is_pressed(mouse):
                        timeout = time.time()

                        if buttonID == "next":

                            if current_item == len(menuitems) - 1:
                                current_item = 0
                            else:
                                current_item += 1

                            clear_lcd()
                            lcd_text(menuitems[current_item], 2, 5)

                            match menuitems[current_item]:
                                case "FEED":
                                    print("FEED")
                                    food = current_tamagotchi.get_energy()
                                    lcd_text(food, 2, 40)
                                case "MEDICINE":
                                    print("MEDICINE")
                                    med = current_tamagotchi.get_health()
                                    lcd_text(med, 2, 40)
                                case "PLAY":
                                    print("HAPPINESS")
                                    happ = current_tamagotchi.get_happiness()
                                    lcd_text(happ, 2, 40)
                                case "SLEEP/UNSLEEP":
                                    print("SLEEP")
                                    s = current_tamagotchi.get_is_asleep()
                                    if s:
                                        lcd_text("SLEEPING", 2, 40)
                                    else:
                                        lcd_text("AWAKE", 2, 40)

                        if buttonID == "select":
                            clear_lcd()
                            lcd_text(menuitems[current_item], 2, 5)

                            match menuitems[current_item]:
                                case "FEED":
                                    print("FEED")
                                    food = current_tamagotchi.get_energy()
                                    lcd_text(food, 2, 40)
                                case "MEDICINE":
                                    print("MEDICINE")
                                    med = current_tamagotchi.get_health()
                                    lcd_text(med, 2, 40)
                                case "PLAY":
                                    print("HAPPINESS")
                                    happ = current_tamagotchi.get_happiness()
                                    lcd_text(happ, 2, 40)
                                case "SLEEP/UNSLEEP":
                                    print("SLEEP")
                                    s = current_tamagotchi.get_is_asleep()
                                    if s:
                                        lcd_text("SLEEPING", 2, 40)
                                    else:
                                        lcd_text("AWAKE", 2, 40)

                            if menuitems[current_item] == "STATS":
                                print("STATS")
                                stats()
                                clear_lcd()
                                lcd_text(menuitems[current_item], 2, 5)
                            if menuitems[current_item] == "FEED":
                                print("FEED")
                                current_tamagotchi.feed()
                            if menuitems[current_item] == "PLAY":
                                print("PLAY")
                                current_tamagotchi.play()
                            if menuitems[current_item] == "SLEEP/UNSLEEP":
                                print("SLEEP")
                                current_tamagotchi.set_is_asleep(not current_tamagotchi.get_is_asleep())
                                in_menu = False
                            if menuitems[current_item] == "MEDICINE":
                                print("MEDICINE")
                                current_tamagotchi.medicine()
                            if menuitems[current_item] == "SAVE":
                                print("SAVE")
                                save(current_tamagotchi)
                                clear_lcd()
                                lcd_text("SAVED", 2, 5)
                                time.sleep(1)
                                clear_lcd()
                                lcd_text(menuitems[current_item], 2, 5)
                            if menuitems[current_item] == "BACK":
                                print("BACK")
                                in_menu = False
                            if menuitems[current_item] == "RESET AND EXIT":
                                print("RESET")
                                in_menu = False
                                running = False

                                clear_lcd()
                                lcd_text("PLEASE DELETE THE SAVE.BIN FILE", 2, 5)
                                time.sleep(2)

                                clear_lcd()
                                display_delay = 0.01
                                lcd_matrix(tamagotchi.TamagotchiGraphic("death").get_graphic(), 0, 0,
                                           pixel_size=PIXEL_SIZE)
                                time.sleep(5)

                        if buttonID == "back":

                            if current_item == 0:
                                current_item = len(menuitems) - 1
                            else:
                                current_item -= 1

                            clear_lcd()
                            lcd_text(menuitems[current_item], 2, 5)

                            match menuitems[current_item]:
                                case "FEED":
                                    print("FEED")
                                    food = current_tamagotchi.get_energy()
                                    lcd_text(food, 2, 40)
                                case "MEDICINE":
                                    print("MEDICINE")
                                    med = current_tamagotchi.get_health()
                                    lcd_text(med, 2, 40)
                                case "PLAY":
                                    print("HAPPINESS")
                                    happ = current_tamagotchi.get_happiness()
                                    lcd_text(happ, 2, 40)
                                case "SLEEP/UNSLEEP":
                                    print("SLEEP")
                                    s = current_tamagotchi.get_is_asleep()
                                    if s:
                                        lcd_text("SLEEPING", 2, 40)
                                    else:
                                        lcd_text("AWAKE", 2, 40)
    print("Menu quit")
    current_state = "idle"


m = tamagotchi.TamagotchiGraphic("tamatchi").get_graphic()
lcd_text("LOADING...", 2, 30)

last_update = time.time()
idle_x = 10
idle_y = 10
sleep_z_pos = [
    [30, 50],
    [50, 40],
    [70, 30]
]
sleep_z_index = 0
stopped = False


def idle_screen():
    global m
    global last_update
    global idle_y
    global idle_x
    global sleep_z_index
    global display_delay
    global stopped
    global current_state
    global static_image_overwritten
    pygame.display.set_caption("Tamagotchi - " + current_tamagotchi.get_type() + " Health: " + str(current_tamagotchi.get_health()))

    if current_tamagotchi.get_dead():
        if static_image_overwritten:
            current_state = "idle"
            print("DEAD")
            clear_lcd()
            display_delay = 0.0001
            lcd_matrix(tamagotchi.TamagotchiGraphic("death").get_graphic(), 0, 0, pixel_size=PIXEL_SIZE)
            static_image_overwritten = False
        return

    m = tamagotchi.TamagotchiGraphic(current_tamagotchi.get_type()).get_graphic()
    if last_update + 1 < time.time():
        if current_tamagotchi.get_is_asleep():
            if sleep_z_index < 2:
                sleep_z_index += 1
            else:
                sleep_z_index = 0
            clear_lcd()
            flipped = list(zip(*m[::-1]))
            lcd_matrix(flipped, 20, 55, PIXEL_SIZE)
            lcd_text("Z", sleep_z_pos[sleep_z_index][0], sleep_z_pos[sleep_z_index][1])

        else:

            if random.random() > 0.5:
                m = [n[::-1] for n in m]

            if idle_x < 50:
                idle_x += 1
            else:
                idle_x = 0
                if idle_y < 50:
                    idle_y += 5
                else:
                    idle_y = 0

            clear_lcd()

            print("tick")
            lcd_matrix(m, idle_x, idle_y, PIXEL_SIZE)
        last_update = time.time()


clear_lcd()

last_tamagotchi_update = time.time()


def run_tamagotchi():
    global current_tamagotchi
    global last_tamagotchi_update
    if last_tamagotchi_update + 1 < time.time():
        t = current_tamagotchi
        print("RUN TAMAGOTCHI")
        t.tick()
        if t.next().get_type() != t.get_type():
            print("Your tamagotchi has become a ", t.next().get_type())
            t_old = t.export_data()
            current_tamagotchi = t.next()
            current_tamagotchi.import_data(t_old)
        last_tamagotchi_update = time.time()


def run_main():
    global running
    global current_state
    current_state = "idle"
    while running:
        mouse = pygame.mouse.get_pos()
        run_tamagotchi()
        idle_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:

                for button, buttonID in zip(buttons, ["next", "select", "back"]):
                    if button.is_pressed(mouse):
                        print("pressed", buttonID)

                        lcd_menu()
    print("QUIT")
    save(current_tamagotchi)


try:
    while reload_waiting:
        reload_waiting = False
        current_tamagotchi = load()
        current_state = "loading"
        for i in range(current_tamagotchi.get_offline_time()):
            current_tamagotchi.tick()
        run_main()
except KeyboardInterrupt:
    try:
        save(current_tamagotchi)
    except Exception as e:
        print(e)
