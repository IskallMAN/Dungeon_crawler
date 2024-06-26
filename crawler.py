from pygame import *
from random import choice
from entity import *
from a_star_and_rdfs import randomized_dfs_maze
from tiles import *

WIDTH,HEIGHT = 1280,720
BLACK = (0,0,0)
WHITE = (255,255,255)

screen = display.set_mode((WIDTH,HEIGHT), FULLSCREEN)
display.set_caption('Simulation')
font.init()
clock = time.Clock()
font_dict = {}

maze_l = 51
maze = randomized_dfs_maze((1,1),maze_l,maze_l)
maze_cell_width = 6
floor_and_walls = [[87]*maze_l*maze_cell_width for i in range(maze_l*maze_cell_width)]
wall,dirt = set(),set()


for i in range(maze_l):
    for j in range(maze_l):
        if maze[i][j] == 1:
            floor_and_walls[i*maze_cell_width][j*maze_cell_width] = choice([w1110,w1010,w1100,w1000][(maze[i][max(0,j-1)] == 1) + 2*(maze[max(0,i-1)][j] == 1)])
            floor_and_walls[i*maze_cell_width][(j+1)*maze_cell_width-1] = choice([w1111,w1010][(maze[i][min(maze_l-1,j+1)] == 1)])
            floor_and_walls[(i+1)*maze_cell_width-1][j*maze_cell_width] = choice([w1101,w0101,w1100,w0100][(maze[i][max(0,j-1)] == 1) + 2*(maze[min(maze_l-1,i+1)][j] == 1)])
            floor_and_walls[(i+1)*maze_cell_width-1][(j+1)*maze_cell_width-1] = choice([w1111,w0101][(maze[i][min(maze_l-1,j+1)] == 1)])

            if maze[i][max(0,j-1)] == 0:
                for k in range(1,maze_cell_width-1):
                    floor_and_walls[i*maze_cell_width + k][j*maze_cell_width] = choice(w1100)

            if maze[min(maze_l-1,i+1)][j] == 0:
                for k in range(1,maze_cell_width-1):
                    floor_and_walls[(i+1)*maze_cell_width-1][j*maze_cell_width + k] = choice(w0101)

            if maze[i][min(maze_l-1,j+1)] == 0:
                for k in range(1,maze_cell_width-1):
                    floor_and_walls[i*maze_cell_width + k][(j+1)*maze_cell_width-1] = choice(w1111)

            if maze[max(0,i-1)][j] == 0:
                for k in range(1,maze_cell_width-1):
                    floor_and_walls[i*maze_cell_width][j*maze_cell_width + k] = choice(w1010)
        else:
            for x in range(i*maze_cell_width, (i+1)*maze_cell_width):
                for y in range(j*maze_cell_width, (j+1)*maze_cell_width):
                    floor_and_walls[x][y] = choice(list(dirt_tiles))
for i in range(maze_cell_width*maze_l):
    floor_and_walls[i][0] = 87
    floor_and_walls[0][i] = 87
    floor_and_walls[len(floor_and_walls)-1][0] = 87
    floor_and_walls[0][len(floor_and_walls)-1] = 87

def write(text : str, color : tuple, position : tuple, size : int, font_name : str = 'Helvetica') -> None:
    if not (size,font_name) in font_dict:
        font_dict[size,font_name] = font.SysFont(font_name, size)
    screen.blit(font_dict[size,font_name].render(text,False,color),position)

def show_maze():
    screen.fill(WHITE)
    for i in range(max(round((player_1.x-WIDTH/2)//tile_display_width),0),min(len(floor_and_walls),1+round(WIDTH/2+player_1.x)//tile_display_width)):
        for j in range(max(round((player_1.y-HEIGHT/2)//tile_display_width),0),min(len(floor_and_walls[0]),1+round(HEIGHT/2+player_1.y)//tile_display_width)):
            screen.blit(tiles[floor_and_walls[i][j]],(WIDTH/2+i*tile_display_width-player_1.x,HEIGHT/2+j*tile_display_width-player_1.y))
    player_1.show(screen)
    for e in enemies:
        e.show(screen,player_1)

monsters_sprites = ["priest1","priest2","priest3","priest4","priest5","priest6","skeleton1","skeleton2","skeleton3","skeleton4","skull1","skull2","vampire1","vampire2"]
player_1 = player((maze_cell_width+1)*tile_display_width,(maze_cell_width+1)*tile_display_width,0,0)
enemies = [enemy(100*i,0,monsters_sprites[i]) for i in range(len(monsters_sprites))]

while True:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
    player_1.get_speed()
    player_1.move(tile_display_width*maze_cell_width,maze)
    show_maze()
    clock.tick(30)
    display.flip()
