import math

class Ball:
    def __init__(self, position, velocity, radius):
        self.position = position  # (x, y)
        self.velocity = velocity  # (vx, vy)
        self.radius = radius  # 반지름
        self.mass = math.pi * (radius / 10) ** 3  # 반지름에 비례한 질량
        self.acceleration = (0, 0)  # 중력 가속도
        
    #중력 적용
    def apply_gravity(self, gravity=50):
        self.acceleration = (0, gravity)

    #바닥과 충돌 시 반동 효과를 적용.
    def bounce(self, restitution=0.8, is_on_ground=True):
        if is_on_ground:
            vx, vy = self.velocity
            # y축 속도를 반사시키고, 질량과 탄성 계수를 반영
            dynamic_restitution = restitution + (1 - restitution) * (1 / self.mass)
            self.velocity = (vx, -vy * dynamic_restitution)
            
   
    #중력을 고려한 공의 속도 및 위치 업데이트.
    def update(self, delta_time, is_on_ground):
        # 속도 업데이트
        vx, vy = self.velocity
        ax, ay = self.acceleration
        self.velocity = (vx + ax * delta_time, vy + ay * delta_time)

        # 위치 업데이트
        x, y = self.position
        self.position = (x + self.velocity[0] * delta_time, y + self.velocity[1] * delta_time)

        # 바닥과 충돌 시 반동 적용
        if is_on_ground and self.velocity[1] > 0:  # 아래 방향 속도일 경우 반동 처리
            self.bounce()

    #두 공간 충돌 감지
    def detect_collision(self, other_ball, restitution=0.8):
        dx = self.position[0] - other_ball.position[0]
        dy = self.position[1] - other_ball.position[1]
        distance = math.sqrt(dx**2 + dy**2)

        # 충돌 조건: 두 공의 중심 간 거리가 반지름의 합보다 작음
        if distance < self.radius + other_ball.radius:
            # 충돌 처리
            normal = (dx / distance, dy / distance)
            relative_velocity = (
                self.velocity[0] - other_ball.velocity[0],
                self.velocity[1] - other_ball.velocity[1],
            )
            velocity_along_normal = relative_velocity[0] * normal[0] + relative_velocity[1] * normal[1]

            if velocity_along_normal > 0:  # 이미 서로 멀어지는 경우
                return False

            # 충격량 계산
            m1, m2 = self.mass, other_ball.mass
            impulse = -(1 + restitution) * velocity_along_normal / (1 / m1 + 1 / m2)
            impulse_vector = (impulse * normal[0], impulse * normal[1])

            # 운동량 보존에 따른 속도 업데이트
            self.velocity = (
                self.velocity[0] + impulse_vector[0] / m1,
                self.velocity[1] + impulse_vector[1] / m1,
            )
            other_ball.velocity = (
                other_ball.velocity[0] - impulse_vector[0] / m2,
                other_ball.velocity[1] - impulse_vector[1] / m2,
            )
            return True
        return False