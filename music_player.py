import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame

root = Tk()
root.title('Music Player')
root.resizable(False, False)
root.configure(bg='orange')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Загрузка изображений
last_img = ImageTk.PhotoImage(Image.open('assets/last.png'))
pause_img = ImageTk.PhotoImage(Image.open('assets/pause.png'))
continue_img = ImageTk.PhotoImage(Image.open('assets/continue.png'))
next_img = ImageTk.PhotoImage(Image.open('assets/next.png'))
list_img = ImageTk.PhotoImage(Image.open('assets/list.png'))
add_img = ImageTk.PhotoImage(Image.open('assets/add.png'))
circle_img = ImageTk.PhotoImage(Image.open('assets/circle.png'))
close_img = ImageTk.PhotoImage(Image.open('assets/close.png'))
volume_no_img = ImageTk.PhotoImage(Image.open('assets/volume_no.png'))
volume_low_img = ImageTk.PhotoImage(Image.open('assets/volume_low.png'))
volume_medium_img = ImageTk.PhotoImage(Image.open('assets/volume_medium.png'))
volume_high_img = ImageTk.PhotoImage(Image.open('assets/volume_high.png'))
increase_img = ImageTk.PhotoImage(Image.open('assets/increase.png'))
decrease_img = ImageTk.PhotoImage(Image.open('assets/decrease.png'))

# Начальные значения
first = True # Индикатор того, что песня проигрывается впервые
closed = False # Текущее состояние меню
stopped = True # Индикатор того, что музыка поставлена на паузу
current_volume = 50 # Первоначальный уровень громкости

def music_menu_func():
    """
    Переключает отображение музыкального меню в графическом интерфейсе,
    изменяя размер окна и иконку на кнопке в зависимости от текущего состояния меню 
    (открыто или закрыто).
    """
    global closed
    if closed:
        root.geometry("350x300")
        closed = False
        list_btn['image'] = close_img
    else:
        root.geometry("600x300")
        closed = True
        list_btn['image'] = list_img

music = []
music_name = []

# Загрузка списка воспроизведения
for i in open('playlist.txt', 'r').read().replace('[','').replace(']', '').split(', '):
    if os.path.isfile(i.replace("'", '')):
        music.append(i.replace("'", ''))
    else:
        print(i.replace("'", ''))

# Обновление списка воспроизведения
open('playlist.txt', 'r+').truncate()
open('playlist.txt', 'w').write(str(music))

pygame.mixer.init()

if music:
    music_now = music[0]
else:
    music_now = ''

if music_now != '':
    music_length = pygame.mixer.Sound(music_now).get_length() * 1000

music_pos = 0

# Формирование списка названий музыки
for i in music:
    music_name.append(i.split('/')[-1])

# Функции управления музыкой
def continue_stop_func():
    """
    Функция приостанавливает или возобновляет воспроизведение музыки.
    В зависимости от текущего состояния воспроизведения (пауза или воспроизведение),
    функция либо приостанавливает, либо продолжает воспроизведение музыки, обновляя
    изображение кнопки паузы/воспроизведения.
    """
    global stopped
    global first
    if stopped:
        pause_continue_btn['image'] = continue_img
        if music_now != '':
            pygame.mixer.music.pause()
        stopped = False
    else:
        if first:
            if music_now != '':
                pygame.mixer.music.load(music_now)
                pygame.mixer.music.play()
            first = False

        pause_continue_btn['image'] = pause_img
        if music_now != '':
            pygame.mixer.music.unpause()
        stopped = True

def set_music(music_this):
    """
    Функция переключает состояние воспроизведения музыки между паузой и продолжением. 
    Если музыка на паузе, то при нажатии на кнопку, она будет возобновлена. 
    Если музыка воспроизводится, то при нажатии на кнопку, она будет поставлена на паузу.
    Визуально обновляется иконка кнопки паузы/продолжения.
    """
    global return_name
    global music_now
    global music_length
    global music_pos
    global first
    global stopped
    global letter_glob

    music_now = music_this
    music_pos = 0
    pygame.mixer.music.pause()
    music_length = pygame.mixer.Sound(music_now).get_length() * 1000
    return_name = music_now.split('/')[-1][0:25]
    letter_glob = 25
    first = True
    stopped = False
    continue_stop_func()
    pygame.mixer.music.unpause()

