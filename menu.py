import random
import button
import sys
from os import path

def menu(pygame, window):
    
    newgame = button.Button((255,255,255), 300, 180, 200, 50, 'New Game')
    loadgame = button.Button((255,255,255), 300, 250, 200, 50, 'Continue')
    
    running = True
    
    while running:
        event = pygame.event.wait()
        pos = pygame.mouse.get_pos()
        window.fill((127,127,127))
        
        newgame.draw(window, (0,0,0))
        loadgame.draw(window, (0,0,0))
        if path.exists("saved_data.txt"):
            font = pygame.font.SysFont('comicsans', 32)
            load_text = font.render('A saved game exists', 1, (0,0,0))
        else:
            font = pygame.font.SysFont('comicsans', 32)
            load_text = font.render('No saved game exists', 1, (0,0,0))

        window.blit(load_text, (290, 340))
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print('Press')
            if newgame.is_over(pos):
                print('New game')
                return 1
            if loadgame.is_over(pos):
                print('Load Game')
                return 2

        if event.type == pygame.MOUSEMOTION:
            newgame.is_over(pos)
            loadgame.is_over(pos)
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
