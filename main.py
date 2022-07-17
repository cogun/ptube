from tkinter import *
from tkinter import ttk
import threading
import shutil
import requests
import os
from PIL import ImageTk, Image  
from youtubesearchpython import VideosSearch
from papi import Downloader

class Tile(ttk.Frame):
    def __init__(self,parent,callback,data = {}):
        ttk.Frame.__init__(self,parent)
        adjustString = lambda b: b.ljust(abs(28 - len(b)+5)," ") if len(b) < 28 else b[:28 - 3]+"..."

        self.mainFrame = ttk.Frame(self, style="Card",padding=(5, 6, 7, 8))
        self.mainFrame.pack(fill=X,padx=3,pady=3)

        self.frame = ttk.Frame(self.mainFrame)
        self.frame.pack(side=RIGHT,padx=3,pady=3)

        self.Detailsframe = ttk.Frame(self.mainFrame)
        self.Detailsframe.pack(padx=3,pady=3,side=LEFT)
        
        self.label = ttk.Label(self.Detailsframe,text=adjustString(data["title"]))
        self.label.pack(side=TOP)
        self.label = ttk.Label(self.Detailsframe,text=data["duration"] if data["duration"] else "live")
        self.label.pack(side=TOP,anchor=W)
        self.button = ttk.Button(self.frame,text="Play", style="Accent.TButton",padding=(0,0,0,0),command=lambda : callback(data))
        self.button.pack(side=RIGHT)