def next_func():
    """
    Функция воспроизводит следующую песню в плейлисте.
    Функция ищет текущую песню в плейлисте и, если она не является последней,
    текущая песня ставится на паузу, переключается на следующую песню и начинает её воспроизведение.
    """
    global return_name
    global music_now
    global music_length
    global music_pos
    global first
    global stopped
    global letter_glob

    for i in range(0, len(music)):
        if music[i] == music_now:
            if i + 1 != len(music):
                music_pos = 0
                pygame.mixer.music.pause()
                music_now = music[i + 1]
            music_length = pygame.mixer.Sound(music_now).get_length() * 1000
            return_name = music_now.split('/')[-1][0:25]
            letter_glob = 25
            first = True
            stopped = False
            continue_stop_func()
            pygame.mixer.music.unpause()
            break

def last_func():
    """
    Функция воспроизводит предыдущую песню в плейлисте.
    Функция ищет текущую песню в плейлисте и, если она не является первой,
    ставит на паузу текущую песню, переключается на предыдущую и начинает её воспроизведение.
    """
    global music_now
    global music_length
    global music_pos
    global first
    global stopped
    global return_name
    global letter_glob

    for i in range(0, len(music)):
        if music[i] == music_now:
            if i != 0:
                music_pos = 0
                pygame.mixer.music.pause()
                music_now = music[i - 1]
                music_length = pygame.mixer.Sound(music_now).get_length() * 1000
                return_name = music_now.split('/')[-1][0:25]
                letter_glob = 25
                first = True
                stopped = False
                continue_stop_func()
                pygame.mixer.music.unpause()
                break

def add():
    """
    Функция добавляет песню в плейлист.
    Функция открывает диалоговое окно для выбора музыкального файла 
    (форматы .mp3, .wav, .ogg) и добавляет выбранный файл в список воспроизведения, 
    если он еще не добавлен. После этого обновляется файл плейлиста и отображается название песни.
    """
    global music
    possible_files = [('MUSIC', '*.mp3;*.wav;*oog;*')]
    file = filedialog.askopenfilename(filetypes=possible_files)
    if file != '':
        if file not in music:
            music.append(file)
            open('playlist.txt', 'r+').truncate()
            open('playlist.txt', 'w').write(str(music))
            music_list.insert(END, music[-1].split('/')[-1])
            set_music(music[-1])

def increase_volume():
    """
    Функция увеличивает громкость песни на 10%.
    Функция увеличивает текущую громкость на 10%, если она меньше 100%.
    После изменения громкости обновляется настройка громкости в Pygame и
    отображается соответствующий значок громкости.
    """
    global current_volume
    if current_volume < 100:
        current_volume += 10
        pygame.mixer.music.set_volume(current_volume / 100)
        music_func()

def decrease_volume():
    """
    Функция уменьшает громкость песни на 10%.
    Функция уменьшает текущую громкость на 10%, если она больше 0%.
    После изменения громкости обновляется настройка громкости в Pygame и
    отображается соответствующий значок громкости.
    """
    global current_volume
    if current_volume > 0:
        current_volume -= 10
        pygame.mixer.music.set_volume(current_volume / 100)
        music_func()

# UI Elements and Main Loop (keeping the existing structure)
last_btn = Button()
last_btn.configure(image=last_img, bg='orange', relief=FLAT, activebackground='orange', command=last_func)
last_btn.place(x = 50, y = 25)

pause_continue_btn = Button()
continue_stop_func()
pause_continue_btn.configure(bg='orange', relief=FLAT, activebackground='orange', command=continue_stop_func)
pause_continue_btn.place(x = 125, y = 25)

next_btn = Button()
next_btn.configure(image=next_img, bg='orange', relief=FLAT, activebackground='orange', command=next_func)
next_btn.place(x = 200, y = 25)

list_btn = Button()
list_btn.configure(bg='orange', relief=FLAT, activebackground='orange', command=music_menu_func)
list_btn.place(x = 275, y = 5)

add_btn = Button()
add_btn.configure(image=add_img, bg='orange', relief=FLAT, activebackground='orange', command=add)
add_btn.place(x = 5, y = 5)

volume_label = Label()
volume_label.configure(image=volume_medium_img, relief=FLAT, bg='orange', fg='white')
volume_label.place(x = 125, y = 150)

increase_button = Button()
increase_button.configure(image=increase_img, relief=FLAT, bg='orange', fg='white', command=increase_volume)
increase_button.place(x = 210, y = 150)

