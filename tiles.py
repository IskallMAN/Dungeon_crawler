from pygame import *
from random import choice

screen = display.set_mode((1280,720), FULLSCREEN)
font.init()

#width = 50
tileset = image.load("2D Pixel Dungeon Asset Pack\character and tileset\Dungeon_Tileset.png")
tiles = [tileset.subsurface(16*i,16*j,16,16) for i in range(10) for j in range(10)]

dirt_tiles = {60,61,62,70,72,80,81,82,90,91,92,7,17,27,37,22}
wall_dirt_tile = {}

w1111 = [10,20,30,40]
w1010 = [50,51,52,53]
w0101 = [0,1,2,3]
w1100 = [14,24,34,44,15,25]
w1110 = [5,45]
w1101 = [35,55]
w0100 = [4]
w1000 = [54]

def build_walls(walls,dirt,wall) -> set:
    for e in walls:
        if ((e[0]+1,e[1]) in walls) + ((e[0],e[1]+1) in walls) + ((e[0]-1,e[1]) in walls) + ((e[0],e[1]-1) in walls) == 2:
#two walls :
            if (e[0]+1,e[1]) in walls and (e[0],e[1]+1) in walls:
                if (e[0]+1,e[1]+1) in dirt:
                    wall[e[0]][e[1]] = choice(w0101)
                else:
                    wall[e[0]][e[1]] = choice(w1110)
            if (e[0]-1,e[1]) in walls and (e[0],e[1]+1) in walls:
                if (e[0]-1,e[1]+1) in dirt:
                    wall[e[0]][e[1]] = choice(w1010)
                else:
                    wall[e[0]][e[1]] = choice(w1101)
            if (e[0],e[1]+1) in walls and (e[0],e[1]-1) in walls:
                if (e[0]+1,e[1]) in dirt:
                    wall[e[0]][e[1]] = choice(w0101)
                else:
                    wall[e[0]][e[1]] = choice(w1010)
            if (e[0]-1,e[1]) in walls and (e[0]+1,e[1]) in walls:
                if (e[0],e[1]+1) in dirt:
                    wall[e[0]][e[1]] = choice(w1111)
                else:
                    wall[e[0]][e[1]] = choice(w1100)
            if (e[0]+1,e[1]) in walls and (e[0],e[1]-1) in walls:
                if (e[0]+1,e[1]-1) in dirt:
                    wall[e[0]][e[1]] = choice(w0100)
                else:
                    wall[e[0]][e[1]] = choice(w1111)
            if (e[0]-1,e[1]) in walls and (e[0],e[1]-1) in walls:
                if (e[0]-1,e[1]-1) in dirt:
                    wall[e[0]][e[1]] = choice(w1000)
                else:
                    wall[e[0]][e[1]] = choice(w1111)
        else:
            wall[e[0]][e[1]] = choice(w1111)
    return wall

def fill_dirt(dirt : set,wall : set, max_size = 1000) -> set:
    prev_len = 0
    while len(dirt) > prev_len and len(dirt) <= max_size:
        prev_len = len(dirt)
        for e in dirt.copy():
            for neighboor in [(0,1),(1,0),(0,-1),(-1,0)]:
                if (e[0]+neighboor[0],e[1]+neighboor[1]) not in wall:
                    dirt.add((e[0]+neighboor[0],e[1]+neighboor[1]))
    print(len(dirt))
    return dirt

if __name__ == "__main__":
    width = 16
    k = 0
    while True:
        screen.fill((0,0,0))
        for ev in event.get():
            if ev.type == QUIT:
                quit()
        m_pos = mouse.get_pos()
        for i in range(len(tiles)):
            screen.blit(tiles[i],(width*(i//10),(i%10)*width))
        s = 0
        for e in dirt_tiles:
            screen.blit(tiles[e],((width+5)*s,10*width + 30))
            s += 1
        for i in range(9):
            screen.fill(3*(255),rect=(width*i,0,1,10*width))
        for i in range(9):
            screen.fill(3*(255),rect=(0,width*i,10*width,1))
        if m_pos[0] < width*10 and m_pos[1] < width*10:
            k = round((m_pos[0]-width/2)/width)*10+round((m_pos[1]-width/2)/width)
        screen.blit(font.SysFont('Helvetica', 30).render(str(k),False,(255,0,0)),(0,10*width))
        display.flip()
