from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QInputDialog, QFileDialog
app = QApplication([])
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
from PIL import Image
import os
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)



notes_win = QWidget()
notes_win.setWindowTitle('Easy Editor')
notes_win.resize(900, 600)

papka_ = QListWidget()
lb_image = QLabel('Картинка')
button_papka = QPushButton('Папка') #появляется окно с полем "Введите имя заметки"
button_rotate_left = QPushButton('Лево')
button_rotate_right = QPushButton('Право')
button_mirror = QPushButton('Зеркало')
button_rezk= QPushButton('Резкость')
button_black_white = QPushButton('Черно\белоая')
vert1 = QVBoxLayout()
vert2 = QVBoxLayout()
gorizont1 = QHBoxLayout()
gorizont2 = QHBoxLayout()
vert1.addWidget(button_papka)
vert1.addWidget(papka_)
vert2.addWidget( lb_image)
gorizont2.addWidget(button_rotate_left)
gorizont2.addWidget(button_rotate_right)
gorizont2.addWidget(button_mirror)
gorizont2.addWidget(button_rezk)
gorizont2.addWidget(button_black_white)
vert2.addLayout(gorizont2)
gorizont1.addLayout(vert1, 20)
gorizont1.addLayout(vert2, 80)
notes_win.setLayout(gorizont1)
workdir = ""
def filter(files,extensions):
    result= []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                result.append(file)
    return result
def chjoseWordir():
    global workdir
    workdir =   QFileDialog.getExistingDirectory()
def showFilenames():
    extensions = [".jpg",".jpeg",".png",".gif",".bmp"]
    chjoseWordir()
    filenames= filter(os.listdir(workdir), extensions)
    papka_.clear()
    for filename in filenames:

        papka_.addItem(filename)
button_papka.clicked.connect(showFilenames)
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    def LoadImage(self , dir , filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir , filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w , h , Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir , self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def flp(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def shrp(self):
       self.image = self.image.filter(SHARPEN)
       self.saveImage()
       image_path = os.path.join(workdir, self.save_dir, self.filename)
       self.showImage(image_path)


def ShowChosenImage():
    if papka_.currentRow() >=0:
        filename = papka_.currentItem().text()
        workimage.LoadImage(workdir , filename)
        image_path = os.path.join(workimage.dir,  workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()
papka_.currentRowChanged.connect(ShowChosenImage)
button_black_white.clicked.connect(workimage.do_bw)
button_rotate_left.clicked.connect(workimage.do_left)
button_mirror.clicked.connect(workimage.flp)
button_rotate_right.clicked.connect(workimage.do_right)
button_rezk.clicked.connect(workimage.shrp)
notes_win.show()
app.exec_()