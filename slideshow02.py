# -*- coding: utf-8 -*-
import os
from moviepy.editor import *
from moviepy.editor import TextClip,VideoFileClip, concatenate_videoclips

dir_name = "" 
dir_output = ""
fnamemp4 = "File.mp4"
text_site = "https://github.com/igoradmtg" # Текст для интро и аутро
#fontsize_intro = 80 # Размер шрифта для интро и аутро
#video_width = 1920 # clip width 1920
#video_height = 1080 # clip height 1080 
fontsize_intro = 50 # Размер шрифта для интро и аутро
Video_type = 5 # Разрешение для видео 1 - 720х480, 2 - 854x480, 3 - 1280x720, 4 - 1920x1080,  5 - 3840x2160
video_width = 720 # Default clip width 1280
video_height = 480 # Default clip height 720 
save_only_image = True # Сохранять только слайдшоу
time_for_image = 8 # Количество секунд на одну картинку
    
DW = 1 # 1 - Up  2 - Down
DH = 1 # 1 - Left 2 - Right
K_W_H = video_width / video_height # Коэффициент ширина и высота 1920 / 1080 = 1,77777
SIZE = (video_width, video_height) # Размер видео
CHANGE_DIRECTION = True # Менять направление 

def set_video_size() :
    global video_width,video_height,Video_type,SIZE,K_W_H
    if Video_type == 1:
        video_width = 720 # clip width 1280
        video_height = 480 # clip height 720 
    elif Video_type == 2:    
        video_width = 854 # clip width 1280
        video_height = 480 # clip height 720 
    elif Video_type == 3:    
        video_width = 1280 # clip width 1280
        video_height = 720 # clip height 720 
    elif Video_type == 4:    
        video_width = 1920 # clip width 1280
        video_height = 1080 # clip height 720 
    elif Video_type == 5:    
        video_width = 3840 # clip width 3840
        video_height = 2160 # clip height 2160 
    K_W_H = video_width / video_height # Коэффициент ширина и высота 1920 / 1080 = 1,77777
    SIZE = (video_width, video_height) # Размер видео
    print("Video_type ",Video_type)
    print("Video size ",video_width,video_height)
    

def intro() :
    global text_site, SIZE, fontsize_intro
    duration_intro = 2 # Длительность каждого текстового клипа
    logo1 = (TextClip(txt=text_site,color="#0000AA", align='West',fontsize=fontsize_intro,font = 'Arial').set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    logo1_clip = CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])  
    logo2 = (TextClip(txt="present",color="#0000AA", align='West',fontsize=fontsize_intro,font = 'Arial').set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    logo2_clip = CompositeVideoClip([logo2.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])  
    return concatenate_videoclips([logo1_clip,logo2_clip])
  
def outro() :
    global text_site, SIZE, fontsize_intro
    duration_intro = 4 # Длительность каждого текстового клипа
    logo1 = (TextClip(txt=text_site,color="#0000AA", align='West',fontsize=fontsize_intro,font = 'Arial').set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    return CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])
  
