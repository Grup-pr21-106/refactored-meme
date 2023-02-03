from kivymd.app import MDApp
from kivymd.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    # Отскок мячика при коллизии с панелькой игрока
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):

    # Скорость движения нашего шарика по двум осям
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # Создаем условный вектор
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)  # связь с объектом шарика
    player1 = ObjectProperty(None)  # Игрок 1
    player2 = ObjectProperty(None)  # Игрок 2

    # начальный угол
    def serve_ball(self, vel=(3, 2)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()  # двигаем шарик в каждом обновлении экрана

        # проверка отскока шарика от панелек игроков
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # отскок шарика по оси Y
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        # отскок шарика по оси X
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 1))

        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 1))

    # Событие прикосновения к экрану
    def on_touch_move(self, touch):

        if touch.x < self.width / 3:
            self.player1.center_y = touch.y

        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class PongApp(MDApp):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60)  # 60 FPS
        return game


if __name__ == '__main__':
    PongApp().run()
