from pygame import *
from random import choice
from entity import *
from a_star_and_rdfs import randomized_dfs_maze
from tiles import build_walls

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
wall,dirt = set(),set()

#you can actually place the right kind of wall (top, right, left and bottom) from the beginning and worry about the corners later
for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == 1:
            wall.update({(i*maze_cell_width+k*(maze_cell_width-1),j*maze_cell_width+l*(maze_cell_width-1)) for k in range(2) for l in range(2)})
            if maze[i][max(0,j-1)] == 0:
                wall.update({(i*maze_cell_width+k,j*maze_cell_width) for k in range(maze_cell_width)})
            if maze[min(maze_l-1,i+1)][j] == 0:
                wall.update({((i+1)*maze_cell_width-1,j*maze_cell_width+k) for k in range(maze_cell_width)})
            if maze[i][min(maze_l-1,j+1)] == 0:
                wall.update({(i*maze_cell_width+k,(j+1)*maze_cell_width-1) for k in range(maze_cell_width)})
            if maze[max(0,i-1)][j] == 0:
                wall.update({(i*maze_cell_width,j*maze_cell_width+k) for k in range(maze_cell_width)})
        else:
            floor_and_walls[i*maze_cell_width,(i+1)*maze_cell_width][j*maze_cell_width,(j+1)*maze_cell_width] = choice()
#            dirt.update({(i*maze_cell_width+l,j*maze_cell_width+k) for k in range(maze_cell_width) for l in range(maze_cell_width)})

walls = build_walls()

def write(text : str, color : tuple, position : tuple, size : int, font_name : str = 'Helvetica') -> None:
    if not (size,font_name) in font_dict:
        font_dict[size,font_name] = font.SysFont(font_name, size)
    screen.blit(font_dict[size,font_name].render(text,False,color),position)

def update_window() -> None:
    screen.fill((100,100,100))
    dl = HEIGHT/10
    for i in range(round(WIDTH/dl)+2):
        for j in range(round(HEIGHT/dl)+2):
            if (i+j)%2 == 0 and dl*i-player_1.x%(2*dl) >= 0 and dl*j-player_1.y%(2*dl) >= 0:
                screen.fill(WHITE,rect=(dl*i-player_1.x%(2*dl),dl*j-player_1.y%(2*dl),dl,dl))
    player_1.show(screen)
    for e in enemies:
        e.show(screen,player_1)
    write(f'{round(player_1.x)},{round(player_1.y)}',BLACK,(0,0),30)

def show_maze():
    screen.fill(WHITE)
    for e in wall:
        x,y = e[0]*16-player_1.x, e[1]*16-player_1.y
        if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
            screen.fill(BLACK,rect=(x,y,16,16))
    for e in dirt:
        x,y = e[0]*16-player_1.x, e[1]*16-player_1.y
        if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
            screen.fill((0,255,0),rect=(x,y,16,16))
    for i in range():
        for j in range():
            pass
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

