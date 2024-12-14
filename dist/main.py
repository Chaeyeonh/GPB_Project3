import pygame
import random
from ball import Ball
from tile import Tile
from particle import ParticleSystem

pygame.init()
pygame.mixer.init()  # 믹서 초기화
pygame.mixer.set_num_channels(32)
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Harmony of Collisions")
clock = pygame.time.Clock()
FPS = 60
background = pygame.image.load('background.jpg')  # 배경 이미지 로드
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 크기에 맞게 조정
WHITE = (255, 255, 255)

TILE_COLORS = [
    (255, 0, 0),    # 빨강
    (255, 165, 0),  # 주황
    (255, 255, 0),  # 노랑
    (0, 128, 0),    # 초록
    (0, 0, 255),    # 파랑
    (75, 0, 130),   # 남색
    (148, 0, 211),  # 보라
]

# 충돌 사운드 파일
COLLISION_SOUND = "sound/drum.mp3" 

tile_width = SCREEN_WIDTH // 7
tile_height = 20
tiles = [
    Tile(
        position=(i * tile_width, SCREEN_HEIGHT - tile_height),
        width=tile_width,
        height=tile_height,
        sound_file=f"sound/{i+1}.mp3",
        color=TILE_COLORS[i]
    )
    for i in range(7)
]

# 충돌 사운드 미리 로드
collision_sound = pygame.mixer.Sound(COLLISION_SOUND)
# 파티클 시스템 초기화
particle_system = ParticleSystem()

def run_game():
    balls = []
    running = True
    
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
              # 클릭한 공이 있는지 확인
                ball_removed = False
                for ball in balls[:]:
                    distance = ((x - ball.position[0])**2 + (y - ball.position[1])**2)**0.5
                    if distance <= ball.radius:
                        print(f"Ball clicked and removed: {ball}")
                        particle_system.emit(ball.position)
                        balls.remove(ball)
                        ball_removed = True
                        break

                # 공이 없거나 클릭한 공이 없으면 새 공 생성
                if not ball_removed:
                    print('Creating new ball...')
                    radius = random.randint(10, 30)
                    new_ball = Ball((x, y), (0, 0), radius)
                    balls.append(new_ball)
                    print(f"New ball created at ({x}, {y}) with radius {radius}")

        # 배경 그리기
        screen.blit(background, (0, 0))

        for tile in tiles:
            tile.draw(screen)

        # 공 간 충돌 처리 -> 드럼 사운드 재생
        for i, ball1 in enumerate(balls):
            for ball2 in balls[i + 1:]:
                if ball1.detect_collision(ball2):  # 충돌 감지 및 처리
                    collision_sound.play()  # 충돌 사운드 재생

        # 각 공에 중력 적용 및 속도, 가속도 업데이트 
        for ball in balls:
            # 바닥 접촉 여부 확인
            is_on_ground = ball.position[1] + ball.radius >= SCREEN_HEIGHT - tile_height
            ball.apply_gravity()
            ball.update(1 / FPS, is_on_ground)

        # 타일과 공의 충돌 처리
            for tile in tiles:
                if tile.is_collided(ball):
                    ball.position = (ball.position[0], tile.position[1] - ball.radius)
                    ball.bounce(restitution=0.8)
                    tile.play_sound(ball.mass)

            pygame.draw.circle(screen, (255, 255, 255), (int(ball.position[0]), int(ball.position[1])), ball.radius)

        # 파티클 시스템 업데이트 및 그리기
        particle_system.update()
        particle_system.draw(screen)

        #화면 업데이트
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    run_game()
