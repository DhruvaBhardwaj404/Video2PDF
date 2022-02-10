from tkinter import Tk,BOTH,X,Y,CENTER,TOP,PhotoImage,StringVar,LEFT,Menu,Message,filedialog,IntVar,Canvas
from tkinter.ttk import Frame,Label,Button,Style,Labelframe,Entry,Progressbar
from converter import Converter
import time
import threading
import math

class GUI_interface(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.parent = parent
        self.loc = StringVar(value='./')
        self.UI_handler()
        self.status=IntVar()
        self.status.set(0)
        self.status_mess=StringVar()


    def UI_handler(self):
        self.parent.title("V2P")
        self.pack(fill=BOTH, expand=True)
        styles = Style()
        bgIMG = PhotoImage("./bg.png")
        styles.configure("head.TFrame", background="SlateBlue4",backgroundhighlight='black',relief="ridge",border=10,colourhighlight="slateblue3")
        styles.configure("cont.TFrame", background="aliceblue",relief="sunken",border=10,colourhighlight="slategray1")
        styles.configure("head.TLabelframe",font=("ubuntu","30"),border=10,backgroundhighlight='black')
        self.toolBar()
        self.header()
        self.content()

    def toolBar(self):
        menu=Menu(self,tearoff=False)
        self.parent.config(menu=menu)
        menu.add_command(label="Setting",command=self.get_settings)
        menu.add_command(label="Version", command=self.get_settings)
        menu.add_command(label="Developer", command=self.get_settings)

    def header(self):
        self.headFrame = Frame(self,height=100,relief="sunken",border=5,style="head.TFrame")
        self.headFrame.rowconfigure(2, weight=3)
        self.headFrame.columnconfigure(1,weight=1)
        self.headFrame.columnconfigure(2,weight= 3)
        self.headFrame.columnconfigure(3, weight=1)
        self.headFrame.pack(fill=X)
        heading= Message(self.headFrame,text="V2P")
        heading.config(font=("Apple SD Gothic Neo",40),background='SlateBlue4',foreground="snow")
        heading.grid(column=1,row=2,pady=20)

    def content(self):
        self.contentFrame= Frame(self,relief='ridge',border=5,style="cont.TFrame")
        self.contentFrame.pack(fill=BOTH,expand=True)
        innerLabel=Labelframe(self.contentFrame,text="Let's convert!",)
        innerLabel.pack(fill=BOTH,padx=50,pady=160)
        locationV=Entry(innerLabel,textvariable=self.loc,width=200)
        locationV.pack(pady=20,padx=20)
        changeBut=Button(innerLabel,text="Change Location",command=lambda : self.changeLocation(self.loc))
        continueBut=Button(innerLabel,text="Convert",command=lambda : [self.gotoConversionScreen(),threading.Thread(target=self.convert).start(),threading.Thread(target=self.update_Status).start()])
        changeBut.pack(pady=10)
        continueBut.pack(pady=5)

    def convert(self):
        try:
            print("In convert")
            self.Con = Converter(self.loc.get())

        except:
            self.status_mess = "An Error Occurred! Choose a video File!"
            self.convertFrame.pack_forget()
            self.contentFrame.pack(fill=BOTH)
            return

        self.Con.run()

    def changeLocation(self,current):
        getLocation = filedialog.askopenfilename(title='Choose Your Video', initialdir=current)
        self.loc.set(getLocation)
        print(self.loc)

    def gotoConversionScreen(self):
        self.contentFrame.pack_forget()
        self.convertFrame = Frame(self, style="cont.TFrame", height=600)
        self.convertFrame.pack(fill=BOTH, expand=True)

        for x in range(0, 5):
            self.convertFrame.rowconfigure(str(x), weight=1)
            self.convertFrame.columnconfigure(str(x), weight=1)
        statusBar = Progressbar(self.convertFrame,variable=self.status, length=100)
        statusBar.grid(row=2, column=1, columnspan=3)

    def gotoPreviewScreen(self):
        self.convertFrame.pack_forget()
        self.PFrame= Frame(self,style="cont.TFrame")
        for x in range(0, 9):
            self.convertFrame.rowconfigure(str(x), weight=1)
            self.convertFrame.columnconfigure(str(x), weight=1)
        back=Button(self.PFrame,text="<",command=lambda : self.changeImage(-1))
        next=Button(self.PFrame,text=">",command=lambda : self.changeImage(1))
        self.IFrame=Frame(self.PFrame)
        self.curr_Image=IntVar()
        self.curr_Image.set(0)
        self.PFrame.pack()
        back.grid(column=1,row=4)
        next.grid(column=9,row=4)
        self.displayImage()
        canvas = Canvas(self.PFrame)
        canvas.create_bitmap(self.pro_Image)
        self.canvas.grid(column=2, columnspan=7, row=1, rowspan=9)
        canvas.pack()
# TODO: saves images to jpeg and then use them in GUI for preview

    def displayImage(self):
      pass


    def changeImage(self,i):
        pass
    def get_settings(self):
        pass

    def update_Status(self):
        while(True):
            time.sleep(1)
            self.status.set(self.Con.give_status())

            if(self.status.get()==100):
                self.status_mess="Completed!"
                self.raw_Image,self.pro_Image = self.Con.getTemp()
                self.gotoPreviewScreen()
                break

def main():
    root = Tk()
    root.config(bg="AntiqueWhite1")
    root.geometry("800x640")
    root.resizable()
    main_win= GUI_interface(root)
    root.mainloop()
    print("hello")

if __name__ =="__main__":
    main()
