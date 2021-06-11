from time import time
import pygame
import time
import random
from pathlib import Path
from ships_and_lasers import PlayerShip, EnemyShip, collide
pygame.font.init()

class SpaceInvadersGame:
    def __init__(self) -> None:
        self.FPS = 60
        self.WIDTH = 750
        self.HEIGHT = 750
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("space invaders")

        self.assets_root = Path(__file__).parent / "assets"
        # Load images
        self.RED_SPACE_SHIP = pygame.image.load(self.assets_root / "pixel_ship_red_small.png")
        self.GREEN_SPACE_SHIP = pygame.image.load(self.assets_root / "pixel_ship_green_small.png")
        self.BLUE_SPACE_SHIP = pygame.image.load(self.assets_root / "pixel_ship_blue_small.png")

        # Player player
        self.YELLOW_SPACE_SHIP = pygame.image.load(self.assets_root / "pixel_ship_yellow.png")

        # Lasers
        self.RED_LASER = pygame.image.load(self.assets_root / "pixel_laser_red.png")
        self.GREEN_LASER = pygame.image.load(self.assets_root / "pixel_laser_green.png")
        self.BLUE_LASER = pygame.image.load(self.assets_root / "pixel_laser_blue.png")
        self.YELLOW_LASER = pygame.image.load(self.assets_root / "pixel_laser_yellow.png")
        self.COLOR_MAP = {
                        "red": (self.RED_SPACE_SHIP, self.RED_LASER),
                        "green": (self.GREEN_SPACE_SHIP, self.GREEN_LASER),
                        "blue": (self.BLUE_SPACE_SHIP, self.BLUE_LASER)
                        }
        # Background
        self.BG = pygame.transform.scale(pygame.image.load(self.assets_root / "background-black.png"), (self.WIDTH, self.HEIGHT))
        
        self.run = True
        self.level = 0
        self.lives = 5
        self.player_velocity = 5
        self.enemies = []
        self.wave_length = 5
        self.enemy_velocity = 1
        self.laser_velocity = 5
        self.lost = False
        self.lost_count = 0
        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 80)
        self.clock = pygame.time.Clock()

        self.main_menu() # start game


    def game(self):
        self.player = PlayerShip(300, 630, self.YELLOW_SPACE_SHIP, self.YELLOW_LASER)
        while self.run:
            self.clock.tick(self.FPS)
            self.redraw_window()

            if self.lives <= 0 or self.player.health <= 0:
                self.lost = True
                self.lost_count += 1
            
            if self.lost:
                if self.lost_count > self.FPS * 3:
                    self.run = False
                else:
                    continue  

            if len(self.enemies) == 0:
                self.level += 1
                self.wave_length += 5
                for i in range(self.wave_length):
                    ship_img, laser_img = self.COLOR_MAP[random.choice(["red", "blue", "green"])]
                    enemy_ship = EnemyShip(random.randrange(50, self.WIDTH-100), random.randrange(-1500, -100), ship_img, laser_img)
                    self.enemies.append(enemy_ship)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and (self.player.x - self.player_velocity > 0): # left
                self.player.x -= self.player_velocity
            if keys[pygame.K_RIGHT] and (self.player.x + self.player_velocity + self.player.get_width() < self.WIDTH): # right
                self.player.x += self.player_velocity
            if keys[pygame.K_UP] and (self.player.y - self.player_velocity > 0): # up
                self.player.y -= self.player_velocity
            if keys[pygame.K_DOWN] and (self.player.y + self.player_velocity + self.player.get_height() + 15 < self.HEIGHT): # down
                self.player.y += self.player_velocity
            if keys[pygame.K_SPACE]: # shoot laser
                self.player.shoot()

            for enemy in self.enemies[:]:
                enemy.move(self.enemy_velocity)
                enemy.move_lasers(self.laser_velocity, self.player, self.HEIGHT)

                if random.randrange(0, 2*self.FPS) == 1:
                    enemy.shoot()
                
                if collide(enemy, self.player):
                    self.player.health -= 10
                    self.enemies.remove(enemy)
                
                elif enemy.y + enemy.get_height() > self.HEIGHT:
                    self.lives -= 1
                    self.enemies.remove(enemy)
            
            self.player.move_lasers(-self.laser_velocity, self.enemies, self.HEIGHT)


    def redraw_window(self):
        self.WIN.blit(self.BG, (0, 0))
        lives_label = self.main_font.render(f"lives: {self.lives}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"level: {self.level}", 1, (255, 255, 255))
        self.WIN.blit(lives_label, (10, 10))
        self.WIN.blit(level_label, (self.WIDTH - level_label.get_width() - 10, 10))
        
        for enemy in self.enemies[:]:
            enemy.draw(self.WIN)
        
        self.player.draw(self.WIN)

        if self.lost:
            lost_label = self.lost_font.render("GAME OVER", 1, (255, 255, 255))
            self.WIN.blit(lost_label, (self.WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()


    def main_menu(self):
        begin_font = pygame.font.SysFont("comicsans", 70)
        while self.run:
            self.WIN.blit(self.BG, (0, 0))
            begin_label = begin_font.render("PRESS ANY KEY TO BEGIN", 1, (255, 255, 255))
            self.WIN.blit(begin_label, (self.WIDTH/2 - begin_label.get_width()/2, 350))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    self.game()
        pygame.quit()


if __name__ == "__main__":
    SpaceInvadersGame()
