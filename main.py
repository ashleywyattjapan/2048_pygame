import pygame
import random 
import math

pygame.init()

#constants 
FPS = 60
WIDTH, HEIGHT = 800, 800 
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS 
RECT_WIDTH = WIDTH // COLS 

OUTLINE_COLOR = (187, 173, 160) #gray color 
OUTLINE_THICKNESS = 10 
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20
#Pygame window setup
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

class Tile: 
    #more colors to support higher tile values 
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]
    def __init__(self, value, row, col):
        self.value = value 
        self.row = row
        self.col = col 
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT 

    def get_color(self):
        #Calculates the color of the tile based on its value. 
        color_index = int(math.log2(self.value)) - 1
        #to prevent indexerror for high numbers use last color 
        color = self.COLORS[color_index]
        return color
        #if color_index >= len(self.COLORS):
           # return self.COLORS[-1]
        
        #return self.COLORS[color_index]

    def draw(self, window): 
        #Draws the tile on the game window
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))
        # render the text (the tiles value)
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        #center the text w/in the tile 
        window.blit(
            text,
             (
                self.x + (RECT_WIDTH /2 - text.get_width() / 2), 
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
              ), 
            )


    def set_pos(self, ceil = False): #current row col position 
        if ceil: 
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x /RECT_WIDTH)
        else: 
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x /RECT_WIDTH)
        

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

def draw_grid(window): 
    for row in range(1, ROWS): 
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS): 
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values(): 
        tile.draw(window)

    draw_grid(window)

    pygame.display.update() #fills screen w bg color 
    
def get_random_pos(tiles): 
    row = None 
    col = None 
    while True: 
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        #checks if this key exists in the dictionary 
        if f"{row}{row}" not in tiles: 
            break 
    return row, col 

def move_tiles(window, tiles, clock, direction):
    updated = True 
    blocks = set()

    if direction == "left": 
        sort_func = lambda x: x.col 
        reverse = False #ascending or descending order
        delta =(-MOVE_VEL, 0) #how much to move each tile frame
        boundary_check = lambda tile: tile.col == 0 #have we hit the boundary of screen 
        #func to get us the next tile 
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col -1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL #whether we should merge tile based on current movement
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL #when we move & tile is to left of us but not same value 
        ceil = True #should we round up or down 



    elif direction == "right": 
        pass 
    elif direction == "up": 
        pass 
    elif direction == "down": 
        pass

    while updated: 
        #update screen to look like moving 
        clock.tick(FPS)
        updated = False 
        sorted_tiles = sorted(tiles.values(), key = sort_func, reverse = reverse)
        for i, tile in enumerate(sorted_tiles): 
            if boundary_check(tile): 
                continue 

            next_tile = get_next_tile(tile)
            if not next_tile: 
                tile.move(delta)
            #is this tile the same value 
            elif (tile.value == next_tile.value and tile not in blocks and next_tile not in blocks): 
                if merge_check(tile, next_tile): 
                    tile.move(delta)
                else: 
                    next_tile.value *= 2 
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile): 
                tile.move(delta)
            else: 
                continue

            tile.set_pos(ceil)
            updated = True 
        update_tiles(window, tiles, sorted_tiles)
        return end_move(tiles)

#check whether game is over & last cleanup operation
def end_move(tiles): 
    if len(tiles) == 16: 
        return "lost"
    
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

def update_tiles(window, tiles, sorted_tiles): 
    tiles.clear()
    for tile in sorted_tiles: 
        tiles[f"{tile.row}{tile.col}"] = tile 
    draw(window, tiles)

def generate_tiles(): 
    #empty dictionary to store our tiles. 
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)
    
    return tiles
#Main Game Loop
def main(window): 
    clock = pygame.time.Clock()
    run = True
    #dictionary to store the tile objects 
    #key is a string like row_col for easy access.
    tiles = generate_tiles()

    while run: 
        clock.tick(FPS) 

        for event in pygame.event.get(): #loop through all events that occured 
            if event.type == pygame.QUIT: 
                run = False 
                break
        
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT: 
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP: 
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN: 
                    move_tiles(window, tiles, clock, "down")
            

        draw(window, tiles)

    pygame.quit()



if __name__ == "__main__":
    main(WINDOW)