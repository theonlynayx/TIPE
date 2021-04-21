from OSINT.GetInsta import main
import threading
from tkinter import *
import tkinter.font as tkFont
from time import sleep
import pyglet
import datetime
import queue
import json
import os    

# Cringe Font
pyglet.font.add_file('assets/HACKED.ttf')

def DisplayDorks(i):
    if i == 4:
        i = 0
    Data_Canvas.delete('all')
    Next_Button = Button(root,text='next',font=('HACKED',10),command=lambda : DisplayDorks(i+1))
    Data_Canvas.create_window(430,20,window=Next_Button)

    KeyList = [
        ('AccountList','Linked Accounts:'),
        ('InstaText','Linked Posts:'),
        ('RespAllText','Linked Websites:'),
        ('RespAllUrl','Linked URLs:')
    ]

    Key = KeyList[i][0]
    if Key in ret['Dorks']:
        dork_coords = {'width' : 20, 'height' : 20}
        size = len(ret['Dorks'][Key])
        if size > 10:
            Max = 10
        else:
            Max = size
        j = 0
        Data_Canvas.create_text(dork_coords['width'],dork_coords['height'],text=KeyList[i][1],font=('HACKED',15),fill='white',anchor='w')
        dork_coords['height'] += 50
        while j < Max:
            if len(ret['Dorks'][Key][j]) > 40:
                string = str(ret['Dorks'][Key][j])[:41] + '...'
            else:
                string = str(ret['Dorks'][Key][j])
            Data_Canvas.create_text(dork_coords['width'],dork_coords['height'],text=string,font=('Helvetica',15),fill='white',anchor='w')
            j += 1
            dork_coords['height'] += 40
    else:
        DisplayDorks(i+1)

def DisplayStats(i):
    if i == 3:
        i = 0
    Data_Canvas.delete('all')
    Next_Button = Button(root,text='next',font=('HACKED',10),command=lambda : DisplayStats(i+1))
    Data_Canvas.create_window(430,20,window=Next_Button)

    KeyList = [
        ('Commenters','Top Commenters:'),
        ('HashTags','Top HashTags:'),
        ('TaggedUsers','Top Tagged Users:')
    ]
    Key = KeyList[i][0]
    if Key in ret['Stats']:
        top_coords = {'width' : 20, 'height' : 20}
        size = len(ret['Stats'][Key])
        if size > 10:
            Max = 10
        else:
            Max = size
        j = 0
        Data_Canvas.create_text(top_coords['width'],top_coords['height'],text=KeyList[i][1],font=('HACKED',15),fill='white',anchor='w')
        top_coords['height'] += 50
        while j < Max:
            Data_Canvas.create_text(top_coords['width'],top_coords['height'],text='{}. '.format(j+1) + str(ret['Stats'][Key][j]),font=('Helvetica',15),fill='white',anchor='w')
            j += 1
            top_coords['height'] += 40
    else:
        DisplayStats(i+1)


def DisplayPost(i):
    Data_Canvas.delete('all')
    Next_Button = Button(root,text='next',font=('HACKED',10),command=lambda : DisplayPost(i+1))
    Data_Canvas.create_window(430,20,window=Next_Button)
    post_coord = {'width' : 20, 'height' : 20}

    try:
        Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='Last Posts:',font=('HACKED',15),fill='white',anchor='w')
        post_coord['height'] += 50
        Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='Likes Number: ' + str(ret['Posts'][i]['LikesNumber']),font=('Helvetica',15),fill='white',anchor='w')
        post_coord['height'] += 40

        if ret['Posts'][i]['CommentsNumber'] != False:
            Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='Comments Number: ' + str(ret['Posts'][i]['CommentsNumber']),font=('Helvetica',15),fill='white',anchor='w')
        else:
            Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='Comments Number: \U0000274c',font=('Helvetica',15),fill='white',anchor='w')
        post_coord['height'] += 40

        Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='Date: {}'.format(datetime.datetime.fromtimestamp(ret['Posts'][i]['timestamp']).strftime('%Y-%m-%d %H:%M:%S')),font=('Helvetica',15),fill='white',anchor='w')
        post_coord['height'] += 40

        if 'Location' in ret['Posts'][i]:
            Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='Location: ' + ret['Posts'][i]['Location'],font=('Helvetica',15),fill='white',anchor='w')
            post_coord['height'] += 40

        if 'Comments' in ret['Posts'][i]:
            Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='\U00002705 Comments Section has been saved',font=('Helvetica',15),fill='white',anchor='w')
            post_coord['height'] += 40

        if 'Pic' in ret['Posts'][i] or 'Vid' in ret['Posts'][i]:
            Data_Canvas.create_text(post_coord['width'],post_coord['height'],text='\U00002705 Post has been saved',font=('Helvetica',15),fill='white',anchor='w')
            post_coord['height'] += 40
    except:
        DisplayPost(0)

    return 0

