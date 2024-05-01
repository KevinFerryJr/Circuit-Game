import pygame
import os
import sys
from utils import *
import grid

# Constants
WIDTH  = grid.TILE_SIZE*grid.GRID_WIDTH 
HEIGHT = grid.TILE_SIZE*grid.GRID_HEIGHT
FPS = 30

#Player Instance (Playes selection in the grid)
selection_indicator = grid.Selection_Indicator((0, 0))
    
tilemap = grid.Tilemap(grid.map_data)

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Circuit")
    clock = pygame.time.Clock()

    #Sprites
    all_sprites = pygame.sprite.Group()
    all_sprites.add(selection_indicator)

    #Main Game Loop
    running = True
    while running:

        #Handle Input
        for event in pygame.event.get():
            running = event_handler(event)
        
        #Draw the image (not yet visible)
        screen.fill(BG_COLOR)
        tilemap.draw(screen)
        all_sprites.draw(screen)
        
        #Diaplay and Tick (make it visible and tick the clock)
        pygame.display.flip()
        clock.tick(FPS)

    #Shutdown Routine
    pygame.quit()
    sys.exit()

def event_handler(event):
    #if Window exit button is pressed
    if event.type == pygame.QUIT:
        return False

    #Called ONCE every time a key is pressed
    elif event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        selection_indicator.update(keys)
        
    #ANY CLICK
    elif event.type == pygame.MOUSEBUTTONDOWN:
        os.system('cls' if os.name == 'nt' else 'clear')
        selected_tile_pos = grid.get_tile_pos(event.pos)

        #Check if the position clicked is in grid space
        if tilemap.validate_pos(selected_tile_pos):
            tile = tilemap.tiles[selected_tile_pos[1]][selected_tile_pos[0]]
        else:
            return True
        
        #LEFT CLICK
        if event.button == 1:  # Check for left mouse button
            if selection_indicator.get_pos() == selected_tile_pos:
                tile.rotate_tile()
            else:
                selection_indicator.set_pos(selected_tile_pos)
        
        #RIGHT CLICK
        elif event.button == 3:  # Check for right mouse button
            selection_indicator.set_pos(selected_tile_pos)
            tile.rotate_tile()
        
        # #Pathing Logic
        tilemap.clear_power()
        tilemap.trace_power(tilemap.battery.position)
        
    return True   

if __name__ == "__main__":
    main()
