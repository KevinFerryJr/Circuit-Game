import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TILE_SIZE = 64
GRID_WIDTH = 20
GRID_HEIGHT = 12

# Tilemap class
class Tilemap:
    def __init__(self):
        self.map_data = self.load_data()
        self.width = len(self.map_data[0])
        self.height = len(self.map_data)
        self.tiles = pygame.sprite.Group()

        for row in range(self.height):
            for col in range(self.width):
                if self.map_data[row][col] == 1:
                    tile = pygame.sprite.Sprite()
                    tile.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    tile.image.fill(BLACK)
                    tile.rect = tile.image.get_rect()
                    tile.rect.x = col * TILE_SIZE
                    tile.rect.y = row * TILE_SIZE
                    self.tiles.add(tile)
                    
    def draw(self, surface):
        self.tiles.draw(surface)
        
    def load_data(self):
        map_data = []
        #Load map as all zeros
        for y in range(GRID_HEIGHT):
            horiz_line = []
            for x in range(GRID_WIDTH):
                horiz_line.append(0)
            map_data.append(horiz_line)
        return map_data 
    
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * TILE_SIZE
        self.rect.y = pos[1] * TILE_SIZE
        self.speed = TILE_SIZE

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
    def set_pos(self, pos, pos_type = 'grid'):
        if pos_type == 'grid':
            self.rect.x = pos[0] * TILE_SIZE
            self.rect.y = pos[1] * TILE_SIZE
        
        elif pos_type == 'absolute':
            self.rect.x = pos[0]
            self.rect.y = pos[1]
    
# Return the tile coords at a given location
def get_tile_pos(pos):
    new_x = pos[0] // TILE_SIZE
    new_y = pos[1] // TILE_SIZE
    return (new_x,new_y)