#import pygame
import sys
from utils import *

# Constants
WIDTH  = TILE_SIZE*GRID_WIDTH 
HEIGHT = TILE_SIZE*GRID_HEIGHT
FPS = 30

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tilemap System in Pygame")
    clock = pygame.time.Clock()

    player = Player((0, 0))
    
    
    tilemap = Tilemap()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                player.update(keys)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_tile_pos = get_tile_pos(event.pos)
                player.set_pos(selected_tile_pos)
                print(selected_tile_pos)

        screen.fill(WHITE)
        tilemap.draw(screen)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
