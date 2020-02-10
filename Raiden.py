import pygame
import sys
import os


os.environ['SDL_VIDEO_CENTERED'] = '1'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 185, 0)
YELLOW = (255, 245, 50)
RED = (255, 0, 0)
BLUE = (50, 135, 255)
GRAY = (80, 80, 80)
fps = 60
SHIP_WIDTH = 30
SHIP_HEIGHT = 50
size = WIDTH, HEIGHT = 16 * 32, 700
timer = 0
count = 0
count2 = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 5
        self.image = pygame.Surface((32, 32)).convert()
        self.image.fill(GRAY)
        self.rect = pygame.Rect(xpos, ypos, 32, 32)


class Ship(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.top_speed = 4
        self.side_speed = 5
        self.image = pygame.Surface((32, 32)).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.container.centerx
        self.rect.y = self.container.bottom - (3 * self.rect.height)
        self.energy = 10000

    def update(self, camera_entity, bullet_group, huey_bullet_group):
        global timer
        key = pygame.key.get_pressed()
        if camera_entity.rect.y < self.container.bottom - HEIGHT / 2:
            if key[pygame.K_w] or key[pygame.K_UP]:
                self.rect.y -= self.top_speed
            if key[pygame.K_s] or key[pygame.K_DOWN]:
                self.rect.y += self.top_speed
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                self.rect.x += self.side_speed
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                self.rect.x -= self.side_speed
            if key[pygame.K_SPACE]:
                if timer % 10 == 0:
                    bullet = Bullet(self.container, self.rect.centerx - 20, self.rect.y + self.rect.height / 4, True, 0,-15)
                    bullet2 = Bullet(self.container, self.rect.centerx + 10, self.rect.y + self.rect.height / 4, True, 0,-15)
                    bullet_group.add(bullet)
                    bullet_group.add(bullet2)
                    timer += 1

        if camera_entity.is_moving:
            self.rect.y -= 1

        if self.rect.bottom > camera_entity.rect.y + HEIGHT / 2:
            self.rect.bottom = camera_entity.rect.y + HEIGHT / 2

        if self.rect.top < camera_entity.rect.y - HEIGHT / 2:
            self.rect.top = camera_entity.rect.y - HEIGHT / 2
        elif camera_entity.rect.y == HEIGHT/2 and self.rect.bottom > camera_entity.rect.y + HEIGHT / 2:
            self.rect.bottom = camera_entity.rect.y + HEIGHT / 2

        collisions = pygame.sprite.spritecollide(self, huey_bullet_group, True)
        for h in collisions:
            self.energy -= 500

        if self.energy == 0:
            self.kill()

        self.rect.clamp_ip(self.container)


class Camera:
    def __init__(self, container):
        self.x_offset = 0
        self.y_offset = 0
        self.width = container.width
        self.height = container.height

    def apply(self, obj):
        return pygame.Rect(obj.rect.x + self.x_offset, obj.rect.y + self.y_offset, obj.rect.width, obj.rect.height)

    def update(self, ship, camera_entity):
        self.x_offset = -ship.rect.x + WIDTH / 2
        self.y_offset = -camera_entity.rect.y + HEIGHT / 2

        if self.x_offset < -(self.width - WIDTH):
            self.x_offset = -(self.width - WIDTH)

        if self.x_offset > 0:
            self.x_offset = 0

        if self.y_offset < -(self.height - HEIGHT):
            self.y_offset = -(self.height - HEIGHT)

        if self.y_offset > 0:
            self.y_offset = 0


class Camera_Entity(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.image = pygame.Surface((10, 10)).convert()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = container.centerx
        self.rect.centery = container.bottom
        self.is_moving = False

    def update(self, container):
        if self.rect.top > HEIGHT/2:
            self.rect.y -= 1

        if self.rect.top < container.height - HEIGHT/2 and self.rect.top > HEIGHT/2:
            self.is_moving = True
        else:
            self.is_moving = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, container, xpos, ypos, dir, dx,dy):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.image = pygame.Surface((10, 10)).convert()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(xpos, ypos)
        self.dir = dir
        self.dx = dx
        self.dy = dy

    def update(self, camera):
        self.rect.x -= self.dx
        self.rect.y += self.dy

        if self.rect.y < -camera.y_offset:
            self.kill()

        if self.rect.y > -camera.y_offset + HEIGHT:
            self.kill()


class Huey(pygame.sprite.Sprite):
    def __init__(self, container):
        pygame.sprite.Sprite.__init__(self)
        self.container = container
        self.side_speed = 5
        self.top_speed = 4
        self.image = pygame.Surface((75, 75)).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.container.centerx
        self.rect.y = self.container.bottom - HEIGHT - self.rect.height
        self.dir = True
        self.xpos = self.rect.x
        self.dis = 150
        self.energy = 100000

    def update(self, huey_bullet_group, bullet_group, camera_entity, camera):
        global timer, count

        if -camera.y_offset < self.rect.y + self.rect.height:
            if timer % 120 == 2:
                bullet = Bullet(self.container, self.rect.centerx - 5, self.rect.bottom, False, 0, 15)
                bullet2 = Bullet(self.container, self.rect.centerx - 5, self.rect.bottom, False, 5, 15)
                bullet3 = Bullet(self.container, self.rect.centerx - 5, self.rect.bottom, False, -5, 15)
                huey_bullet_group.add(bullet)
                huey_bullet_group.add(bullet2)
                huey_bullet_group.add(bullet3)
                timer += 1

        if self.rect.y > -camera.y_offset + self.rect.height:
            self.rect.y -= 1

            if self.dir:
                self.rect.x -= 1
                if self.rect.x < self.xpos - self.dis:
                    self.dir = False
            else:
                self.rect.x += 1
                if self.rect.x > self.xpos + self.dis:
                    self.dir = True
        if count >= 2500:
            self.rect.y += 3
            self.rect.x += 5


        collisions = pygame.sprite.spritecollide(self, bullet_group, True)
        for b in collisions:
            self.energy -= 500

        if self.energy == 0:
            self.kill()


def main():
    global fps, size, timer, count
    pygame.init()
    pygame.display.set_caption('Raiden')
    clock = pygame.time.Clock()
    play = True
    screen = pygame.display.set_mode(size, pygame.SRCALPHA)
    platform_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    huey_bullet_group = pygame.sprite.Group()
    ship_group = pygame.sprite.Group()
    huey_group = pygame.sprite.Group()
    level = [
       "PPPPPPPPPPPPPPPPPPPPPPPPPPP",
       "P                         P",
       "P                         P",
       "P                  PPPPPPPP",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                         P",
       "P                         P",
       "P                   PPPPPPP",
       "P                         P",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                    PPPPPP",
       "PPPPPP                    P",
       "P                         P",
       "P                         P",
       "P             PPPPPPPPPPPPP",
       "P                         P",
       "P                         P",
       "P                         P",
       "PPPPP                     P",
       "P                         P",
       "P                     PPPPP",
       "P                         P",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                    PPPPPP",
       "PPPPPP                    P",
       "P                         P",
       "P                         P",
       "P             PPPPPPPPPPPPP",
       "P                         P",
       "P                         P",
       "P                         P",
       "PPPPP                     P",
       "P                         P",
       "P                     PPPPP",
       "PPPPPPPPPPPP              P",
       "P                         P",
       "P                         P",
       "P                      PPPP",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                         P",
       "P                  PPPPPPPP",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                         P",
       "P                         P",
       "P                   PPPPPPP",
       "P                         P",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                    PPPPPP",
       "PPPPPP                    P",
       "P                         P",
       "P                         P",
       "P             PPPPPPPPPPPPP",
       "P                         P",
       "P                         P",
       "P                         P",
       "PPPPP                     P",
       "P                         P",
       "P                     PPPPP",
       "P                         P",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                    PPPPPP",
       "PPPPPP                    P",
       "P                         P",
       "P                         P",
       "P             PPPPPPPPPPPPP",
       "P                         P",
       "P                         P",
       "P                         P",
       "PPPPP                     P",
       "P                         P",
       "P                     PPPPP",
       "PPPPPPPPPPPP              P",
       "P                         P",
       "P                         P",
       "P                      PPPP",
       "P                         P",
       "PPPPPPPPPP                P",
       "P                         P",
       "P                         P",
       "PPPPPPPPPPPPPPPPPPPPPPPPPPP", ]

    container = pygame.Rect(0, 0, len(level[0]) * 32, len(level) * 32)
    ship = Ship(container)
    camera = Camera(container)
    camera_entity = Camera_Entity(container)
    huey = Huey(container)
    ship_group.add(ship)
    huey_group.add(huey)

    x = y = 0

    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platform_group.add(p)
            x += 32
        y += 32
        x = 0

    platform_group.add(camera_entity)

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        ship_group.update(camera_entity, bullet_group, huey_bullet_group)
        camera_entity.update(container)
        camera.update(ship, camera_entity)
        bullet_group.update(camera)
        huey_bullet_group.update(camera)
        huey_group.update(huey_bullet_group, bullet_group, camera_entity, camera)

        screen.fill(WHITE)

        for p in platform_group:
            screen.blit(p.image, camera.apply(p))
        for s in ship_group:
            screen.blit(s.image, camera.apply(s))
        for h in huey_group:
            screen.blit(h.image, camera.apply(h))
        for h in huey_bullet_group:
            screen.blit(h.image, camera.apply(h))
        for b in bullet_group:
            screen.blit(b.image, camera.apply(b))
        count += 1
        timer += 1
        clock.tick(fps)
        pygame.display.flip()

if __name__ == "__main__":
    main()
