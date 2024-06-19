from pygame import *
import pygame.gfxdraw
import sys
import random
import button
import card
import menu
from os import path

def generate_text(ranking):
    for i, v in enumerate(ranking):
        if v == 4:
            last = i
        elif v == 1:
            first = i
            
    if last == 0:
        last_text = 'You'
    else:
        last_text = 'Player ' + str(last)

    if first == 0:
        first_text = 'You'
    else:
        first_text = 'Player ' + str(first)

    return first_text, last_text
    

def render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn):
    window.blit(background, (0,0))
    font = pygame.font.SysFont('comicsans',32)
    if turn == 0 and is_playing[0]:
        turn_text = font.render('Your turn', 1, (0,0,0))
    else:
        turn_text = font.render('Player '+str(turn)+"'s turn", 1, (0,0,0))

    if 0 not in ranking:
        first_text, last_text = generate_text(ranking)
        penalty_text = font.render('Best card from {0} is going to {1}'.format(last_text, first_text), 1, (0,0,0))
        penalty_text2 = font.render('Worst card from {1} is going to {0}'.format(last_text, first_text), 1, (0,0,0))
        restart_button.draw(window,(255,0,0))
        window.blit(penalty_text, (160, 295 + 60))
        window.blit(penalty_text2, (160, 295 + 90))
    else:
        if turn == 0 and is_playing[0]:
            card_confirm.draw(window, (255,0,0))
            pass_button.draw(window, (255,0,0))
            save_button.draw(window, (255,0,0))
            quit_button.draw(window, (255,0,0))
        window.blit(turn_text, (310, 295))
    
    players[0].draw(window, ranking[1])
    players[1].draw(window, ranking[2])
    players[2].draw(window, ranking[3])

    if ranking[0] != 0:
        rank_text = font.render("Rank " + str(ranking[0]), 1, (255,255,255))
        window.blit(rank_text, (310,450))
    elif len(our_played_cards) == 0 and is_playing[0] == False:
        skipped_text = font.render("Skipped", 1, (255,255,255))
        window.blit(skipped_text, (310,450))
    else:
        for i, single_card in enumerate(our_played_cards):
            single_card.x = 310 + i*single_card.SIZE[0] / 2
            single_card.y = 500 - single_card.SIZE[1]
            single_card.draw(window)
            
    # render your cards
    for i, single_card in enumerate(your_set):
        single_card.draw(window)

    pygame.display.update()

def end_of_round(playing):
    false_count = 0
    for i in playing:
        if i is False:
            false_count += 1

    return false_count == 3

def card_switch(first, last):
    first.append(last[len(last)-1])
    last.pop()
    last.append(first[0])
    first.pop(0)
    last.sort(key = lambda item: item.value)
    first.sort(key = lambda item: item.value)

def remove(index, chosen_cards):
    new_list = []
    for v in chosen_cards:
        if v != index:
            new_list.append(v)

    return new_list

def remove_multiple(chosen_cards, your_set):
    new_list = []
    for i, single_card in enumerate(your_set):
        if i not in chosen_cards:
            new_list.append(single_card)

    return new_list
        

def is_valid(chosen_cards, new_card_i, your_set, played_cards):
    #Unselect the card
    if new_card_i in chosen_cards:
        return True
    #Start of the round selection
    if len(played_cards) == 0:
        if len(chosen_cards) == 0:
            return True
        if your_set[chosen_cards[0]].value == your_set[new_card_i].value:
            return True
    #Defending against another player's card
    if len(played_cards) > 0:
        if len(chosen_cards) == 0 and your_set[new_card_i].value > played_cards[0].value:
            return True
        #Selecting multiple
        if len(chosen_cards) > 0 and len(chosen_cards) < len(played_cards) and your_set[chosen_cards[0]].value == your_set[new_card_i].value:
            return True
        
    return False

def save_game(your_set, players, is_playing, ranking, played_cards):
    save_file = open("saved_data.txt", "w", encoding='utf-8')
    save_file.write(str(len(your_set)) + '\n')
    for card in your_set:
        save_file.write('{0},{1}:{2}:{3}:{4}\n'.format(card.coord[0], card.coord[1], card.number, card.tp, card.value))
    i = 1
    for i, player in enumerate(players):
        save_file.write(str(len(player.cards)) + '\n')
        for card in player.cards:
            save_file.write('{0},{1}:{2}:{3}:{4}\n'.format(card.coord[0], card.coord[1], card.number, card.tp, card.value))
        save_file.write(str(len(player.chosen_cards)) + '\n')
        for chosen_card in player.chosen_cards:
            save_file.write('{0},{1}:{2}:{3}:{4}\n'.format(chosen_card.coord[0], chosen_card.coord[1], chosen_card.number, chosen_card.tp, chosen_card.value))
        save_file.write(str(is_playing[i+1]) + '\n')
        save_file.write(str(ranking[i+1]) + '\n')

    save_file.write(str(len(played_cards)) + '\n')
    for card in played_cards:
        save_file.write('{0},{1}:{2}:{3}:{4}\n'.format(card.coord[0], card.coord[1], card.number, card.tp, card.value))
    save_file.close()

