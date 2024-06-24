from a_star_and_rdfs import a_star
from pygame import *

class enemy:
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.type = type
        self.lr = 0
        self.frame_list = [[transform.scale(image.load(f"sprites\{type}\{type}_{i}.png"),(64,64)) for i in range(1,5)]]
        self.frame_list.append([transform.flip(e,1,0) for e in self.frame_list[0]])
        self.frame_count = 0
        self.frame = 0

    def seek(self,player,maze):
        path = a_star(maze,(self.x,self.y),(player.x,player.y))
        if path != None:
            (self.x,self.y) = path[min(len(path)-1,1)]
    
    def show(self,screen,player):
        screen.blit(self.frame_list[self.lr][self.frame],(self.x-player.x,self.y-player.y))
        if self.frame_count == 30:
            self.frame = (self.frame + 1)%4
            self.frame_count = 0
        self.frame_count += 1

class player:
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dash_cooldown = 0
        self.facing_x = 0
        self.facing_y = 0
        self.frame_list = [[transform.scale(image.load(f"sprites\\vampire1\\vampire1_{i}.png"),(64,64)) for i in range(1,5)]]
        self.frame_list.append([transform.flip(e,1,0) for e in self.frame_list[0]])
        self.frame = 0
        self.lr = 0
        self.frame_count = 0
        self.is_moving = False

    def move(self):
        if self.dash_cooldown != 0:
            self.dash_cooldown -= 1
        amplifier = 1
        keys = key.get_pressed()
        if keys[K_z] or keys[K_s] or keys[K_d] or keys[K_q]:
            self.facing_x = 0
            self.facing_y = 0
            self.is_moving = True
        else:
            self.is_moving = False
        self.vx *= 0.95
        self.vy *= 0.95
        if keys[K_z]:
            self.vy = min(-0.5,self.vy)
            self.facing_y -= 1
        if keys[K_s]:
            self.vy = max(0.5,self.vy)
            self.facing_y += 1
        if keys[K_q]:
            self.vx = min(-0.5,self.vx)
            self.facing_x -= 1
            self.lr = 1
        if keys[K_d]:
            self.vx = max(0.5,self.vx)
            self.facing_x += 1
            self.lr = 0
        if keys[K_LSHIFT]:
            amplifier = 0.5
        if keys[K_SPACE] and self.dash_cooldown == 0:
            self.vy = self.facing_y*10
            self.vx = self.facing_x*10
            self.dash_cooldown = 200
        self.x += self.vx*amplifier
        self.y += self.vy*amplifier
    
    def show(self,screen):
        screen.blit(self.frame_list[self.lr][self.frame],(640-64,360-64))
        if self.frame_count == 30:
            self.frame = (self.frame + 1)%4
            self.frame_count = 0
        if self.is_moving:
            self.frame_count += 1