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
screen.fill(WHITE)
display.flip()
font.init()
font_dict = {}
maze_l = 51
maze = randomized_dfs_maze((1,1),maze_l,maze_l)
maze_cell_width = 6
floor_and_walls = [[87]*maze_l*maze_cell_width for i in range(maze_l*maze_cell_width)]
print(len(floor_and_walls),len(floor_and_walls[0]))
wall,dirt = set(),set()

#you can actually place the right kind of wall (top, right, left and bottom) from the beginning and worry about the corners later
for i in range(maze_l):
    for j in range(maze_l):
        if maze[i][j] == 1:
            floor_and_walls[i*maze_cell_width][j*maze_cell_width] = choice([w1110,w1010,w1100,w1000][(maze[i][max(0,j-1)] == 1) + 2*(maze[max(0,i-1)][j] == 1)])
            floor_and_walls[i*maze_cell_width][(j+1)*maze_cell_width-1] = choice([w1101,w0101,w1100,w0100][(maze[i][min(maze_l-1,j+1)] == 1) + 2*(maze[min(maze_l-1,i+1)][j] == 1)])
            floor_and_walls[(i+1)*maze_cell_width-1][j*maze_cell_width] = choice(w1111)
            floor_and_walls[(i+1)*maze_cell_width-1][(j+1)*maze_cell_width-1] = choice(w1111)

            if maze[i][max(0,j-1)] == 0:
                for k in range(1, maze_cell_width-1):
                    floor_and_walls[i*maze_cell_width + k][j*maze_cell_width] = choice(w1100)

            if maze[min(maze_l-1,i+1)][j] == 0:
                for k in range(1, maze_cell_width-1):
                    floor_and_walls[(i+1)*maze_cell_width-1][j*maze_cell_width + k] = choice(w0101)

            if maze[i][min(maze_l-1,j+1)] == 0:
                for k in range(1, maze_cell_width-1):
                    floor_and_walls[i*maze_cell_width + k][(j+1)*maze_cell_width-1] = choice(w1111)

            if maze[max(0,i-1)][j] == 0:
                for k in range(1, maze_cell_width-1):
                    floor_and_walls[i*maze_cell_width][j*maze_cell_width + k] = choice(w1010)
        else:
            for x in range(i*maze_cell_width, (i+1)*maze_cell_width):
                for y in range(j*maze_cell_width, (j+1)*maze_cell_width):
                    floor_and_walls[x][y] = choice(list(dirt_tiles))

#walls = build_walls()

def write(text : str, color : tuple, position : tuple, size : int, font_name : str = 'Helvetica') -> None:
    if not (size,font_name) in font_dict:
        font_dict[size,font_name] = font.SysFont(font_name, size)
    screen.blit(font_dict[size,font_name].render(text,False,color),position)

def show_maze():
    screen.fill(WHITE)
#    for e in wall:
#        x,y = e[0]*16-player_1.x, e[1]*16-player_1.y
#        if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
#            screen.fill(BLACK,rect=(x,y,16,16))
#    for e in dirt:
#        x,y = e[0]*16-player_1.x, e[1]*16-player_1.y
#        if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
#            screen.fill((0,255,0),rect=(x,y,16,16))
    for i in range(max(round(-player_1.x//16),0),min(len(floor_and_walls),WIDTH-(player_1.x//16))):
        for j in range(max(round(-player_1.y//16),0),min(len(floor_and_walls[0]),HEIGHT-(player_1.y//16))):
            screen.blit(tiles[floor_and_walls[i][j]],(i*16-player_1.x,j*16-player_1.y))
    player_1.show(screen)
    for e in enemies:
        e.show(screen,player_1)

monsters_sprites = ["priest1","priest2","priest3","priest4","priest5","priest6","skeleton1","skeleton2","skeleton3","skeleton4","skull1","skull2","vampire1","vampire2"]
player_1 = player(0,0,0,0)
enemies = [enemy(100*i,0,monsters_sprites[i]) for i in range(len(monsters_sprites))]

while True:
    for ev in event.get():
        if ev.type == QUIT:
            quit()
    player_1.move()
    show_maze()
    display.flip()
