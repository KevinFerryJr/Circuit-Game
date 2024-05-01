import pygame
import math
import maps
import random
import time

map_data = maps.map_table["hard"]["1"]

TILE_SIZE = 100
GRID_WIDTH = len(map_data[0])
GRID_HEIGHT = len(map_data)

map_key = {
    1: "battery",
    2: "wire_line",
    3: "wire_corner",
    4: "wire_inter",
    5: "led"
}

tile_sprites = {
    "battery": {"on":pygame.image.load('./assets/tiles/battery/bat_1.png')},
    "wire_line": {"off":pygame.image.load('./assets/tiles/wires/wire_1_off.png'), "on":pygame.image.load('./assets/tiles/wires/wire_1_on.png')},
    "wire_corner": {"off":pygame.image.load('./assets/tiles/wires/wire_2_off.png'), "on":pygame.image.load('./assets/tiles/wires/wire_2_on.png')},
    "wire_inter": {"off":pygame.image.load('./assets/tiles/wires/wire_3_off.png'), "on":pygame.image.load('./assets/tiles/wires/wire_3_on.png')},
    "led": {"off":pygame.image.load('./assets/tiles/leds/led_1_empty.png'), "on":pygame.image.load('./assets/tiles/leds/led_1_full.png')},
}

class Tilemap:
    def __init__(self, map_data):
        self.tiles = []
        self.battery = None
        self.map_data = map_data
        self.width = len(self.map_data[0])
        self.height = len(self.map_data)
        self.tile_sprites = pygame.sprite.Group()
        self.scale_tile_sprites()
        self.populate()
        self.clear_power()
        self.trace_power(self.battery.position)

    def populate(self):
        for row in range(self.height):
            tile_row = []
            for col in range(self.width):
                location_value = map_data[row][col]
                if location_value in map_key:
                    tile_type = map_key[location_value]
                    #Instantiate a tile and add to tile array
                    tile = Tile(self, tile_type, row, col)
                    tile.rotate_tile(rotation=random.randint(0,3))
                    tile_row.append(tile)
                    
                    #Add to the sprite group
                    self.tile_sprites.add(tile.sprite)
            self.tiles.append(tile_row)
            
    def draw(self, surface):
        self.tile_sprites.draw(surface)
        
    def validate_pos(self, pos):
        if pos[0] < GRID_WIDTH and pos[0] >= 0:
            if pos[1] < GRID_HEIGHT and pos[1] >= 0:
                return True
        else:
            return False

    def scale_tile_sprites(self, sprites=tile_sprites):
        for key, value in sprites.items():
            # Check if the value is a dictionary (nested dictionary)
            for sub_key, sub_value in value.items():
                scaled_image = pygame.transform.scale(sub_value, (TILE_SIZE, TILE_SIZE))
                sprites[key][sub_key] = scaled_image
            
    def trace_power(self, next_pos):
        cur_pos = next_pos
        cur_tile = self.tiles[cur_pos[1]][cur_pos[0]]
        
        # Loop through our current tiles ports
        for port in cur_tile.ports:
            port_dir = cur_tile.get_port_dir(port)
            next_pos = (cur_pos[0] + port_dir[0], cur_pos[1] + port_dir[1])
            
            #Check if poistion is in map array
            if self.validate_pos(next_pos):
                next_tile = self.tiles[next_pos[1]][next_pos[0]]
            else:
                print("Index out of map array range!")
                continue
            
            #If tile has already been connected
            if next_tile.power:
                print("that tile is already on!")
                continue
            
            print(next_pos)
            # Loop through next tiles ports
            for sub_port in next_tile.ports:
                sub_port_dir = next_tile.get_port_dir(sub_port)
                sub_next_pos = (next_pos[0] + sub_port_dir[0], next_pos[1] + sub_port_dir[1])
                
                #Check if poistion is in map array
                if self.validate_pos(sub_next_pos):
                    sub_next_tile = self.tiles[sub_next_pos[1]][sub_next_pos[0]]
                else:
                    print("Index out of map array range!")
                    continue
                
                #If the sub tile has a connection to the current tile
                if sub_next_pos == cur_pos:
                    next_tile.set_image(tile_sprites[next_tile.type]["on"])
                    next_tile.power = True
                    #Recurse and keep looking for more connections
                    self.trace_power(next_pos)

    def clear_power(self):
        for row in self.tiles:
            for tile in row:
                if tile.type != "battery":
                    tile.set_image(tile_sprites[tile.type]["off"])
                    tile.power = False
    
class Tile:
    def __init__(self, Parent, tile_type, row, col):
        self.type = tile_type
        self.sprite = pygame.sprite.Sprite()
        self.ports = [0]
        self.rotation = 0
        self.position = (col, row)
        self.power = False
        self.sprite.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = col * TILE_SIZE
        self.sprite.rect.y = row * TILE_SIZE
        self.initialize(Parent)
        
    def initialize(self, parent):
        #Set initial tile sprites
        if self.type == "battery":
            self.power = True
            self.sprite.image = tile_sprites[self.type]["on"]
            parent.battery = self
        else:
            self.sprite.image = tile_sprites[self.type]["off"]
        
        # Configure wire ports by type  
        if self.type == "wire_line":
            self.ports = [1,3]
        elif self.type == "wire_corner":
            self.ports = [0,1]
        elif self.type == "wire_inter": # Tile is a wire intersection
            self.ports = [0,1,3]
            print(self.ports)
            
    def set_image(self, image):
        rot_angle = self.rotation * -90
        rotated_image = pygame.transform.rotate(image, rot_angle)
        self.sprite.image = rotated_image
    
    def rotate_tile(self, rotation = 1):
        self.sprite.image = pygame.transform.rotate(self.sprite.image, rotation * -90)
        self.rotation = (self.rotation + rotation) % 4
 
    def get_port_dir(self, port):
        angle = ((port + self.rotation) % 4) * (math.pi/2)
        x = round(-math.sin(angle))
        y = round(math.cos(angle))
        dir = (x,y)
        return dir
    
class Selection_Indicator(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        original_image = pygame.image.load('./assets/tiles/select/selection.png')
        scaled_image = pygame.transform.scale(original_image, (TILE_SIZE, TILE_SIZE))
        self.image = scaled_image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] * TILE_SIZE
        self.rect.y = pos[1] * TILE_SIZE

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= TILE_SIZE
        if keys[pygame.K_RIGHT]:
            self.rect.x += TILE_SIZE
        if keys[pygame.K_UP]:
            self.rect.y -= TILE_SIZE
        if keys[pygame.K_DOWN]:
            self.rect.y += TILE_SIZE
        
    def get_pos(self):
        x = self.rect.x / TILE_SIZE
        y = self.rect.y / TILE_SIZE
        return (x,y)
            
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