def slide_clip(fname, not_direction = False) :
    global DW, DH, SIZE, video_width, video_height, K_W_H, CHANGE_DIRECTION, time_for_image
    def calc_up(t, duration, h1):
        if t<2 :
          val = 0
        elif t>time_for_image - 2 :
          val = video_height-h1
        else :
          val = (video_height-h1)*((t-2)/duration)
        return ('center', val)
    def calc_dwn(t, duration, h1):
        if t<2 :
          val = video_height-h1
        elif t>time_for_image - 2 :
          val = 0
        else :
          val = (video_height-h1)*(1-((t-2)/duration))
        return ('center', val)
    def calc_left(t, duration, w1):
        if t<2 :
          val = 0
        elif t>time_for_image - 2 :
          val = video_width-w1
        else :
          val = (video_width-w1)*((t-2)/duration)
        return (val,'center')
    def calc_right(t, duration, w1):
        if t<2 :
          val = video_width-w1
        elif t>time_for_image - 4 :
          val = 0
        else :
          val = (video_width-w1)*(1-(t-2)/duration)
        return (val,'center')
    clip = ImageClip(fname).set_duration(time_for_image)
    clip_w = clip.w # Ширина клипа (Например 4608)
    clip_h = clip.h # Высота клипа (Например 3072)
    clip_k = clip_w / clip_h # Коэффициент ширины и высоты клипа (Например 4608 / 3072 = 1,5)
    # print("clip_w =", clip_w,"clip_h =", clip_h,"clip_k =", clip_k) 
    if clip_k < K_W_H : 
        clip = clip.resize(width=video_width)
        clip_w = clip.w # Ширина клипа (Например 4608)
        clip_h = clip.h # Высота клипа (Например 3072)
        #print("clip_resize width", clip_w) 
        if not_direction:
            return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos("center","center")],size=SIZE)
        else:  
            if CHANGE_DIRECTION == True :
                if DW==1 :
                    DW=2
                    return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos(lambda t: calc_dwn(t,time_for_image - 4,clip_h))],size=SIZE)
                else :
                    DW=1
                    return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos(lambda t: calc_up(t,time_for_image - 4,clip_h))],size=SIZE)
            else:
                return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos(lambda t: calc_up(t,time_for_image - 4,clip_h))],size=SIZE)
      
    else :
        clip = clip.resize(height=video_height)
        clip_w = clip.w # Ширина клипа (Например 4608)
        clip_h = clip.h # Высота клипа (Например 3072)
        #print("clip_resize height", clip_h) 
        if not_direction:
            return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos("center","center")],size=SIZE)
        else:    
            if CHANGE_DIRECTION == True :
                if DH==1 :
                    DH=2
                    return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos(lambda t: calc_right(t,time_for_image - 4,clip_w))],size=SIZE)
                else :
                    DH=1
                    return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos(lambda t: calc_left(t,time_for_image - 4,clip_w))],size=SIZE)
            else :
                return CompositeVideoClip([clip.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255]).set_pos(lambda t: calc_left(t,time_for_image - 4,clip_w))],size=SIZE)
    

def save_clip() :
    global dir_name, fnamemp4 , SIZE , dir_output
    clip_list = []
    names = os.listdir(dir_name)
    # Сортируем 
    names.sort()
    for name in names:
        #print("File ",name)
        if name.lower().find(".jpg") == -1 :
            print("Пропуск файла ",name) # Пропуск файла
            continue
        fullname = os.path.join(dir_name, name) # получаем полное имя
        if not os.path.isfile(fullname) :
            print("Не найден файл ",fullname)
            continue
        print(fullname)
        clip_list.append(slide_clip(fullname,True))
    # Объеденение всех клипов в один
    final_clip_f = concatenate_videoclips(clip_list)
    # Делаем клип текстовый логотип верхний правый угол и длительностью final_clip_f.duration
    logo = (TextClip(txt=text_site, color='white', align='West',fontsize=16,font = 'Arial-Bold').set_duration(final_clip_f.duration).margin(right=8, top=8, opacity=0).set_pos(("right","top")))
    # Создаем клип с наложенным логотипом
    final_clip_f2 = CompositeVideoClip([final_clip_f,logo], size=SIZE)         
    #final_clip_f3 = concatenate_videoclips([intro(),final_clip_f2])         
    # Добавляем интро и аутро
    final_clip_f3 = concatenate_videoclips([intro(),final_clip_f2,outro()])
    # Сохранение клипа в файл
    if save_only_image:
        final_clip_f.write_videofile(os.path.join(dir_output, fnamemp4), fps=30, threads=4, audio = False)
    else:    
        final_clip_f3.write_videofile(os.path.join(dir_output, fnamemp4), fps=30, threads=4, audio = False)

def main() : 
    global dir_name, fnamemp4, dir_output, Video_type , video_width, video_height
    dir_name = sys.argv[1]
    fnamemp4 = sys.argv[2]
    dir_output = sys.argv[3]
    Video_type = int(sys.argv[4])
    if len(sys.argv)>6: # Если получены дополнительные параметры тогда установка размера видео
        video_width = int(sys.argv[5]) # Новая ширина видео
        video_height = int(sys.argv[6]) # Новая высота видео
    set_video_size() # Установка размера видео
    save_clip()
  
if __name__ == "__main__":
    main()  
  