decrease_button = Button()
decrease_button.configure(image=decrease_img, relief=FLAT, bg='orange', fg='white', command=decrease_volume)
decrease_button.place(x = 60, y = 150)

def pos():
    """
    Функция обрабатывает позицию песни во время воспроизведения.
    Функция рассчитывает текущую позицию воспроизведения песни на основе положения указателя мыши.
    Затем она обновляет позицию воспроизведения в Pygame и при необходимости ставит музыку на паузу.
    """
    global music_pos
    if not first:
        if music_now != '':
            pos_x = root.winfo_pointerx() - root.winfo_rootx()
            music_pos = ((pos_x - 45) / 200 * music_length)
            pygame.mixer.music.stop()
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(music_pos / 1000)
            if not stopped:
                pygame.mixer.music.pause()

progress_line = Button()
progress_line.configure(bg='white', relief=FLAT, command=pos)
progress_line.place(x = 50, y = 130, width = 200, height = 5)

circle_lbl = Label()
circle_lbl.configure(image=circle_img, bg='orange')

name = Label()
name.configure(bg='orange', foreground='white')
name.place(x=81, y=100)

music_list = Listbox(listvariable=StringVar(value=music_name))
music_list.configure(bg='orange', relief=FLAT, foreground='white', highlightcolor='white', selectmode=EXCEPTION)
music_list.place(x = 350, width = 250, height = 300)

music_menu_func()

def x():
    """
    Функция рассчитывает и обновляет прогресс текущей песни.
    Функция отслеживает текущую позицию воспроизведения песни и обновляет индикатор прогресса.
    Если песня достигла конца, она либо продолжает воспроизведение следующей песни в списке, либо повторяет первый трек.
    """
    global music_length
    if music_now != '':
        if pygame.mixer.music.get_pos() != -1:
            if int((pygame.mixer.music.get_pos() + music_pos) / 1000) >= int(music_length / 1000):
                if music_now != music[-1]:
                    next_func()
                else:
                    set_music(music[0])
            return ((pygame.mixer.music.get_pos() + music_pos) / music_length) * 200 + 40
        else:
            return 45
    else:
        return 45

letter_glob = 25
if music_now != '':
    return_name = music_now.split('/')[-1][0:25]

def text(name_of_music):
    """
    Функция анимирует отображение имени текущей песни.
    Функция поочередно добавляет символы из названия песни в строку, создавая эффект анимации. 
    Когда строка достигает конца, она циклично прокручивается.
    """
    global letter_glob
    global return_name
    for i in range(0, len(name_of_music)):
        if letter_glob == len(name_of_music):
            letter_glob = 0
        if letter_glob == i:
            return_name += name_of_music[i]
            return_name = return_name[1:]
            if i + 1 == len(name_of_music):
                for j in range(0, 5):
                    return_name = return_name[1:]
                    return_name += ''
            if i < len(name_of_music):
                letter_glob = i + 1
            else:
                letter_glob = 0
            return return_name

def upd():
    """
    Функция обновляет элементы графического интерфейса.
    Функция периодически обновляет текст, отображающий название текущей песни, а также обновляет
    положение круга прогресса. Также она проверяет, не был ли выбран новый трек в списке воспроизведения.
    """
    global music_now
    if music_now != '':
        name.configure(text=text(music_now.split('/')[-1]))

    circle_lbl.place(x=x(), y=126)

    if not closed:
        chosen = str(music_list.curselection())[1:][:-2]
        if chosen != '':
            if music_now != music[int(chosen)]:
                set_music(music[int(chosen)])

    root.after(200, upd)

def music_func():
    """
    Функция обновляет изображение индикатора громкости в зависимости от уровня громкости.
    Функция проверяет текущий уровень громкости и обновляет отображаемое изображение
    индикатора громкости в соответствии с этим уровнем. Используются разные изображения 
    для высокого, среднего, низкого уровня громкости и для беззвучного режима.
    """
    if current_volume >= 70:
        volume_label['image'] = volume_high_img
    elif current_volume < 70 and current_volume > 30:
        volume_label['image'] = volume_medium_img
    elif current_volume <= 30 and current_volume > 0:
        volume_label['image'] = volume_low_img
    elif current_volume == 0:
        volume_label['image'] = volume_no_img

music_func()
upd()
if __name__ == '__main__':
    root.mainloop()
