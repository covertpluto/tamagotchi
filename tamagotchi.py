import random
import time
import math
import os

class TamagotchiGraphic:
    def __init__(self, type):
        self.__type = type

    def fetch_graphic(self):
        filename = f"{self.__type.lower()}.txt"
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")

    def get_graphic(self):
        return self.fetch_graphic().split("\n")

    def print_graphic(self):
        for i in self.get_graphic():
            for j in i:
                print("." if j == "1" else " ", end="")
            print()



class Tamagotchi:
    def __init__(self):
        # public

        self.type = "Babytchi"

        # private
        self._health = 100
        self._happiness = 100
        self._energy = 100
        self._hygiene = 100
        self._age = 0  # days
        self._weight = 0
        self._intelligence = 0
        self._birth = time.time()  # time when born
        self._abs_age = time.time()  # time since created
        self._is_asleep = False
        self._name = ""
        self._life_stage = 0
        self._last_check_in = time.time()

    def set_name(self, name):
        self._name = name
    def export_data(self):
        return {
            "name": self._name,
            "abs_age": self._abs_age,
            "birth": self._birth
        }

    def next(self):
        if "devconfig" in os.listdir("./"):
            stage_0_time = 5
            stage_1_time = 10
        else:
            stage_0_time = 30
            stage_1_time = 60
        if self._life_stage == 0 and time.time() - self._abs_age > stage_0_time:

            return Marutchi()
        if self._life_stage == 1 and time.time() - self._abs_age > stage_1_time:
            if self._hygiene > 75 and self._happiness > 75:
                return Tamatchi()
            else:
                return Kuchitamachi()
        return self


    def import_data(self, data):
        self._name = data["name"]
        self._abs_age = data["abs_age"]
        self._birth = data["birth"]

    def feed(self):
        # increase the energy level by 10
        self._energy += 10 if self._energy <= 90 else 0

        # have a 1% chance of growing by 1
        if random.random() < 0.01:
            self._weight += 1

    def medicine(self):
        # if the health is below 20 increase the health by 10
        # if the health is between 20 and 80 increase the health by 5
        # if the health is above 80 do nothing
        if self._health < 20:
            self._health += 10
        elif 20 <= self._health <= 90:
            self._health += 5

    def wash(self):
        # set the hygiene level to 100
        self._hygiene = 100

    def play(self):
        if self._happiness <= 95:
            self._happiness += 5
        else:
            self._happiness = 100
        self._energy -= 5

    def sleep(self):
        self._is_asleep = True

    def wake_up(self):
        self._is_asleep = False
        if self._energy > 95:
            self._energy = 100
        if self._health <= 90:
            self._health += 10  # sleep to recover!
        if self._happiness >= 90:
            self._intelligence += 1

    def get_dead(self):
        return self._health <= 0

    def get_offline_time(self):
        return int(time.time() - self._last_check_in)

    def tick(self):
        if self._is_asleep:
            self._last_check_in = time.time()
            return
        self._last_check_in = time.time()

        # randomly decrement the health
        if random.random() > 0.9995:
            self._health -= 1
        if self._health <= 0:
            self._health = 0
        self._energy -= 0.01 if self._energy > 1 else 0
        self._hygiene -= 0.01 if self._hygiene > 1 else 0
        self._happiness -= 0.01 if self._happiness > 1 else 0



        if self._energy < 0:
            self._health -= 1

        current_time = time.time()
        self._age = math.floor((current_time - self._birth))

    def hatch(self):
        self._birth = time.time()

    def get_health(self):
        return str(int(self._health)) + " %"

    def get_happiness(self):
        return str(int(self._happiness)) + " %"

    def get_energy(self):
        return str(int(self._energy)) + " %"

    def get_hygiene(self):
        return str(int(self._hygiene)) + " %"

    def get_age(self):
        if self._age > 31536000:
            return str(int(self._age / 31536000)) + " YEAR"
        if self._age > 86400:
            return str(int(self._age / 86400)) + " DAY"
        if self._age > 3600:
            return str(int(self._age / 3600)) + " HOUR"
        if self._age > 60:
            return str(int(self._age / 60)) + " MINUTE"
        return str(int(self._age)) + " SECOND"

    def get_weight(self):
        return self._weight

    def get_intelligence(self):
        return self._intelligence

    def get_is_asleep(self):
        return self._is_asleep

    def get_type(self):
        return self.type

    def set_health(self, health):
        self._health = health

    def set_happiness(self, happiness):
        self._happiness = happiness

    def set_energy(self, energy):
        self._energy = energy

    def set_hygiene(self, hygiene):
        self._hygiene = hygiene

    def set_age(self, age):
        self._age = age

    def set_weight(self, weight):
        self._weight = weight

    def set_intelligence(self, intelligence):
        self._intelligence = intelligence

    def set_is_asleep(self, is_asleep):
        self._is_asleep = is_asleep


# define some tamagotchi variants

class Marutchi(Tamagotchi):
    def __init__(self):
        super().__init__()
        self._intelligence = 1

        self.type = "Marutchi"
        self._life_stage = 1

    def tick(self):
        if self._is_asleep:
            return

        # randomly decrement the health
        self._health -= random.choice([0] * 70 + [1] * 10 + [2] * 5 + [3] * 5 + [5] * 3 + [10] * 2 + [20] * 1 + [50])
        self._energy -= 5  # hungry!
        self._hygiene -= 1
        self._happiness -= 1

        current_time = time.time()

        self._age = math.floor((current_time - self._birth))

class Tamatchi(Tamagotchi):
    def __init__(self):
        super().__init__()
        self._intelligence = 5
        self._life_stage = 2
        self.type = "tamatchi"

class Kuchitamachi(Tamagotchi):
    def __init__(self):
        super().__init__()
        self._intelligence = 2
        self._life_stage = 2
        self.type = "kuchitamachi"