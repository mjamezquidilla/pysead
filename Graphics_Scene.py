import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)

        # settings
        self.grid_size = 30
        self.grid_squares = 5

        self.color_background = QColor('#19232D')
        self.setBackgroundBrush(self.color_background)

        self.scene_width, self.scene_height = 64000, 64000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)

        self.color_light = QColor('#455364')
        self.pen_light = QPen(self.color_light)
        self.pen_light.setWidth(1)

        self.color_dark = QColor('#455364')
        self.pen_dark = QPen(self.color_dark)
        self.pen_dark.setWidth(3)
        
        self.color_red = QColor('#D64550')
        self.pen_red = QPen(self.color_red)
        self.pen_red.setWidth(3)
        
        self.color_green = QColor('#69995D')
        self.pen_green = QPen(self.color_green)
        self.pen_green.setWidth(3)

    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        lines_light, lines_dark, lines_red, lines_green = [], [], [], []
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)
        lines_green.append(QLine(left, 0, right, 0))
        lines_red.append(QLine(0, top, 0, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if (y % (self.grid_size*self.grid_squares) != 0): lines_light.append(QLine(left, y, right, y))
            else: lines_dark.append(QLine(left, y, right, y))
        for x in range(first_left, right, self.grid_size):
            if (x % (self.grid_size*self.grid_squares) != 0): lines_light.append(QLine(x, top, x, bottom))
            else: lines_dark.append(QLine(x, top, x, bottom))
            

        painter.setPen(self.pen_light)
        painter.drawLines(*lines_light)

        painter.setPen(self.pen_dark)
        painter.drawLines(*lines_dark)

        painter.setPen(self.pen_red)
        painter.drawLines(*lines_red)

        painter.setPen(self.pen_green)
        painter.drawLines(*lines_green)
  
 