import time
import tkinter as tk
import classes

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=1)
target_number = 8

screen = canvas.create_text(400, 300, text='', font='28')
scoreboard = classes.Scoreboard(canvas)


# функция новой игры
def new_game():
    global scoreboard
    bullets = []
    targets = []
    gun = classes.Gun(canvas, bullets)
    canvas.itemconfig(screen, text='')
    targets_lives = 0
    for i in range(target_number):
        new_target = classes.Target(canvas)
        targets.append(new_target)
        targets_lives += targets[i].live
    canvas.bind('<Button-1>', gun.fire2_start)
    canvas.bind('<ButtonRelease-1>', gun.fire2_end)
    canvas.bind('<Motion>', gun.targeting)

    while targets_lives or bullets:
        to_del = []
        for j in range(target_number):
            targets[j].move()
        for i, b in enumerate(bullets):
            b.move()
            for j in range(target_number):
                if b.hit_test(targets[j]) and targets[j].live:
                    targets_lives -= targets[j].live
                    targets[j].live = 0
                    targets[j].hit()
            if b.live < 0:
                to_del.append(i)
                canvas.delete(b.id)
        for i in range(len(to_del) - 1, -1, -1):
            del bullets[to_del[i]]
        canvas.update()
        time.sleep(0.03)
        gun.targeting()
        gun.power_up()
    scoreboard.update_score(1)
    canvas.bind('<Button-1>', '')
    canvas.bind('<ButtonRelease-1>', '')
    canvas.itemconfig(screen, text='Вы уничтожили цель за ' + str(gun.num_bullets) + ' выстрелов')
    canvas.delete(gun.id)
    root.after(1500, new_game)


new_game()

tk.mainloop()
