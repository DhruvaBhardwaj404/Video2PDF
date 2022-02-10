import cv2
import threading

class Converter:
    def __init__(self,location):
        self.video = cv2.VideoCapture(location)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.height=self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.width=self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.fcount = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.time=self.fcount/self.fps
        self.pages = list()
        self.processed=list()
        self.status=0
        self.status_lock= threading.Lock()


    def printVideoProps(self):
        print("fps",self.fps,"\nheight",self.height,"\nwidth",self.width,"\ntime",self.time)
        print("No. of pages",len(self.pages))

    def findBestFrames(self):

        interval=int(5*self.fps)
        t=1
        while(True):
            best=cv2.UMat()
            bestS=0;

            for frame in range(t,t+interval):
                self.video.set(1, frame)
                ret,cur =self.video.read()
                if(ret==False):
                    break;
                gcur=cv2.cvtColor(cur,cv2.COLOR_RGB2GRAY,)
                score=cv2.Laplacian(gcur,ddepth=cv2.CV_16S).var()
                if score>bestS:
                    best=cur
                    bestS=score
            self.pages.append(best)
            t+=interval

            self.status_lock.acquire()
            self.status=((t/(self.fcount*1.5))*100)
            self.status_lock.release()

            #remove after debug
            if(t>=100):
                break
            if(t>=self.fcount):
                break

    def getTemp(self):
        return (self.pages,self.processed)

    def cropPic(self):
        i=1
        pcount=len(self.pages)
        for up in self.pages:
            p=cv2.cvtColor(up,cv2.COLOR_RGB2GRAY)
            th, temp = cv2.threshold(p, 100, 255, cv2.THRESH_BINARY)
            self.pages.append(temp)
            border,hier = cv2.findContours(temp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            page_border=max(border,key=cv2.contourArea)
            x,y,w,h= cv2.boundingRect(page_border)
            temp=p[y:y+h,x:x+w]
            self.processed.append(temp)
            self.status_lock.acquire()
            self.status=75+((i/pcount)*25)
            self.status_lock.release()

    def testGui(self):
        win = cv2.namedWindow("Test")
        for x in self.processed:
            cv2.imshow("img",x)
            cv2.waitKey()

    def give_status(self):
        if(not(self.status_lock.locked())):
            return self.status

    def run(self):
        self.findBestFrames()
        self.cropPic()

if __name__ == "__main__":
    test=Converter("./video")
    test.findBestFrames()
    test.saveTemp()
    test.cropPic()
    test.testGui()
    test.printVideoProps()