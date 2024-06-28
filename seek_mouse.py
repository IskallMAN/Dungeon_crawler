from pygame import *
from a_star_and_rdfs import randomized_dfs_maze
from entity import *

WIDTH,HEIGHT = 650,650
BLACK = (0,0,0)
WHITE = (255,255,255)

screen = display.set_mode((WIDTH,HEIGHT))
display.set_caption('Simulation')
screen.fill(WHITE)
display.flip()
font.init()
font_dict = {}

def write(text : str, color : tuple, position : tuple, size : int, font_name : str = 'Helvetica') -> None:
    if not (size,font_name) in font_dict:
        font_dict[size,font_name] = font.SysFont(font_name, size)
    screen.blit(font_dict[size,font_name].render(text,False,color),position)

w,h = 301,301
maze = randomized_dfs_maze((1,1),w,h)
if w/h > WIDTH/HEIGHT:
    dx = round(WIDTH/w)
else:
    dx = round(HEIGHT/h)

def draw_maze(maze):
    screen.fill(WHITE)
    for i in range(w):
        for j in range(h):
            if maze[i][j] == 1:
                screen.fill((100,100,100),rect=(i*dx,j*dx,dx,dx))
            else:
                screen.fill((255,255,255),rect=(i*dx,j*dx,dx,dx))
    screen.fill((255,0,0),rect=(x_p*dx,y_p*dx,dx,dx))
    screen.fill((0,0,255),rect=(enemy_1.x*dx,enemy_1.y*dx,dx,dx))


m_player = player(w-2,h-2,0,0)
enemy_1 = enemy(1,1,"vampire1")

while True:
#    print(e for e in key.get_pressed() if e != False)
    print(type(key.get_pressed()))
    for ev in event.get():
        if ev.type == QUIT:
            quit()
        m_pos = mouse.get_pos()
        x_p,y_p = round(-0.5+m_pos[0]/dx), round(-0.5+m_pos[1]/dx)
        if x_p < w and y_p < h and maze[x_p][y_p] == 0:
            m_player.x,m_player.y = x_p,y_p
            path = a_star(maze,(1,1),(m_player.x,m_player.y))
    enemy_1.seek(m_player,maze)
    draw_maze(maze)
    display.flip()