def Gresult():

    global ret
    ret = que.get()
    global pp
    pp = PhotoImage(file=ret['Profile']['ProfilePic'])

    # coordonnées dans le canvas

    pp_coord = {'width' : 160, 'height' : 160}
    text_coord = {'width' : 330, 'height' : 20}
    message_coord = {'width' : 10, 'height' : 340}
    buttons_coord = {'width' : 285, 'height' : 590}

    User_Canvas = Canvas(root,width=670,height=480,bg="#212121",bd=0, highlightthickness=0)
    User_Canvas.create_image(pp_coord['width'],pp_coord['height'],image=pp)
    User_Canvas.pack(expand=YES,fill='both')

    # Informations générales

    Bg_Canvas.create_window(340,250,window=User_Canvas)
    User_Canvas.create_text(text_coord['width'],text_coord['height'],text='Profile:',font=('HACKED',15),fill='white',anchor='w')
    text_coord['height'] += 50
    if ret['Profile']['Profile Name'] != False:
        Name = ret['Profile']['Profile Name']
    else:
        Name = ret['Profile']['Username']

    for key,val in ret['Profile'].items():
        if key in ('Biography','IsBusiness','ProfilePic','Category','Url','FaceBook Page'):
            continue
        User_Canvas.create_text(text_coord['width'],text_coord['height'],text=key + ': ' + str(val),font=('Helvetica',15),fill='white',anchor='w')
        text_coord['height'] += 35

    # Informations optionnelles

    if ret['Profile']['IsBusiness']:
        User_Canvas.create_text(text_coord['width'],text_coord['height'],text='Category: ' + str(ret['Profile']['Category']),font=('Helvetica',15),fill='white',anchor='w')
        text_coord['height'] += 35
    if 'Url' in ret['Profile']:
        User_Canvas.create_text(text_coord['width'],text_coord['height'],text='URL: ' + str(ret['Profile']['Url']),font=('Helvetica',15),fill='white',anchor='w')
        text_coord['height'] += 35
    if 'FaceBook Page' in ret['Profile']:
        User_Canvas.create_text(text_coord['width'],text_coord['height'],text='FaceBook Page: ' + str(ret['Profile']['FaceBook Page']),font=('Helvetica',15),fill='white',anchor='w')

    # Téléchargement de la bio, de la photo de profil et de la story

    User_Canvas.create_text(message_coord['width'],message_coord['height'],text='\U00002705 Biography has been saved',font=('Helvetica',15),fill='white',anchor='w')
    User_Canvas.create_text(message_coord['width'],message_coord['height'] + 25,text='\U00002705Profile Pic has been saved',font=('Helvetica',15),fill='white',anchor='w')
    if ret['Story'] != 'No_Story_Available' and ret['Story'] != "":
        User_Canvas.create_text(message_coord['width'],message_coord['height'] + 50,text='\U00002705 Story has been saved',font=('Helvetica',15),fill='white',anchor='w')
    else:
        User_Canvas.create_text(message_coord['width'],message_coord['height'] + 50,text='\U0000274c No story available',font=('Helvetica',15),fill='white',anchor='w')

    # Nouveau canvas pour les données

    global Data_Canvas
    Data_Canvas = Canvas(root,width=480,height=480,bg="#212121",bd=0,highlightthickness=0)
    Bg_Canvas.create_window(935,250,window=Data_Canvas)

    # On crée les boutons

    Post_Button = Button(root,text='Posts',font=tkFont.Font(family="HACKED", size=40,weight='normal'),command=lambda: DisplayPost(0))
    Stat_Button = Button(root,text='Stats',font=tkFont.Font(family="HACKED", size=40,weight='normal'),command=lambda: DisplayStats(0))
    Dork_Button = Button(root,text='Dorks',font=tkFont.Font(family="HACKED", size=40,weight='normal'),command= lambda: DisplayDorks(0))

    if ret['Posts']:
        Bg_Canvas.create_window(buttons_coord['width'],buttons_coord['height'],window=Post_Button)
        buttons_coord['width'] += 333
    if ret['Stats']:
        Bg_Canvas.create_window(buttons_coord['width'],buttons_coord['height'],window=Stat_Button)
        buttons_coord['width'] += 333
    if ret['Dorks']:
        Bg_Canvas.create_window(buttons_coord['width'],buttons_coord['height'],window=Dork_Button)

