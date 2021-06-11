import pygame

class BaseShip:
    def __init__(self, x, y, health=100) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.COOL_DOWN = 30
    
    def draw (self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    

    def move_lasers(self, velocity, object, height):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(object):
                object.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()


    def get_height(self):
        return self.ship_img.get_height()
    

    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class PlayerShip(BaseShip):
    def __init__(self, x, y, ship_img, laser_img, health=100) -> None:
        super().__init__(x, y, health)
        self.ship_img = ship_img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


    def move_lasers(self, velocity, objects, height):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for object in objects:
                    if laser.collision(object):
                        objects.remove(object)
                        if laser in self.lasers:
                            self.lasers.remove(laser)


    def draw(self, window):
        super().draw(window)
        self.health_bar(window)


    def health_bar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * self.health / self.max_health, 10))


class EnemyShip(BaseShip):
    def __init__(self, x, y, ship_img, laser_img, health=100) -> None:
        super().__init__(x, y, health)
        self.ship_img = ship_img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.ship_img)
    

    def move(self, velocity):
       self.y += velocity 


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Laser:
    def __init__(self, x, y, img) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    

    def move(self, veloctiy):
        self.y += veloctiy
    

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None