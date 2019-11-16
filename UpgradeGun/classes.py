from random import randrange as rnd, choice, uniform
import math


# класс шариков
class Ball:
    def __init__(self, canvas, x=None, y=None, vx=None, vy=None, r=None, color=None, g=0.0, k=0.0, u=0.0):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        x = self.x = rnd(350, 480) if x is None else x
        y = self.y = rnd(300, 450) if y is None else y
        r = self.r = rnd(2, 50) if r is None else r
        vy = self.vy = rnd(10, 20) * choice([-1, 1]) if vy is None else vy
        vx = self.vx = rnd(10, 20) * choice([-1, 1]) if vx is None else vx
        color = self.color = choice(['blue', 'green', 'pink', 'brown', 'yellow', 'purple']) if color is None else color
        self.g = g
        self.u = u
        self.k = k
        self.canvas = canvas
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 20
        self.in_air = True

    def set_coords(self):
        self.canvas.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.vy < 5 and self.y >= 600 - self.r and self.g > 0:
            self.in_air = False
        self.collision()
        self.x += self.vx
        if self.in_air:
            self.y += self.vy
            self.vy += self.g
        else:
            self.vx *= (1 - self.u)
            self.live -= 1
        self.set_coords()

    def collision(self):
        flag = False
        if self.x > 800 - self.r:
            self.vx = -self.vx * (1 - self.k)
            self.vy *= (1 - self.u)
            self.x = 800 - self.r
            flag = True
        if self.x < self.r:
            self.vx = -self.vx * (1 - self.k)
            self.vy *= (1 - self.u)
            self.x = self.r
            flag = True
        if self.y > 600 - self.r:
            self.vy = -self.vy * (1 - self.k)
            self.vx *= (1 - self.u)
            self.y = 600 - self.r
            flag = True
        if self.y < self.r:
            self.vy = -self.vy * (1 - self.k)
            self.vx *= (1 - self.u)
            self.y = self.r
            flag = True
        return flag


# класс снарядов
class Bullet(Ball):
    def __init__(self, canv):
        super().__init__(canvas=canv, x=40, y=450, r=10, g=1.5, k=0.9, u=0.7)
        self.life = 20

    def collision(self):
        if super().collision():
            self.life -= 1

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


# класс целей
class Target(Ball):
    def __init__(self, canvas=None):
        self.live = 1
        self.points = 0
        vx = rnd(4, 10) * choice([-1, 1])
        vy = rnd(4, 10) * choice([-1, 1])
        y = self.y = rnd(300, 550)
        x = self.x = rnd(600, 740)
        r = self.r = rnd(10, 50)
        color = self.color = 'red'

        super().__init__(canvas, x, y, vx, vy, r, color, 0, 0, 0)
        super().set_coords()

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.canvas.delete(self.id)


# класс пушек
class Gun:
    def __init__(self, canvas=None, balls=None):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.canvas = canvas
        self.id = self.canvas.create_line(20, 450, 50, 420, width=7)
        self.balls = balls
        self.num_bullets = 0
        self.canvas = canvas

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.A
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        self.num_bullets += 1
        new_ball = Bullet(self.canvas)
        new_ball.r += 5
        self.angle = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.angle)
        new_ball.vy = self.f2_power * math.sin(self.angle)
        self.balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targeting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            self.canvas.itemconfig(self.id, fill='orange')
        else:
            self.canvas.itemconfig(self.id, fill='black')
        self.canvas.coords(self.id, 20, 450,
                           20 + max(self.f2_power, 20) * math.cos(self.angle),
                           450 + max(self.f2_power, 20) * math.sin(self.angle)
                           )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1


# класс табло
class Scoreboard:
    def __init__(self, canvas=None):
        self.score = 0
        self.canvas = canvas
        self.id_points = self.canvas.create_text(30, 30, text=self.score, font='30')

    def update_score(self, point=1):
        self.score += point
        self.canvas.itemconfig(self.id_points, text=self.score)
