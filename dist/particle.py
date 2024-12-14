import pygame
import random

class Particle:
    def __init__(self, position, velocity, lifetime, color, size):
        self.position = list(position)
        self.velocity = list(velocity)
        self.lifetime = lifetime
        self.color = color
        self.size = size

    def update(self):
        # 속도에 따라 위치 업데이트
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # 수명 감소
        self.lifetime -= 1

    def draw(self, screen):
      if self.lifetime > 0:
          # 수명에 따라 색상 변화
          alpha = max(0, int(255 * (self.lifetime / 40)))
          color = (self.color[0], self.color[1], self.color[2], alpha)
          
          surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
          pygame.draw.circle(surface, color, (self.size, self.size), self.size)
          screen.blit(surface, (int(self.position[0] - self.size), int(self.position[1] - self.size)))


    def is_alive(self):
        return self.lifetime > 0


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, position):
        # 여러 개의 파티클 생성
        print(f"Emitting particles at position: {position}")
        for _ in range(20):  # 한 번에 20개의 파티클 생성
            velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
            lifetime = random.randint(20, 40)
            color = (255, random.randint(100, 255), 0)  # 주황색 계열
            size = random.randint(2, 4)
            self.particles.append(Particle(position, velocity, lifetime, color, size))

    def update(self):
        # 모든 파티클 업데이트
        for particle in self.particles:
            particle.update()

        # 수명이 다한 파티클 제거
        self.particles = [particle for particle in self.particles if particle.is_alive()]

    def draw(self, screen):
        # 모든 파티클 그리기
        for particle in self.particles:
            particle.draw(screen)
