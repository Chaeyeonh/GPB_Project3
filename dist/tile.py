import pygame
class Tile:
    def __init__(self, position, width, height, sound_file, color):
        self.position = position  # (x, y)
        self.width = width
        self.height = height
        self.color = color  # 타일 색상
        self.sound = pygame.mixer.Sound(sound_file)  # 사운드 로드

    def is_collided(self, ball):
        ball_x, ball_y = ball.position
        tile_x, tile_y = self.position
        return (tile_x <= ball_x <= tile_x + self.width) and (ball_y + ball.radius >= tile_y)

    def play_sound(self, ball_mass):
        volume = Tile.calculate_volume(ball_mass)  # 정적 메서드 호출
        self.sound.set_volume(volume)
        self.sound.play()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.width, self.height))

    @staticmethod
    def calculate_volume(mass, min_mass=1, max_mass=10):
        """
        질량에 따라 음량을 계산 (0.0 ~ 1.0 사이 값 반환).
        """
        volume = (mass - min_mass) / (max_mass - min_mass)
        return max(0.0, min(1.0, volume))  # 0.0 ~ 1.0 사이로 제한
