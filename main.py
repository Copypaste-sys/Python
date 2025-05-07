import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")


WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


clock = pygame.time.Clock()
fps = 60

bird_size = 30
bird_x = 100
bird_y = HEIGHT // 2
bird_vel = 0
gravity = 0.5
jump = -8


pipe_w = 50
pipe_gap = 150
pipe_vel = 3
pipes = []

pipe_timer = 0


score = 0
font = pygame.font.Font(None, 36)

def img_sc(patch,width,height):
    img = pygame.image.load(patch).convert_alpha()
    return pygame.transform.scale(img, (width, height))

bird_img = img_sc("yellowbird-midflap.png", bird_size * 2, bird_size* 2)
Pipe_img = img_sc("Pipe.png", pipe_w, 200)
bottom_img = img_sc("bottom.jpg", pipe_w, 200)
try:
    bg_img = pygame.image.load("sky.jpg").convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
except:
    bg_img = None


def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))


running = True
while running == True:
    if bg_img:
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill((0, 150, 255))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                bird_vel = jump

    bird_vel += gravity
    bird_y += bird_vel

    if bird_y > HEIGHT - bird_size or bird_y < 0:
        running = False


    pipe_timer += 1
    if pipe_timer > 90:
        pipe_h = random.randint(100, HEIGHT - pipe_gap - 100)
        pipes.append([WIDTH, pipe_h, False])
        pipe_timer = 0

    new_pipes = []

    bird_rect = pygame.Rect(bird_x, bird_y, bird_size, bird_size)


    for i in pipes:
        i[0] -= pipe_vel
        if i[0] + pipe_w > 0:
            new_pipes.append(i)


        top_rect = pygame.Rect(i[0], 0, pipe_w, i[1])
        bottom_rect = pygame.Rect(i[0], i[1] + pipe_gap, pipe_w, HEIGHT - i[1] - pipe_gap)

        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)



        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            running = False

        if not i[2] and i[0] + pipe_w < bird_x:
            score += 1
            i[2] = True

    pipes = new_pipes
    screen.blit(bird_img, (bird_x, bird_y))

    draw_text(f"Очки: {score}", 10, 10)

    pygame.display.flip()
    clock.tick(fps)

print(score)
pygame.quit()