import pygame
import math
import numpy as np
import cv2 

pygame.init()

w, h = 640, 480
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

# For video writer
video_filename = "stickman_animation.mp4"
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_filename, fourcc, fps, (w, h))

x1 = 50
x2 = 590
y = 300

bird_x = [100, 300, 500]
bird_y = [60, 80, 50]

frame = 0
state = "walk"
shake_frame = 0

def draw_background():
    screen.fill((200, 230, 255))
    pygame.draw.circle(screen, (255, 244, 122), (550, 80), 40)
    pygame.draw.ellipse(screen, (255, 255, 255), (80, 50, 100, 40))
    pygame.draw.ellipse(screen, (255, 255, 255), (110, 40, 120, 50))
    pygame.draw.ellipse(screen, (255, 255, 255), (140, 50, 100, 40))
    pygame.draw.rect(screen, (180, 255, 180), (0, y + 40, w, h - y - 40))
    for i in range(0, w, 60):
        height = 100 + (i % 120)
        pygame.draw.polygon(screen, (200, 200, 200), [(i, y + 40), (i + 30, y + 40 - height), (i + 60, y + 40)])

def draw_birds():
    for i in range(len(bird_x)):
        pygame.draw.arc(screen, (0, 0, 0), (bird_x[i], bird_y[i], 20, 10), 3.14, 6.28, 2)
        pygame.draw.arc(screen, (0, 0, 0), (bird_x[i] + 10, bird_y[i], 20, 10), 3.14, 6.28, 2)
        bird_x[i] -= 2
        if bird_x[i] < -40:
            bird_x[i] = w + 20

def draw_stickman(x, y, pose="default", flip=False, frame=0):
    direction = -1 if flip else 1
    pygame.draw.circle(screen, (0, 0, 0), (x, y - 60), 20)
    pygame.draw.line(screen, (0, 0, 0), (x, y - 40), (x, y), 3)
    if pose == "shake":
        pygame.draw.line(screen, (0, 0, 0), (x, y - 30), (x + 15 * direction, y - 15), 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y - 30), (x - 15 * direction, y - 15), 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x - 10, y + 30), 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x + 10, y + 30), 3)
    elif pose == "walk":
        step_angle = math.sin(frame * 0.2) * 20
        leg1_end = (x + math.sin(math.radians(step_angle)) * 20,
                    y + math.cos(math.radians(step_angle)) * 30)
        leg2_end = (x - math.sin(math.radians(step_angle)) * 20,
                    y + math.cos(math.radians(step_angle)) * 30)
        arm1_end = (x - math.sin(math.radians(step_angle)) * 15,
                    y - 20 + math.cos(math.radians(step_angle)) * 15)
        arm2_end = (x + math.sin(math.radians(step_angle)) * 15,
                    y - 20 - math.cos(math.radians(step_angle)) * 15)
        pygame.draw.line(screen, (0, 0, 0), (x, y - 30), arm1_end, 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y - 30), arm2_end, 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y), leg1_end, 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y), leg2_end, 3)
    else:
        pygame.draw.line(screen, (0, 0, 0), (x, y - 20), (x - 15, y - 20), 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y - 20), (x + 15, y - 20), 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x - 10, y + 30), 3)
        pygame.draw.line(screen, (0, 0, 0), (x, y), (x + 10, y + 30), 3)

# Frame limit to avoid infinite loop
max_frames = 300  # ~10 seconds of video at 30 fps
while frame < max_frames:
    clock.tick(fps)
    frame += 1

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            video.release()
            exit()

    draw_background()
    draw_birds()

    distance = abs(x1 - x2)
    if state == "walk":
        if distance > 80:
            x1 += 2
            x2 -= 2
        else:
            state = "shake"
            shake_frame = 0
    elif state == "shake":
        shake_frame += 1
        if shake_frame > 20:
            state = "pass"
    elif state == "pass":
        x1 += 2
        x2 -= 2

    if state in ["walk", "pass"]:
        draw_stickman(x1, y, "walk", frame=frame)
        draw_stickman(x2, y, "walk", flip=True, frame=frame)
    elif state == "shake":
        draw_stickman(x1, y, "shake", frame=frame)
        draw_stickman(x2, y, "shake", flip=True, frame=frame)

    pygame.display.update()

    # Save current frame to video
    pixels = pygame.surfarray.array3d(screen)
    frame_bgr = cv2.cvtColor(np.transpose(pixels, (1, 0, 2)), cv2.COLOR_RGB2BGR)
    video.write(frame_bgr)

pygame.quit()
video.release()
print("Video saved:", video_filename)