def Gloading(xavier):

    [Bg_Canvas.delete(j) for i,j in IDs.items()]
    loading_axis = {'x1':244,'y1':323,'x2':276,'y2':353}
    SquareList = []
    IdList = []
    for i in range(16):
        SquareList.append((loading_axis['x1'],loading_axis['x2']))
        IdList.append(Bg_Canvas.create_rectangle(loading_axis['x1'],loading_axis['y1'],loading_axis['x2'],loading_axis['y2'],fill="#212121"))
        loading_axis['x1'] += 40
        loading_axis['x2'] += 40
    val = 0
    inc = 1
    while xavier.isSet() == False:
        if val == 0:
            inc = 1
        elif val == 15:
            inc = -1
        val += inc
        Bg_Canvas.create_rectangle(SquareList[val][0],loading_axis['y1'],SquareList[val][1],loading_axis['y2'],fill="#d9d9d9")
        sleep(0.05)
        Bg_Canvas.create_rectangle(SquareList[val][0],loading_axis['y1'],SquareList[val][1],loading_axis['y2'],fill="#212121")

    Bg_Canvas.delete("all")
    Bg_Canvas.create_image(0,0,image=bg,anchor="nw")
    Gresult()

def Ginput():
    global que
    que = queue.Queue()
    xavier = threading.Event()
    mThread = threading.Thread(target= lambda q,arg1,arg2 : q.put(main(arg1,arg2)),args=(que,User_Entry.get(),xavier))
    lThread = threading.Thread(target=Gloading,args=(xavier,))

    # Next steps of the program
    lThread.start()

    # Launching Osint engine
    mThread.start()

    # Keep the mainloop active
    return True

if __name__ == "__main__":

    # config
    IDs = {}
    root = Tk()
    Circus = tkFont.Font(family='HACKED', size=95, weight='normal')
    root.title("TIPE")
    root.geometry("1202x676")
    bg = PhotoImage(file="assets/background.png")
    root.iconbitmap('D:/TIPE/assets/bitmap.ico')
    # Background_Canvas
    Main_frame = Frame(root)
    Main_frame.pack(expand=YES)

    # Canvas
    Bg_Canvas = Canvas(Main_frame,width=1202, height=676)
    Bg_Canvas.create_image(0,0,image=bg,anchor="nw")
    Bg_Canvas.pack()

    # Username entry
    global User_Entry
    User_Entry = Entry(root,font=("Helvetica",40))
    User_Button = Button(root,text='Launch',font=tkFont.Font(family="HACKED", size=40,weight='normal'),command=Ginput)

    # Widgets IDs
    IDs['User_Entry_ID'] = Bg_Canvas.create_window(601,190, window=User_Entry)
    IDs['User_Button_ID'] = Bg_Canvas.create_window(601,295,window=User_Button)
    IDs['User_Text_ID'] = Bg_Canvas.create_text(601,85,text="USER",font=Circus,fill="white")

    # Never stop
    root.mainloop()