def continue_game():
    playing = [True]*4
    ranking = [0]*4
    with open("saved_data.txt", "rt", encoding='utf-8') as reader:
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        my_cards = read_cards(number_of_cards, reader)
        
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        player2_cards = read_cards(number_of_cards, reader)
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        player2_chosen_cards = read_cards(number_of_cards, reader)
        playing[1] = reader.readline()[:4] == 'True'
        ranking[1] = int(reader.readline())
        
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        player3_cards = read_cards(number_of_cards, reader)
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        player3_chosen_cards = read_cards(number_of_cards, reader)
        playing[2] = reader.readline()[:4] == 'True'
        ranking[2] = int(reader.readline())
        
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        player4_cards = read_cards(number_of_cards, reader)
        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        player4_chosen_cards = read_cards(number_of_cards, reader)
        playing[3] = reader.readline()[:4] == 'True'
        ranking[3] = int(reader.readline())

        number_of_cards = reader.readline()
        number_of_cards = int(number_of_cards)
        played_cards = read_cards(number_of_cards, reader)

    rank = 0
    first_place = -1
    for i in ranking:
        if i > rank:
            rank = i
        if i == 1:
            first_place = i

    players = [card.Player(player2_cards, (600,150)), card.Player(player3_cards, (310,5)), card.Player(player4_cards, (10,150))]
    players[0].chosen_cards = player2_chosen_cards
    players[1].chosen_cards = player3_chosen_cards
    players[2].chosen_cards = player4_chosen_cards
        
    rank += 1
    return my_cards, players, played_cards, playing, ranking, rank, first_place

    

def read_cards(number_of_cards, reader):
    loaded_cards = []
    for i in range(number_of_cards):
        card_line = reader.readline()
        card_line = card_line.split(':')
        coord_array = card_line[0].split(',')
        coord = (int(coord_array[0]), int(coord_array[1]))
        number = card_line[1]
        tp = card_line[2]
        value = int(card_line[3])
        loaded_cards.append(card.Card(coord, number, tp, value))

    return loaded_cards
            
    

