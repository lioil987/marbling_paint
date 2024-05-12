import random
import tkinter as tk
from math import cos, sin, sqrt, pi
from random import choice


window_width = 3000
window_height = 1500



root = tk.Tk()
root.configure(bg="white")
root.title("marbling")




class scale:

    def __init__(self,platform,length,value,min,max,step,name,):
        self.group_box_frame = tk.Frame(platform, bg="white", bd=5,highlightthickness=0)
        self.group_box_frame.pack(padx=10, pady=10,side=tk.LEFT)

        self.scale = tk.Scale(self.group_box_frame, from_=min, to=max, orient=tk.HORIZONTAL, length=length, showvalue=value, resolution=step,bg="white",border=5)
        self.scale.pack()
        self.selected_value = tk.StringVar(value=f"{name}: {self.scale.get()}")
        self.label = tk.Label(self.group_box_frame, textvariable=self.selected_value,bg="white")
        self.label.pack()
        self.scale.config(command=lambda *args: self.selected_value.set(f"{name}: {self.scale.get()}"))
    def give(self):
        return self.group_box_frame
    def give_value(self):
        return self.scale.get()

class config:
    polygonSides = None
    random_color = True
    random_size = False
    fixed_size = None
    @staticmethod
    def racalc():
        config.polygonSides = poly_side.give_value()
        config.random_color = True
        config.fixed_size = size.give_value()


group_box_menu = tk.Frame(root, bg="white", bd=5)
group_box_menu.pack(fill=tk.BOTH, expand=True)
poly_side = scale(group_box_menu,300,100,3,600,5,"poly count sides")
size = scale(group_box_menu,300,100,10,600,10,"size")

check_button_var = tk.BooleanVar()
def check_box_random_size():
    config.random_size = not config.random_size
rand_size = tk.Checkbutton(group_box_menu, text="random size", variable=check_button_var,onvalue=True, offvalue=False, command=check_box_random_size,bg="white")
rand_size.pack(fill=tk.BOTH,side=tk.LEFT)










# Create a canvas
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

canvas.create_polygon([(0, 0), (window_width, 0), (window_width, window_height), (0, window_height)],
                      fill="white")

center = (window_width / 2, window_height / 2)

circles = []



class circle:
    def __init__(self, x=center[0], y=center[1]):
        config.racalc()
        self.points = [(x, y)]
        self._points = []
        self.position = (x, y)
        self.circle_radius = random.randint(30,250) if config.random_size else config.fixed_size

        self._points.append((self.circle_radius, 0))
        self.side = config.polygonSides
        self.angel = 360 / self.side
        self.radian = (self.angel / 180) * pi
        self.color = choice(
            [
                "red", "orange", "yellow", "green", "blue", "indigo", "violet",
                "black", "white", "gray", "wheat", "beige", "brown", "pink",
                "purple", "cyan", "magenta", "lime", "olive", "navy",
                "maroon", "teal", "silver", "gold", "coral", "tomato",
                "chocolate", "plum", "azure", "orchid", "salmon"
            ]
        )
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
    @staticmethod
    def brushy(event):
      c=15
      z = 60
      u = 1/pow(2,1/c)

      for circle in circles:
          for index in range(0, len(circle.points)):
            minus = abs(circle.points[index][0] - event.x)
            right = pow(u,minus) * z
            result = right + circle.points[index][1]
            circle.points[index] = (circle.points[index][0], result)

      for circle in circles:
          circle.draw()
    @staticmethod
    def brushx(event):
      c=15
      z = 60
      u = 1/pow(2,1/c)

      for circle in circles:
          for index in range(0, len(circle.points)):
            minus = abs(circle.points[index][1] - event.y)
            right = pow(u,minus) * z
            result = right + circle.points[index][0]
            circle.points[index] = ( result,circle.points[index][1])

      for circle in circles:
          circle.draw()


canvas.bind("<Button-1>", manage_window.draw_circle)


root.bind("<s>", manage_window.brushy)
root.bind("<w>", manage_window.brushx)


root.mainloop()
