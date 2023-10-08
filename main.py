from tkinter import * # графический интерфейс
from PIL import Image, ImageTk # для изображений
import random # для спавна еды

# так как при нажатии Заново я просто заново вызываю функцию, то старое окно
# никуда не пропадает и чтобы это исправить при первом открытии будет окно которое
# сразу откроется и после чего уже откроется нормальное, а при нажатии заново
# так как это окно вне функции оно не будет открываться что приведет к правильной работе
window = Tk()

# функция всей игры
def start():
    global in_game, space_size, speed, vector, window
    window.destroy()
    # функция проверяющая столкновения либо с стенками либо с самим собой
    def check_collision():
        global snakecoord
        # берем координаты головы
        x, y = snakecoord[0]
        # проверка на стенки
        if x < 0 or x > 500:
            return True
        if y < 0 or y > 400:
            return True
        # проверка на себя же
        for snakelength in snakecoord[1::]:
            if x == snakelength[0] and y == snakelength[1]:
                return True

    # функция смены вектора движения
    def change_vector(new_vector):
        global vector
        # тут везде по 2 условия так как нельзя идя вверх пойти вниз
        if new_vector == "up":
            if vector != "down":
                vector = new_vector
        elif new_vector == "down":
            if vector != "up":
                vector = new_vector
        elif new_vector == "right":
            if vector != "left":
                vector = new_vector
        elif new_vector == "left":
            if vector != "right":
                vector = new_vector

    def move(SSnake, FFood):
        global window, snakecoord, snakebody, Food, Snake, speed, Move, vector, foodcoord, gameplace, eatcount, counter
        # создание тела которое в свою очередь будет дальше закрыто цветом поля,
        # но это нужно для увеличения змейки при сьедении еды
        for x, y in snakecoord:
            square = Canvas.create_rectangle(gameplace, x, y, x+space_size, y+space_size, fill="#9412b5")
        # берем координаты головы
        x, y = snakecoord[0]
        # векторы движения
        if vector == "right":
            x += space_size
        if vector == "left":
            x -= space_size
        if vector == "up":
            y -= space_size
        if vector == "down":
            y += space_size
        # вставляем в первую ячейку наши координаты
        snakecoord.insert(0, (x, y))
        # создаем голову
        snakehead = Canvas.create_rectangle(gameplace, x, y, x+space_size, y+space_size, fill="#c223eb")
        # так как это голова, то вставляем в начало массива тела змейки
        snakebody.insert(0, snakehead)
        # проверка сьедает ли змейка еду
        if x == foodcoord[0] and y == foodcoord[1]:
            Canvas.delete(gameplace, Food)
            Food = food()
            eatcount += 1
            counter.config(text=f"Счет: {eatcount}")
        else:
            # если еда не сьедена, то мы как раз закрываем всю заднюю часть тела которую создавал там цикл
            x, y = snakecoord[-1]
            square = Canvas.create_rectangle(gameplace, x, y, x+space_size, y+space_size, fill="#26ad2f", outline="#26ad2f")
           # убираем хвост
            del snakecoord[-1]
            Canvas.delete(gameplace, snakebody[-1])
            del snakebody[-1]
        # проверка на столкновения
        if eatcount == 2000:
            gameoverplace = Canvas(window, width=250, height=100, bg="#1b7521", highlightcolor="#1b7521")
            gameoverplace.place(x=175, y=200)
            gameovermessage = Label(window, text=f"Вы победили!", bg="#1b7521", fg="white", font=("Courier", 10))
            gameovermessage.place(x=195, y=215)
            gameoverbutton = Button(window, text="Заново?", command=start, font=("Courier", 12), bg="#26ad2f", fg="white")
            gameoverbutton.place(x=260, y=250)
        elif (check_collision()):
            # если столкновение есть, то выводим сообщение конец игры с выводом очков
            gameoverplace = Canvas(window, width=250, height=100, bg="#1b7521", highlightcolor="#1b7521")
            gameoverplace.place(x=175, y=200)
            gameovermessage = Label(window, text=f"Игра окончена! ваш счет: {eatcount}", bg="#1b7521", fg="white", font=("Courier", 10))
            gameovermessage.place(x=195, y=215)
            gameoverbutton = Button(window, text="Заново?", command=start, font=("Courier", 12), bg="#26ad2f", fg="white")
            gameoverbutton.place(x=260, y=250)
        else:
            # запускаем/продолжаем отрисовку движения змейки
            window.after(speed, move, SSnake, FFood)




    def snake():
        global gameplace, space_size, snakecoord, snakebody
        # размер змейки
        snake_length = 3
        # матрица для координат начальной змейки
        snakecoord = [[0, 0]] * 3
        # тело змейки где будут все части тела
        snakebody = []
        # создание тела змейки(точнее первых трех включая голову частей)
        for x, y in snakecoord:
            square = Canvas.create_rectangle(gameplace, x, y, x+space_size, y+space_size, fill="#9412b5")
            snakebody.append(square)

    # функция отвечающая за спавн еды для змейки
    def food():
        global space_size, gameplace, foodcoord, snakecoord
        z = random.randint(0, int(500/space_size)-1)*space_size # координата x
        y = random.randint(0, int(400/space_size)-1)*space_size # координата y
        foodcoord = [z, y] # координаты еды
        Canvas.create_rectangle(gameplace, z, y, z+space_size, y+space_size, fill="red") # создание еды


    #сама игра
    def game():
        global in_game, gameplace, Food, Snake, Move, eatcount, counter
        if in_game:
            # удаление всех элементов меню для игры
            [i.destroy() for i in [panel, gamename, gamestart]]
            # создание поля для змейки
            gameplace = Canvas(window, width=500, height=400, bg="#26ad2f", highlightcolor="#1b7521")
            gameplace.place(x=45, y=60)
            # счет
            eatcount = 0
            counter = Label(window, text=f"Счет: {eatcount}", bg="#1b7521", fg="white", font=("Courier", 16))
            counter.place(x=50, y=20)
            # создание еды
            Food = food()
            # создание змейки
            Snake = snake()
            # движение
            Move = move(Snake, Food)
    # главное меню
    window = Tk()
    window.title("Змейка")
    window.geometry("600x500+350+150")
    window.iconbitmap("icon.ico")
    window.resizable(width=False, height=False)
    Frame(window, bg="#1b7521", width=600, height=500).place(x=0, y=0)

    # визуал меню
    # иконка
    icon = "icon.png"
    img = Image.open(icon)
    width = 75
    ratio = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(ratio)))
    imag = img.resize((width, height))
    image = ImageTk.PhotoImage(imag)
    panel = Label(window, image=image, bg="#1b7521")
    panel.place(x=260, y=75)
    # надпись
    gamename = Label(window, text="Змейка", bg="#1b7521", fg="white",  font=("Courier", 32))
    gamename.place(x=220, y=150)
    # кнопка играть
    gamestart = Button(window, text="Играть", command=game, font=("Courier", 18), bg="#26ad2f", fg="white")
    gamestart.place(x=247, y=210)

    # переменные
    # переменная для определения играет игрок или нет
    in_game = True
    # размер клетки
    space_size = 10
    # скорость змейки
    speed = 100
    # начальное направление
    vector = "right"
    # бинды для передвижения
    window.bind('<Down>', lambda event: change_vector("down"))
    window.bind('<Up>', lambda event: change_vector("up"))
    window.bind('<Right>', lambda event: change_vector("right"))
    window.bind('<Left>', lambda event: change_vector("left"))
    # открытие окна
    window.mainloop()

# запуск
if __name__ == "__main__":
    start()