def main():
    #Initialize the game state variable (your_set, players, is_playing...)
    your_set, set2, set3, set4 = card.shuffle_cards()
    players = [card.Player(set2, (600,150)), card.Player(set3, (310,5)), card.Player(set4, (10,150))]
    is_playing = [True]*4
    ranking = [0] * 4
    rank = 1
    first_place = -1
    played_cards = []

    #init graphic
    pygame.init()
    window = pygame.display.set_mode((800,640))
    pygame.display.set_caption('Mocsár')
    
    #Handle the menu
    while True:
        menu_action = menu.menu(pygame, window)
        if menu_action == 2:
            if path.exists('saved_data.txt'):
                your_set, players, played_cards, is_playing, ranking, rank, first_place = continue_game()
            break
        elif menu_action == 1:
            break
    # 0 : your turn, 1: player1 turn, ... 4: player4 turn
    turn = 0
    running = True
    last_place = -1

    #set up background and buttons
    background = pygame.image.load("palya.png")
    card_confirm = button.Button((255,255,255), 710, 560, 80, 20, 'Play')
    pass_button = button.Button((255,255,255), 710, 590, 80, 20, 'Pass')
    save_button = button.Button((255,255,255), 5, 560, 80, 20, 'Save')
    quit_button = button.Button((255,255,255), 5, 590, 80, 20, 'Quit')
    restart_button = button.Button((255,255,255), 800/2 - 100, 640/2 - 25, 200, 50, 'Restart')

    our_played_cards = []
    last_to_play = 0

    for i, single_card in enumerate(your_set):
        single_card.set_position(110+i*40, 640-123)

    while running:
        '''
        for i in range(4):
            print(i+1, "rank: ", ranking[i])
        for  v in played_cards:
            print(v.number, v.tp, v.value)
        for i in range(4):
            print(i+1, "playing: ", is_playing[i])
        '''
        render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn)

        #Check if everybody has a rank
        while 0 not in ranking:
            event = pygame.event.wait()
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                restart_button.is_over(mouse_pos)
                render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn)
                
            #Press the restart button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and restart_button.is_over(mouse_pos) and 0 not in ranking:
                #Assign the new turn to the 1st ranked player
                turn = first_place

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #Reset the game
                your_set, set2, set3, set4 = card.shuffle_cards()
                players = [card.Player(set2, (600,150)), card.Player(set3, (310,5)), card.Player(set4, (10,150))]
                is_playing = [True]*4
                played_cards = []
                our_played_cards = []
                last_to_play = 0
                ranking = [0] * 4
                rank = 1
                #Lowest (4th) ranked player has to give the highest card to 1st ranked player
                if last_place == 0:
                    card_switch(players[first_place-1].cards, your_set)
                elif first_place == 0:
                    card_switch(your_set, players[last_place-1].cards)
                else:
                    card_switch(players[first_place-1].cards, players[last_place-1].cards)

                for i, single_card in enumerate(your_set):
                    single_card.set_position(110+i*40, 640-123)                    
        render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn)

        #Your turn  
        chosen_cards = []
        while turn == 0 and is_playing[0]:
            event = pygame.event.wait()
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEMOTION:
                save_button.is_over(mouse_pos)
                pass_button.is_over(mouse_pos)
                card_confirm.is_over(mouse_pos)
                quit_button.is_over(mouse_pos)
                render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn)

            #Press the quit button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and quit_button.is_over(mouse_pos) or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #Press the save button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and save_button.is_over(mouse_pos):
                save_game(your_set, players, is_playing, ranking, played_cards)
            #Press the pass button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and pass_button.is_over(mouse_pos):
                our_played_cards = []
                for i, single_card in enumerate(your_set):
                    if i in chosen_cards:
                        single_card.choose()
                is_playing[0] = False
                turn += 1
                
            #Press the play button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and card_confirm.is_over(mouse_pos) and \
               (len(played_cards) == 0 and len(chosen_cards) > 0 or len(played_cards) > 0 and len(played_cards) == len(chosen_cards)):
                played_cards = []
                our_played_cards = []
                if len(your_set) > 0:
                    last_to_play = 0
                for i in chosen_cards:
                    played_cards.append(your_set[i])
                    our_played_cards.append(your_set[i])
                    
                your_set = remove_multiple(chosen_cards, your_set)
                turn += 1

            #logic for your turn
            for i, single_card in enumerate(your_set):
                if event.type == pygame.MOUSEBUTTONDOWN and single_card.is_over(mouse_pos, i == len(your_set)-1 ):
                    
                    if not is_valid(chosen_cards, i, your_set, played_cards):
                        break
                    
                    if single_card.choose():
                        #print("Log ",chosen_cards)
                        chosen_cards.append(i)
                    else:
                        chosen_cards = remove(i, chosen_cards)
                    #print(chosen_cards)    
                    render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn)
                    #print(single_card.number, single_card.tp, " clicked!")
                    
            #Determine the rank for you
            if len(your_set) == 0 and ranking[0] == 0:
                ranking[0] = rank
                if rank == 1:
                    first_place = 0
                elif rank == 4:
                    last_place = 0
                rank += 1
                is_playing[0] = False

        render(window, background, your_set, our_played_cards, card_confirm, pass_button, save_button, quit_button, restart_button, players, is_playing, ranking, turn)
        #print("Turn: "+ str(turn))
        
        #End of Round for you
        #print("Did it end?",end_of_round(is_playing))
        if end_of_round(is_playing):
            if rank == 4:
                for i, v in enumerate(ranking):
                    if v == 0:
                        ranking[i] = rank
            for i in range(4):
                is_playing[i] = ranking[i] == 0
            for i in range(len(players)):
                players[i].skipped = False
            played_cards = []
            turn = last_to_play
            our_played_cards = []
            continue
        
        if not is_playing[turn]:
            turn = (turn + 1) % 4
            continue
        
        # do something with AI
        pygame.time.wait(1000)
        #Player starts with random card
        if last_to_play == turn or len(played_cards) == 0:
            player_chosen_cards = players[turn-1].attack()
        #Player chooses card to defend
        else:
            player_chosen_cards = players[turn-1].defend(played_cards)

        #Player Skipped    
        if len(player_chosen_cards) == 0:
            #print("Player Skipped!!!!", turn)
            is_playing[turn] = False
            players[turn-1].skipped = True
        #Player Defended/Attacked
        else:
            #print('Defended or Attacked!!!!', turn)
            played_cards = player_chosen_cards
            if len(players[turn-1].cards) > 0:
                last_to_play = turn
                

        #Determine the rank for other players
        if len(players[turn-1].cards) == 0 and ranking[turn] == 0:
            #print("Assigned rank", len(players[turn-1].cards))
            ranking[turn] = rank
            if rank == 1:
                first_place = turn
            elif rank == 4:
                last_place = turn
            rank += 1
            is_playing[turn] = False

        #End of Round for AI
        #print("Did it end?",end_of_round(is_playing))
        if end_of_round(is_playing):
            if rank == 4:
                for i, v in enumerate(ranking):
                    if v == 0:
                        ranking[i] = rank
            for i in range(4):
                is_playing[i] = ranking[i] == 0
            for i in range(len(players)):
                players[i].skipped = False
                players[i].chosen_cards = []
            played_cards = []
            turn = last_to_play
            our_played_cards = []
            continue
        
        turn = (turn + 1) % 4
        
    #print out the score board before we quit
    while True:
        pass


main()
