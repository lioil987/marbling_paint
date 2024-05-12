import random
import tkinter as tk
from math import cos, sin, sqrt, pi
from random import choice

root = tk.Tk()
root.title("marbling")
window_width = 4000
window_height = 2000
# Create a canvas
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

canvas.create_polygon([(0, 0), (window_width, 0), (window_width, window_height), (0, window_height)],
                      fill="white")

center = (window_width / 2, window_height / 2)

circles = []


class circle:
    def __init__(self, x=center[0], y=center[1]):
        self.points = [(x, y)]
        self._points = []
        self.position = (x, y)
        self.circle_radius = random.randint(50,300)
        self._points.append((self.circle_radius, 0))
        self.side = 600
        self.angel = 360 / self.side
        self.radian = (self.angel / 180) * pi
        self.color = choice(
            ["Red", "Green", "Blue", "Yellow", "Purple", "Orange", "Pink", "Brown", "Gray", "Black"])
        self.calculate_dot()
        circles.append(self)

    def calculate_dot(self):
        x = self._points[-1][0]
        y = self._points[-1][1]

        xn = x * cos(self.radian) - y * sin(self.radian)
        yn = y * cos(self.radian) + x * sin(self.radian)
        point = (xn, yn)
        self._points.append(point)
        self.points.append((xn+self.position[0], yn+self.position[1]))
        if len(self._points)-1 > self.side:
            return None
        else:
            self.calculate_dot()

    def draw_dot(self):
        canvas.create_polygon(*self.points, fill=self.color)

    def draw(self):
        self.draw_dot()


class manage_window:
    @staticmethod
    def mathematical(c: tuple, p: tuple, r: float):
        euc = sqrt(pow((c[0] - p[0]), 2) + pow((c[1] - p[1]), 2))
        right_p = None
        if euc !=0:
            right_p = sqrt((pow(r, 2) / pow(euc,2))+1)
        else:
            right_p = sqrt((pow(r, 2) / 1))
        mines = (p[0] - c[0], p[1] - c[1])
        right = (right_p * mines[0], right_p * mines[1])
        result = (right[0] + c[0], right[1] + c[1])
        return result



    @staticmethod
    def calculate_new_circles(circle):
        circleI =circle
        for circleII in circles:
                if not circleII == circleI:
                    for index in range(0, len(circleII.points)):
                        temp = manage_window.mathematical(circleI.position, circleII.points[index] ,circleI.circle_radius)
                        circleII.points[index] = temp

    @staticmethod
    def draw_circle(event):

        manage_window.calculate_new_circles(circle(event.x, event.y))
        manage_window.redraw_circle()

    @staticmethod
    def redraw_circle():
        canvas.create_polygon([(0, 0), (window_width, 0), (window_width, window_height), (0, window_height)],
                              fill="white")
        for circleI in circles:
            circleI.draw()


root.bind("<Button-1>", manage_window.draw_circle)

root.mainloop()
