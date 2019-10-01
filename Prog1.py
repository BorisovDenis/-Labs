from graph import *
from tkinter import Canvas
canvasSize(1000, 800)
windowSize(1000, 800)
w = 1000; h = 800
def main():
    brushColor(100, 100, 255)
    rectangle(0, 0, w, h)
    brushColor(0, 100, 0)
    rectangle(0, (h-1)/2, w, h)
    atlete(0)
    wooman(0)
    atlete(500)
    wooman(500)
    for i in range(5):
        cloud(100 + randint(1, 100) * 20, 100)
def atlete(x): #x is position by w
    #body
    brushColor(100, 100, 100)
    polygon([(100 + x, 280), (250 + x, 280), (175 + x, 500)])
    brushColor(255, 255, 180)
    circle(175 + x, 255, 26)
    #man's hands
    line(110 + x, 290, 80 + x, 400)
    line(240 + x, 290, 295 + x, 400)
    #man's legs
    line(175 + x, 500, 145 + x, 590)
    line(115 + x, 590, 145 + x, 590)
    line(175 + x, 500, 205 + x, 590)
    line(205 + x, 590, 235 + x, 590)
    #ice cream
    brushColor(100, 100, 0)
    polygon([(80 + x, 400), (30 + x, 370), (60 + x, 350)])
    brushColor(255 + x, 255 + x, 180)
    brushColor(240, 240, 200)
    circle(45 + x, 360, 20)
def wooman(x):
    # body
    brushColor(200, 100, 200)
    polygon([(300 + x, 480), (400 + x, 480), (350 + x, 290)])
    brushColor(255, 255, 180)
    circle(350 + x, 270, 25)
    # wooman's hands
    line(295 + x, 400, 350 + x, 300)
    line(400 + x, 400, 352 + x, 300)
    # wooman's legs
    line(330 + x, 480, 330 + x, 550)
    line(315 + x, 550, 330 + x, 550)
    line(370 + x, 480, 370 + x, 550)
    line(385 + x, 590, 370 + x, 550)
    #baloon
    line(400 + x, 400, 430 + x, 290)
    penColor(200, 0, 0)
    brushColor(200, 0, 0)
    circle(430 + x, 233, 15)
    circle(448 + x, 240, 15)
    polygon([(429 + x, 290), (415 + x, 230), (463 + x, 240)])
    circle(45 + x, 360, 20)
def cloud(x, y):
    brushColor(200, 200, 200)
    penColor(200, 200, 200)
    for i in range(2):
        for j in range(3):
            circle(x + i * 5 * randint(1, 6), y + j * 5, 20)
main()
run()
input()






