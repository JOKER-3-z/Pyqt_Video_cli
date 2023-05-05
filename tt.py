from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from GUI import Ui_MainWindow
from myVideoWidget import myVideoWidget

import sys
import numpy as np
import cv2

class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.sld_video_pressed=False  #判断当前进度条识别否被鼠标点击
        self.videoFullScreen = False   # 判断当前widget是否全屏
        self.videoFullScreenWidget = myVideoWidget()   # 创建一个全屏的widget
        self.player = QMediaPlayer()
        self.player.setVideoOutput(self.wgt_video)  # 视频播放输出的widget，就是上面定义的
        self.btn_open.clicked.connect(self.openVideoFile)   # 打开视频文件按钮
        self.btn_play.clicked.connect(self.playVideo)       # play
        self.btn_stop.clicked.connect(self.pauseVideo)       # pause
        self.btn_cast.clicked.connect(self.castVideo)        # 视频截图
        self.player.positionChanged.connect(self.changeSlide)      # change Slide
        self.sld_video.setTracking(False)
        self.sld_video.sliderReleased.connect(self.releaseSlider)
        self.sld_video.sliderPressed.connect(self.pressSlider)
        self.sld_video.sliderMoved.connect(self.moveSlider)   # 进度条拖拽跳转
        self.sld_video.ClickedValue.connect(self.clickedSlider)  # 进度条点击跳转
        self.sld_audio.valueChanged.connect(self.volumeChange)  # 控制声音播放

    def castVideo(self):
        #截图
        screen = QGuiApplication.primaryScreen()
        cast_jpg = './image/'+QDateTime.currentDateTime().toString("dd-hh-mm-")+str(self.getTime(self.player.position()))+'.jpg'
        screen.grabWindow(self.wgt_video.winId()).save(cast_jpg)
        #img=self.qPixmapToCV()
        #cv2.imwrite(cast_jpg,img)

    def qPixmapToCV(self, qPixmap):  # PyQt图像 转换为 OpenCV图像
        qImg = qPixmap.toImage()  # QPixmap 转换为 QImage
        shape = (qImg.height(), qImg.bytesPerLine() * 8 // qImg.depth())
        shape += (4,)
        ptr = qImg.bits()
        ptr.setsize(qImg.byteCount())
        image = np.array(ptr, dtype=np.uint8).reshape(shape)  # 定义 OpenCV 图像
        image = image[..., :3]
        return image

    def volumeChange(self, position):
        volume= round(position/self.sld_audio.maximum()*100)
        print("vlume %f" %volume)
        self.player.setVolume(volume)
        self.lab_audio.setText("volume:"+str(volume)+"%")

    def clickedSlider(self, position):
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.lab_video.setText(self.getTime(self.player.position()))

        else:
            self.sld_video.setValue(0)

    def moveSlider(self, position):
        self.sld_video_pressed = True
        if self.player.duration() > 0:  # 开始播放后才允许进行跳转
            video_position = int((position / 100) * self.player.duration())
            self.player.setPosition(video_position)
            self.lab_video.setText(self.getTime(self.player.position()))

    def pressSlider(self):
        self.sld_video_pressed = True

    def releaseSlider(self):
        self.sld_video_pressed = False

    def changeSlide(self, position):
        if not self.sld_video_pressed:  # 进度条被鼠标点击时不更新
            self.vidoeLength = self.player.duration()+0.1
            self.sld_video.setValue(round((position/self.vidoeLength)*100))
            self.lab_video.setText(self.getTime(self.player.position()))

    def getTime(self,time):
        hours = time // (1000 * 60 * 60)
        minutes = (time % (1000 * 60 * 60)) // (1000 * 60)
        seconds = (time % (1000 * 60)) // 1000
        milliseconds = time % 1000
        return str(hours)+"-"+str(minutes)+"-"+str(seconds)+"-"+str(milliseconds)

    def openVideoFile(self):
        self.player.setMedia(QMediaContent(QFileDialog.getOpenFileUrl()[0]))  # 选取视频文件
        self.player.play()  # 播放视频

    def playVideo(self):
        self.player.play()

    def pauseVideo(self):
        self.player.pause()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vieo_gui = myMainWindow()
    vieo_gui.show()
    sys.exit(app.exec_())