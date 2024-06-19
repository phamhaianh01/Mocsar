import random
import pygame

class Card:
    def __init__(self, coord, number, tp, value):
        self.coord = coord
        self.number = number
        self.tp = tp
        self.value = value
        self.SIZE = (79,123)
        self.image = pygame.image.load("kartya.png")
        self.chosen = False
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        window.blit(self.image, (self.x, self.y), pygame.Rect(self.coord,self.SIZE))

    def is_over(self, pos, is_last):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + (self.SIZE[0] if is_last else self.SIZE[0] / 2):
            if pos[1] > self.y and pos[1] < self.y + self.SIZE[1]:
                return True
            
        return False
    
    def choose(self):
        self.chosen = not self.chosen
        if self.chosen:
            self.y -= 30
        else:
            self.y += 30
        return self.chosen


class Player:
    def __init__(self, cards, text_coord):
        self.cards = cards
        self.text_coord = text_coord
        self.chosen_cards = []
        self.skipped = False

    def defend(self, played_cards):
        defend_cards = []
        for i in range(len(self.cards)-len(played_cards)+1):
            if self.cards[i].value > played_cards[0].value:
                if self.cards[i].value == self.cards[i + len(played_cards)-1].value:
                    for k in range(len(played_cards)):
                        defend_cards.append(self.cards[i+k])
                    break

        print("Defend Cards:",len(defend_cards))
        self.remove_cards(defend_cards)
        return defend_cards

    def remove_cards(self, removed_cards):
        new_list = []
        self.chosen_cards = []
        for single_card in self.cards:
            if single_card not in removed_cards:
                new_list.append(single_card)
            else:
                self.chosen_cards.append(single_card)

        self.cards = new_list


    def draw(self, window, ranking):
        font = pygame.font.SysFont('comicsans',32)
        remaining_text = "Cards left: " + str(len(self.cards))
        rendered_text = font.render(remaining_text, 1, (255,255,255))
        window.blit(rendered_text, self.text_coord)

        if ranking != 0:
            rank_text = font.render('Rank ' + str(ranking), 1, (255,255,255))
            window.blit(rank_text, (self.text_coord[0], self.text_coord[1] + 40))
        
        for i, single_card in enumerate(self.chosen_cards):
            single_card.x = self.text_coord[0] + i*single_card.SIZE[0]/2
            single_card.y = self.text_coord[1] + 40 
            single_card.draw(window)
        if self.skipped:        
            skipped_text = font.render("Skipped", 1, (255,255,255))
            window.blit(skipped_text, (self.text_coord[0], self.text_coord[1] + 40))
            
        
    

    def attack(self):
        choosing = True
        attack_cards = []
        while choosing:
            number_of_cards = random.randint(1,4)
            for i in range(len(self.cards)-number_of_cards + 1):
                if self.cards[i].value == self.cards[i + number_of_cards - 1].value:
                    for k in range(number_of_cards):
                        attack_cards.append(self.cards[i+k])
                    choosing = False
                    break

        print("Attack card:", len(attack_cards))
        self.remove_cards(attack_cards)

        return attack_cards
                    
        

def shuffle_cards(): 
    f = open("kartyak.txt", "rt", encoding="utf-8")
    cards = []
    for x in f:
        x = x.split(":")
        temp = x[0].split(",")
        k = (int(temp[0]), int(temp[1]))
        s = x[1]
        t = x[2]
        e = int(x[3])
        cards.append(Card(k,s,t,e))
    f.close()
    random.shuffle(cards)
    #print(cards)

    standard_number = 3
    
    set1 = cards[0: standard_number]
    set1.sort(key = lambda item: item.value)
    set2 = cards[standard_number: standard_number * 2]
    set2.sort(key = lambda item: item.value)
    set3 = cards[standard_number * 2: standard_number * 3]
    set3.sort(key = lambda item: item.value)
    set4 = cards[standard_number * 3: standard_number * 4]
    set4.sort(key = lambda item: item.value)

    return set1, set2, set3, set4
    
