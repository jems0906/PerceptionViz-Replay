from dataclasses import dataclass


@dataclass
class ConstantVelocityState:
    x: float
    y: float
    vx: float = 0.0
    vy: float = 0.0

    def predict(self) -> tuple[float, float]:
        self.x += self.vx
        self.y += self.vy
        return self.x, self.y

    def update(self, x: float, y: float) -> tuple[float, float]:
        self.vx = 0.65 * self.vx + 0.35 * (x - self.x)
        self.vy = 0.65 * self.vy + 0.35 * (y - self.y)
        self.x = x
        self.y = y
        return self.x, self.y
