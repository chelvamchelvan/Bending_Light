"""
This is Bending Light simulation, written in python 3.3
here used python PIL library for image processing
It created based on snell's law
to install PIL [pip install Pillow]
"""

import tkinter
import math
from PIL import ImageTk, Image


class BendingLight:
    def __init__(self, root):
        self.root = root
        self.canvasCreate()
        self.initThings()
        self.laserObject()
        self.laserScaler()
        self.matrialChangeScaler()

    def canvasCreate(self):
        global c
        c = tkinter.Canvas(self.root, height=700, width=1200)
        c.place(relx=.5, rely=.5, anchor="center")

    def laserObject(self):
        global light_image
        c.create_line(550, 150, 550, 550, dash=(7, 1, 1, 1), width=3)
        light_image = tkinter.PhotoImage(file="laser_light.gif")
        self.root.light_image = light_image
        self.light = c.create_image(self.x, self.y, image=light_image)
        self.image = Image.open("laser_light.gif")
        self.image = self.image.convert('RGBA')

    def initThings(self):
        self.x = 300
        self.y = 350
        self.x1 = 1600
        self.y1 = 350
        self.n = 0.0
        self.angle = 90.0
        self.value_of_reft1 = 1.0
        self.value_of_reft2 = 1.0
        self.n2 = (self.value_of_reft1 * math.sin(math.radians(self.angle))) / self.value_of_reft2
        self.n2 = 90 - math.degrees(math.asin(self.n2))

        self.matrialbox1 = c.create_rectangle(5, 5, 1200, 350, width=2, fill="#c8fffc")
        self.matrialbox2 = c.create_rectangle(5, 350, 1200, 700, width=2, fill="#c8fffc")
        self.r1 = c.create_line(self.x, self.y, 550, 350, fill="red", width=2)
        self.r2 = c.create_line(550, 350, self.x1, self.y1, fill="red", width=3)

        self.angle_of_incidence_text = c.create_text(150, 450, font=("Times New Roman", 18),text="Angle of incidence: ")
        self.angle_of_incidence = c.create_text(275, 450, font=("Times New Roman", 18), text=round((self.angle), 2))
        self.angle_of_refraction_text = c.create_text(150, 500, font=("Times New Roman", 18),text="Angle of refraction: ")
        self.angle_of_refraction = c.create_text(275, 500, font=("Times New Roman", 18), text=round((90 - self.n2), 2))
        self.angle_of_reflection_text = c.create_text(150, 550, font=("Times New Roman", 18),text="Angle of reflection: ")
        self.angle_of_reflection = c.create_text(275, 550, font=("Times New Roman", 18), text="")


    def laserScaler(self):
        c.create_line(114, 100, 114, 350, width=2, fill="blue")
        self.scale = c.create_rectangle(100, 338, 125, 362, fill="yellow")
        c.tag_bind(self.scale, "<1>", self.mouseDown)
        c.tag_bind(self.scale, "<B1-Motion>", self.mouseMoveLaser)

    def mouseDown(self, event):
        self.lastx = event.x
        self.lasty = event.y

    def mouseMoveLaser(self, event):
        if (event.y >= 100 and event.y <= 350):
            c.move(self.scale, 0, event.y - self.lasty)
            self.n = round((350 - event.y) * (90 / 250), 2)
            self.angle = 90-self.n
            self.y = round(350 - (250 * math.sin(math.radians(self.n))), 2)
            self.x = round(550 - (250 * math.cos(math.radians(self.n))), 2)
            self.rayCreatation()
            c.delete(self.light)
            self.tkimage = ImageTk.PhotoImage(self.image.rotate(-self.n, expand=1))
            self.light = c.create_image(self.x, self.y, image=self.tkimage)
            self.lastx = event.x
            self.lasty = event.y

    def matrialChangeScaler(self):
        c.create_line(900, 314, 1100, 314, fill="blue", width=2)
        c.create_line(900, 414, 1100, 414, fill="blue", width=2)
        self.scale_matrial1 = c.create_rectangle(900, 300, 925, 325, fill="red")
        self.scale_matrial2 = c.create_rectangle(900, 400, 925, 425, fill="red")
        c.create_text(900, 280, text="Air")
        c.create_text(1020, 280, text="Water")
        c.create_text(1100, 280, text="Glass")

        c.create_text(900, 380, text="Air")
        c.create_text(1020, 380, text="Water")
        c.create_text(1100, 380, text="Glass")

        c.tag_bind(self.scale_matrial1, "<1>", self.mouseDown)
        c.tag_bind(self.scale_matrial1, "<B1-Motion>", self.mouseMoveMatrialScaler1)
        c.tag_bind(self.scale_matrial2, "<1>", self.mouseDown)
        c.tag_bind(self.scale_matrial2, "<B1-Motion>", self.mouseMoveMatrialScaler2)

        self.refraction_text1 = c.create_text(950, 250, font=("Times New Roman", 18),text="Refreaction " + str(self.value_of_reft1))
        self.refraction_text2 = c.create_text(950, 455, font=("Times New Roman", 18),text="Refreaction " + str(self.value_of_reft2))

    def mouseMoveMatrialScaler1(self, event):
        if (event.x > 900 and event.x < 1100):
            c.move(self.scale_matrial1, event.x - self.lastx, 0)
            self.lastx = event.x
            self.lasty = event.y
            c.delete(self.refraction_text1)
            s = 200-(1100-event.x)
            self.value_of_reft1 = round(1.0+((s/200)*0.53),2)
            self.refraction_text1 = c.create_text(950, 250, font=("Times New Roman", 18), text="Refreaction " + str(self.value_of_reft1))

            self.rayCreatation()
            c.delete(self.light)
            self.tkimage = ImageTk.PhotoImage(self.image.rotate(-self.n, expand=1))
            self.light = c.create_image(self.x, self.y, image=self.tkimage)

            th = 200-int(self.value_of_reft1*100-100)
            tv = 255-int(self.value_of_reft1*100-100)
            tb = 252-int(self.value_of_reft1*100-100)
            colorval = "#%02x%02x%02x" % (th, tv, tb)
            c.itemconfigure(self.matrialbox1, fill=colorval)

    def mouseMoveMatrialScaler2(self, event):
        if (event.x > 900 and event.x < 1100):
            c.move(self.scale_matrial2, event.x - self.lastx, 0)
            self.lastx = event.x
            self.lasty = event.y
            c.delete(self.refraction_text2)
            s = 200 - (1100 - event.x)
            self.value_of_reft2 = round(1.0 + ((s / 200) * 0.53), 2)
            self.refraction_text2 = c.create_text(950, 455, font=("Times New Roman", 18),text="Refreaction " + str(self.value_of_reft2))

            self.rayCreatation()
            c.delete(self.light)
            self.tkimage = ImageTk.PhotoImage(self.image.rotate(-self.n, expand=1))
            self.light = c.create_image(self.x, self.y, image=self.tkimage)

            th = 200 - int(self.value_of_reft2 * 100 - 100)
            tv = 255 - int(self.value_of_reft2 * 100 - 100)
            tb = 252 - int(self.value_of_reft2 * 100 - 100)
            colorval = "#%02x%02x%02x" % (th, tv, tb)
            c.itemconfigure(self.matrialbox2, fill=colorval)

    def rayCreatation(self):
        c.delete(self.r1)
        c.delete(self.angle_of_incidence)
        self.r1 = c.create_line(self.x, self.y, 550, 350, fill="red", width=3)
        self.angle_of_incidence = c.create_text(275, 450, font=("Times New Roman", 18), text=str(round(self.angle, 2)))
        self.n2 = (self.value_of_reft1 * math.sin(math.radians(self.angle))) / self.value_of_reft2

        try:
            c.delete(self.r2)
            self.n2 = 90 - math.degrees(math.asin(self.n2))
            self.y1 = round(350 + (800 * math.sin(math.radians(self.n2))), 2)
            self.x1 = round(550 + (800 * math.cos(math.radians(self.n2))), 2)
            self.r2 = c.create_line(550, 350, self.x1, self.y1, fill="red", width=3)
            c.delete(self.angle_of_refraction)
            self.angle_of_refraction = c.create_text(275, 500, font=("Times New Roman", 18),text=str(round(90 - self.n2, 2)))
            c.delete(self.angle_of_reflection)

        except ValueError:
            c.delete(self.angle_of_reflection)
            self.y1 = round(350 - (800 * math.sin(math.radians(90 - self.angle))), 2)
            self.x1 = round(550 + (800 * math.cos(math.radians(90 - self.angle))), 2)
            self.r2 = c.create_line(550, 350, self.x1, self.y1, fill="red", width=3)
            self.angle_of_reflection = c.create_text(275, 550, font=("Times New Roman", 18),text=round((self.angle), 2))
            c.delete(self.angle_of_refraction)


if __name__ == '__main__':
    root = tkinter.Tk()
    w = 1205
    h = 705
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    BendingLight(root)
    root.title("Bending Light")
    root.mainloop()