import os
from PIL import Image
import shutil
from moviepy.editor import *
from moviepy.editor import TextClip,VideoFileClip, concatenate_videoclips
dir_name_main = "y:\\slideshow\\" # The directory contains other directories - Каталог содержит другие каталоги
dir_name_temp = "y:\\slideshow_tmp" #
dir_name_output = "y:\\slideshow_out2" # Directory for saving files mp4 - Каталог для сохранения файлов mp4
python_scrypt = "slideshow02.py" # Script to start generating the mp4 file - Скрипт для запуска формирования файла mp4
Video_type = 0 #  0 - Не определено, 1 - 720х480, 2 - 854x480, 3 - 1280x720, 4 - 1920x1080,  5 - 3840x2160 - Разрешение для видео
size_multiple = 0.25 # Уменьшение размера видео на этот коэффициент
if os.path.isdir(dir_name_temp):
    shutil.rmtree(dir_name_temp)    
if not os.path.isdir(dir_name_temp):
    os.makedirs(dir_name_temp)
if not os.path.isdir(dir_name_output):
    os.makedirs(dir_name_output)

def save_file_busy(fname):
    f = open(fname,"a")
    f.write("busy")
    f.close()

def main() : 
    global dir_name_main,dir_name_output,python_scrypt
    # Создать каталог если он не существует
    if os.path.isdir(dir_name_output) == False:
        os.mkdir(dir_name_output)
    dir_names = os.listdir(dir_name_main) # We read the contents of the directory - Читаем содержимое каталога
    is_found_dir = False # Found directory attribute - Признак найденного каталога 
    fname_start_mp4 = ""
    dir_fullname = ""
    fname_busy = ""
    for dir_name in dir_names:
        dir_fullname = os.path.join(dir_name_main, dir_name) # We get the full name - Получаем полное имя
        fname_start_mp4 = dir_name # Mp4 file name - Название файла mp4
        print(f"Directory: {dir_name}") # Display the current directory - Выводим текущий каталог  
        print(f"Fullname: {dir_fullname}") # Displaying the full directory name - Выводим полное имя каталога
        print(f"File start mp4: {fname_start_mp4}") # Displaying the name of the mp4 file - Выводим название файла mp4
        if not os.path.isdir(dir_fullname) :
            print("Directory not found ",dir_fullname) # Не найден каталог
            continue
        fname_busy = os.path.join(dir_fullname, "busy.txt") # Flag filename taken - Имя файла с флагом занято  
        if os.path.isfile(fname_busy) :  
            print("Found file ",fname_busy) # Найден файл
            #continue
        is_found_dir = True
        break

    if is_found_dir :
        dir_files = os.listdir(dir_fullname)
        print("Found dir " + dir_fullname)
        list_files = [] # Список файлов для сохранения
        list_dirs = [] # Список информации каталогов для обработки файлов
        for file_name in dir_files:
            full_name = os.path.join(dir_fullname,file_name)
            print(f"File: {full_name}")
            if not os.path.isfile(full_name):  
                continue
            try:
                with Image.open(full_name) as img:
                    width, height = img.size
            except Exception as e:
                continue
            dir_name_size_temp = os.path.join(dir_name_temp,str(width) + "_" + str(height))
            if not os.path.isdir(dir_name_size_temp):
                list_dirs.append({"path":dir_name_size_temp,"width":int(width * size_multiple),"height":int(height * size_multiple)})
                os.makedirs(dir_name_size_temp)
            new_name = os.path.join(dir_name_size_temp,file_name)
            print(f"New name: {new_name}")
            shutil.copyfile(full_name,new_name)


        for dir_info in list_dirs:
            dir_path = dir_info["path"]
            width = dir_info["width"]
            height = dir_info["height"]
            print(f"Dir: {dir_path} Size: {width} x {height}")
            fname_mp4 = fname_start_mp4 + "_" + str(width) + "_" + str(height) + ".mp4"
            str_exec = f"{python_scrypt} \"{dir_path}\" \"{fname_mp4}\" \"{dir_name_output}\" {Video_type} {width} {height}" # form a string for execution - формируем строку для выполнения
            print("Execute ",str_exec) # Displaying - Выводим на экран
            os.system(str_exec) # Run the script for execution - Запускаем скрипт на выполнение
        
  
if __name__ == "__main__":
    main()    