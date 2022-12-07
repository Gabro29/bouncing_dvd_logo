from tkinter import Tk, Canvas, Label
from time import sleep
from threading import Thread
from numpy import random
from math import sin, cos, sqrt, pow
from random import choice
from decimal import Decimal, getcontext


class SQUARE(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Bouncing DVD Logo")
        self.WIDTH = 640
        self.HEIGHT = 640
        self.geometry(f"{self.WIDTH + 100}x{self.HEIGHT + 100}+{500}+{100}")
        self.resizable(0, 0)
        self.propagate(False)

        self.dim_sqaure = Decimal(1)
        getcontext().prec = 70
        self.bad_value = Decimal(0)
        self.offset = self.dim_sqaure

        # Place the frame in which draw the SQUARE
        self.frame = Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg="purple")
        self.frame.place(relx=0.05, rely=0.005)

        self.after(999, Thread(target=self.main).start())

    @staticmethod
    def generate_irrational_numbers(bad_value=0):
        """Rejection method for generating random numbers"""
        r1 = Decimal(random.rand())
        r2 = Decimal(random.rand())

        while Decimal(sin(r2)) > Decimal(cos(r1)) or bad_value == 0:
            bad_value = Decimal(sin(r2) / sin(1))
            r1 = Decimal(random.rand())
            r2 = Decimal(random.rand())
        return Decimal(bad_value)

    def check_position(self, event):
        touch = False

        if self.x1 >= self.WIDTH and self.y1 >= self.HEIGHT:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif self.x1 >= self.WIDTH and 0 < self.y1 < self.HEIGHT:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif self.x1 >= self.WIDTH and self.y1 <= 0.0:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif 0 < self.x1 < self.WIDTH and self.y1 <= 0.0:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif self.x1 <= 0.0 and self.y1 >= self.HEIGHT:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif self.x1 <= 0.0 and 0.0 < self.y1 < self.HEIGHT:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif self.x1 <= 0.0 and self.y1 <= 0.0:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        elif 0 < self.x1 < self.WIDTH and self.y1 >= self.HEIGHT:
            touch = True
            event = self.define_moves_after_collision(event, self.x1, self.y1)

        return event

    def define_moves_after_collision(self, event, x1, y1):
        """Get collision and return the correspective value of bouncing"""

        if self.x1 >= self.WIDTH and self.y1 >= self.HEIGHT:
            if event == "DOWN-RIGHT":
                event = "UP-LEFT"

        elif x1 >= self.WIDTH and 0 < y1 < self.HEIGHT:
            if event == "UP-RIGHT":
                event = "UP-LEFT"

            if event == "DOWN-RIGHT":
                event = "DOWN-LEFT"

        elif x1 >= self.WIDTH and y1 <= 0:
            if event == "UP-RIGHT":
                event = "DOWN-LEFT"

        elif 0 < x1 < self.WIDTH and y1 <= 0:
            if event == "UP-LEFT":
                event = "DOWN-LEFT"

            if event == "UP-RIGHT":
                event = "DOWN-RIGHT"

        elif x1 <= 0 and y1 >= self.HEIGHT:
            if event == "DOWN-LEFT":
                event = "UP-RIGHT"

        elif x1 <= 0 and 0 < y1 < self.HEIGHT:
            if event == "UP-LEFT":
                event = "UP-RIGHT"

            if event == "DOWN-LEFT":
                event = "DOWN-RIGHT"

        elif x1 <= 0 and y1 <= 0:
            if event == "UP-LEFT":
                event = "DOWN-RIGHT"

        elif 0 < x1 < self.WIDTH and y1 >= self.HEIGHT:
            if event == "DOWN-LEFT":
                event = "UP-LEFT"

            if event == "DOWN-RIGHT":
                event = "UP-RIGHT"

        return event

    def draw_rect(self, x1, y1):
        """Draw the rectangle on the next position"""
        self.boncing_logo((x1 + self.bad_value, y1 + self.bad_value, x1 + self.dim_sqaure + self.bad_value, y1 + self.dim_sqaure + self.bad_value), fill="green")

    def del_rect(self, x1, y1):
        """Track the position of the moving rectangle"""
        self.boncing_logo(x1 + self.bad_value, y1 + self.bad_value, x1 + self.dim_sqaure + self.bad_value, y1 + self.dim_sqaure + self.bad_value, fill="white")

    def bouncing_move(self, event):
        """Start SQUARE to move on the screen"""
        if event == "ds":
            self.del_rect(self.x1, self.y1)
            self.x1 -= self.bad_value
            self.y1 += self.bad_value
        elif event == "as":
            self.del_rect(self.x1, self.y1)
            self.x1 += self.bad_value
            self.y1 += self.bad_value
        elif event == "wd":
            self.del_rect(self.x1, self.y1)
            self.x1 += self.bad_value
            self.y1 -= self.bad_value
        elif event == "wa":
            self.del_rect(self.x1, self.y1)
            self.x1 -= self.bad_value
            self.y1 -= self.bad_value

        self.draw_rect(self.x1, self.y1)

    def main(self):
        self.bad_value = self.generate_irrational_numbers()
        self.x1 = Decimal(random.randint(0, self.WIDTH))
        self.y1 = Decimal(random.randint(0, self.HEIGHT))

        # Draw the SQUARE
        self.boncing_logo = self.frame.create_rectangle
        self.boncing_logo((Decimal(self.x1 + self.bad_value), Decimal(self.y1 + self.bad_value), Decimal(self.x1 + self.dim_sqaure + self.bad_value), Decimal(self.y1 + self.dim_sqaure + self.bad_value)))

        moves = {"UP-LEFT": 'wa', "DOWN-LEFT": 'ds', "UP-RIGHT": 'wd', "DOWN-RIGHT": 'as'}
        event = random.choice(list(moves.keys()))
        first = True
        while True:
            self.bouncing_move(moves[event])
            self.update_idletasks()
            event = self.check_position(event)

            if first:
                first = False
                with open("bad_value.txt", 'a') as file:
                    file.write(f"\n({self.x1}, {self.y1}) {self.bad_value}, {moves[event]}")


if __name__ == "__main__":
    SQUARE().mainloop()
