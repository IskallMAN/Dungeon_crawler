from pygame import *
from random import choice
from tiles import build_walls, fill_dirt

WIDTH,HEIGHT = 1280,720
BLACK = (0,0,0)
WHITE = (255,255,255)

screen = display.set_mode((WIDTH,HEIGHT), FULLSCREEN)
display.set_caption('Simulation')
screen.fill(WHITE)
display.flip()
font.init()
font_dict = {}

def write(text : str, color : tuple, position : tuple, size : int, font_name : str = 'Helvetica') -> None:
    if not (size,font_name) in font_dict:
        font_dict[size,font_name] = font.SysFont(font_name, size)
    screen.blit(font_dict[size,font_name].render(text,False,color),position)

tile_preview_size = 16
tileset = image.load("2D Pixel Dungeon Asset Pack\character and tileset\Dungeon_Tileset.png")
tiles = [transform.scale(tileset.subsurface(16*i,16*j,16,16),(tile_preview_size,tile_preview_size)) for i in range(10) for j in range(10)]
tiles.append(image.load("placeholder.png"))
floor_tiles = [60,61,62,70,71,72,80,81,82,90,91,92,7,17,27,37]
floor = [[87 for i in range(100)] for j in range(100)]
walls = [[None for i in range(100)] for j in range(100)]
room = [[None for i in range(100)] for j in range(100)]
k = 0
zoom = 16
selected_tile = k
x_displacement, y_displacement = 0,0
panel_1, panel_2 = False, False
wall_temporary = {(21, 16), (34, 19), (36, 16), (36, 25), (23, 25), (27, 34), (38, 16), (42, 32), (25, 25), (34, 21), (31, 31), (28, 23), (23, 36), (32, 23), (42, 25), (27, 36), (26, 16), (42, 34), (33, 31), (26, 25), (25, 36), (34, 23), (40, 36), (21, 32), (23, 29), (42, 18), (42, 36), (25, 29), (34, 16), (40, 29), (21, 25), (21, 34), (27, 22), (42, 20), (27, 31), (42, 29), (38, 25), (22, 16), (34, 18), (21, 18), (29, 31), (22, 25), (21, 36), (36, 27), (42, 22), (36, 36), (24, 16), (35, 16), (27, 33), (42, 31), (24, 25), (39, 16), (39, 25), (21, 20), (38, 36), (37, 16), (21, 29), (27, 17), (41, 16), (34, 32), (36, 29), (41, 25), (42, 24), (27, 35), (42, 33), (30, 31), (38, 29), (26, 27), (31, 23), (21, 22), (26, 36), (21, 31), (27, 19), (42, 17), (34, 34), (33, 23), (42, 35), (26, 29), (21, 24), (21, 33), (27, 21), (42, 19), (34, 36), (21, 17), (34, 20), (21, 35), (36, 26), (27, 23), (37, 25), (42, 21), (22, 36), (27, 32), (28, 31), (42, 30), (32, 31), (29, 23), (35, 36), (23, 16), (24, 36), (21, 19), (34, 22), (39, 36), (27, 16), (34, 31), (36, 28), (22, 29), (42, 23), (37, 36), (25, 16), (41, 36), (40, 16), (24, 29), (26, 26), (40, 25), (21, 21), (21, 30), (39, 29), (27, 18), (42, 16), (34, 33), (37, 29), (30, 23), (41, 29), (26, 28), (21, 23), (34, 17), (27, 20), (34, 35)}
placing_marker = False
dirt = set()

def handle_inputs(x_displacement,y_displacement) -> tuple:
    keys = key.get_pressed()
    panel_1, panel_2 = False, False
    if keys[K_z]:
        y_displacement += 1
    if keys[K_s]:
        y_displacement -= 1
    if keys[K_d]:
        x_displacement -= 1
    if keys[K_q]:
        x_displacement += 1
    if keys[K_SPACE]:
        panel_1 = True
    if keys[K_w]:
        panel_2 = True
    return((x_displacement,y_displacement,panel_1,panel_2))

def show_canvas() -> None:
    for i in range(100):
        for j in range(100):
            screen.blit(transform.scale(tiles[floor[i][j]],(zoom,zoom)),(i*zoom+x_displacement,j*zoom+y_displacement))
            if room[i][j] != None:
                screen.blit(transform.scale(tiles[room[i][j]],(zoom,zoom)),(i*zoom+x_displacement,j*zoom+y_displacement))
            if walls[i][j] != None:
                screen.blit(transform.scale(tiles[walls[i][j]],(zoom,zoom)),(i*zoom+x_displacement,j*zoom+y_displacement))
    for e in wall_temporary:
        screen.fill((255,0,0),rect=(e[0]*zoom+x_displacement,e[1]*zoom+y_displacement,zoom,zoom))
    for e in dirt:
        screen.fill((0,255,0),rect=(e[0]*zoom+x_displacement,e[1]*zoom+y_displacement,zoom,zoom))
    for i in range(4):
        screen.blit(transform.scale(tiles[100],(32,32)),(WIDTH - (i+1)*32,0))

while True:
    screen.fill(WHITE)
    m_pos = mouse.get_pos()
    for ev in event.get():
        if ev.type == QUIT:
            quit()
        if ev.type == MOUSEWHEEL:
            zoom += ev.y
        m_state = mouse.get_pressed()
        if m_state[0] == 1:#event.button :  1 - left click , 2 - middle click , 3 - right click , 4 - scroll up , 5 - scroll down
            tile = (round((m_pos[0]-x_displacement-zoom/2)/zoom),round((m_pos[1]-y_displacement-zoom/2)/zoom))
            if m_pos[0] > WIDTH-4*32 and m_pos[1] < 32:
                if m_pos[0] > WIDTH-32:
                    if len(dirt) == 0:
                        placing_marker = True
            elif placing_marker:
                dirt.add(tile)
                placing_marker = False
                dirt = fill_dirt(dirt,wall_temporary)
                for e in dirt:
                    floor[e[0]][e[1]] = choice(floor_tiles)
                walls = build_walls(wall_temporary,dirt,walls)
                dirt = set()
                wall_temporary = set()
            elif m_pos[0] < 160 and m_pos[1] < 160 and panel_1:
                selected_tile = k
            elif panel_2:
                wall_temporary.add(tile)
            else:
                room[tile[0]][tile[1]] = selected_tile
        if m_state[2] == 1:
            tile = (round((m_pos[0]-x_displacement-zoom/2)/zoom),round((m_pos[1]-y_displacement-zoom/2)/zoom))
            if panel_2:
                if tile in wall_temporary:
                    wall_temporary.remove(tile)
            elif not panel_1:
                room[tile[0]][tile[1]] = 87
    (x_displacement,y_displacement,panel_1,panel_2) = handle_inputs(x_displacement,y_displacement)
    show_canvas()
    if m_pos[0] < 160 and m_pos[1] < 160:
        k = round((m_pos[0]-8)/16)*10+round((m_pos[1]-8)/16)
        screen.blit(transform.scale(tiles[k],(128,128)),(WIDTH-128,0))
    if panel_1:
        screen.fill(WHITE,rect=(0,0,160,160))
        screen.blit(tileset,(0,0))
    write(str(k),(255,0,0),(0,160),50)
    display.flip()