class App(Tk):
    def __init__(self):
        if not os.path.isdir("tmp"):
            os.makedirs("tmp", exist_ok=True)
        super().__init__()
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text ='Main')
        self.tabControl.add(self.tab2, text ='Play')
        self.tabControl.pack(expand = 1, fill ="both")
        self.currentSelection = ""
        self.tilesRef = []
        self.downloaderAPi = Downloader()
        self.resizable(False, False)
        self.geometry("850x420")
        self.setTheme("dark")
        self.top()
        self.middle()
        self.adjustString = lambda b: b.ljust(abs(28 - len(b)+5)," ") if len(b) < 28 else b[:28 - 3]+"..."
        self.setThumbnail("https://i.ytimg.com/vi/-x_OI0exTqY/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDxM0GyVJdIc1KPkdKoSvfowZMo_A")

    def adjustString(self,b,a = 33):
        if len(b) < a:
            return b.ljust(abs(28 - len(b)+5)," ")
        else:
            return b[:a - 3]+"..."
    def top(self):
        top = ttk.Frame(self.tab1, style='Accent.TFrame', padding=(5, 6, 7, 8))
        # search bar
        self.searchBar = ttk.Entry(top)
        self.searchBar.pack(fill=X,expand=1,side=LEFT)
        self.searchButton = ttk.Button(top,text="Search",style='Accent.TButton',command=lambda : threading.Thread(target=self.search).start())
        self.searchButton.pack(fill=X,side=LEFT,padx=5)
        top.pack(fill=X,side=TOP)

    def middle(self):
        self.middleFrame = ttk.Frame(self.tab1, style='Accent.TFrame', padding=(5, 6, 7, 8))
        self.preview()
        self.links()
        self.middleFrame.pack(fill=BOTH,side=TOP,expand=1)
    def preview(self):
        self.leftMiddleFrame = ttk.Frame(self.tab1,style='Card', padding=(5, 6, 7, 8))
        self.leftMiddleFrame.pack(fill=BOTH,side=LEFT,expand=1,padx=5,pady=5)

        togglebutton = ttk.Checkbutton(self.leftMiddleFrame, text='AutoPlay', style='Switch', )
        togglebutton.pack(anchor="w")

        self.frameMiddleone= ttk.Frame(self.leftMiddleFrame)
        self.frameMiddleone.pack(fill=X,side=TOP,expand=1)
        self.frameMiddletwo= ttk.Frame(self.leftMiddleFrame)
        self.frameMiddletwo.pack(fill=X,side=BOTTOM,expand=1)
        

        image1 = Image.open("tmp/thumb.png")
        resize_image = image1.resize((200, 120))
        test = ImageTk.PhotoImage(resize_image)
        self.thumbnail = ttk.Label(self.frameMiddleone,image=test)
        self.thumbnail.image = test
        self.thumbnail.pack(anchor=CENTER)

        self.titleLabel = ttk.Label(self.frameMiddleone,text=self.adjustString("Some title here | cool here punit"),style="Accent.TLabel")
        self.titleLabel.pack(side=TOP,padx=5,pady=5)

        self.downloadBtn = ttk.Button(self.frameMiddleone,text="Download",style="Accent.TButton",command=lambda : threading.Thread(target=self.handleDownloadBtn).start())
        self.downloadBtn.pack(side=TOP,padx=5,pady=5)

        self.progressLabel = ttk.Label(self.frameMiddletwo,text="0%",style="Accent.TLabel")
        self.progressLabel.pack(side=TOP,padx=5,pady=5)
        # progressBar
        self.progress = ttk.Progressbar(self.frameMiddletwo, orient = HORIZONTAL,
              length = 100, mode = 'determinate')
        self.progress['value'] = 0
        self.progress.pack(fill=X,padx=5)

    def setThumbnail(self,url):
        response = requests.get(url, stream=True)
        with open('tmp/thumb.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        image1 = Image.open("tmp/thumb.png")
        resize_image = image1.resize((200, 120))
        test = ImageTk.PhotoImage(resize_image)
        self.thumbnail.configure(image = test)
        self.thumbnail.image = test
    def links(self):
        self.rightMiddleFrame = ttk.Frame(self.tab1,width=10,style='Card', padding=(5, 6, 7, 8))
        self.rightMiddleFrame.pack(fill=BOTH,side=LEFT,expand=1,padx=5,pady=5)
        self.rightMiddleFrame.pack_propagate(0)

        self.canvas = Canvas(self.rightMiddleFrame,width=25,highlightthickness=0)
        self.canvas.pack(side=LEFT,fill=BOTH,expand=1)
        self.yscrollBar = ttk.Scrollbar(self.rightMiddleFrame,orient="vertical",command=self.canvas.yview)
        self.yscrollBar.pack(side=RIGHT,fill=Y)
        self.canvas.configure(yscrollcommand=self.yscrollBar.set)
        self.canvas.bind("<Configure>",lambda e:self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.linksFrame = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0),window=self.linksFrame,anchor="nw")

        for i in range(100):
            t = Tile(self.linksFrame,self.callback,{"title" : "some punit dataand ocoo dane","duration" : "5:34"})
            t.pack(fill=X)
            self.tilesRef.append(t)
            # lbl = ttk.Label(self.linksFrame,text=f"i am number{i}")
            # lbl.pack(fill=X,expand=1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def setTheme(self,type="light"):
        self.tk.call('source', f'theme/forest-{type}.tcl')
        ttk.Style().theme_use(f'forest-{type}')
    def clearTilesRef(self):
        for i in self.tilesRef:
            i.destroy()
    def search(self):
        self.searchButton["state"] = "disabled"
        text = self.searchBar.get().strip()
        if text:
            self.clearTilesRef()
            res =  VideosSearch(text, limit = 15)
            for i in res.result()["result"]:
                print(i)
                t = Tile(self.linksFrame,lambda x:threading.Thread(target=self.callback,args=(x,)).start(),i)
                t.pack(fill=X)
                self.tilesRef.append(t)
        self.searchButton["state"] = "normal"
    def callback(self,data = {}):
        self.setThumbnail(data["thumbnails"][0]["url"])
        self.titleLabel.configure(text=self.adjustString(data["title"]))
        print(data)
        self.currentSelection = data["link"]
    def handleDownloadBtn(self):
        if self.currentSelection.strip() == "": return False
        self.downloaderAPi.mkPath("songs/today")
        try:
            self.downloaderAPi.download(self.currentSelection,self.progress_function)
        except:
            print("live streams can't be loaded")
        self.progressLabel.configure(text="0%")
        self.progress['value'] = 0
        self.currentSelection = ""
    def handleDownload(self,progress):
        self.progressLabel.configure(text=f"{progress}%")
        self.progress['value'] = progress
    def progress_function(self,stream, chunk, bytes_remaining):
        print(round((1-bytes_remaining/self.downloaderAPi.video.filesize)*100, 3), '% done...')
        self.handleDownload(round((1-bytes_remaining/self.downloaderAPi.video.filesize)*100, 3))
app = App()
app.mainloop()