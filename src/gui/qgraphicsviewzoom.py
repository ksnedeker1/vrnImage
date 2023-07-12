from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt


class QGraphicsViewZoom(QGraphicsView):
    """QGraphicsView promoted class to include scroll-zooming and click-drag-panning"""
    def __init__(self, parent):
        super(QGraphicsViewZoom, self).__init__(parent)
        self.is_panning = False
        self.mouse_click_pos = None

    def wheelEvent(self, event):
        """
        Defines zooming functionality on scroll wheel event. Overrides vertical scrolling.
        """
        # If scroll positive, zoom 5/4, else 4/5
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        """
        Defines 'click' start portion of click-and-drag functionality on mouse press.
        """
        # Left click start initializes click-and-drag by setting is_panning to True and storing the start pos
        if event.button() == Qt.LeftButton:
            self.mouse_click_pos = event.pos()
            self.is_panning = True
        # Preserve functionality of parent's implementation
        super(QGraphicsViewZoom, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """
        Defines 'click' release portion of click-and-drag functionality on mouse release.
        """
        # Left click release ends click-and-drag
        if event.button() == Qt.LeftButton:
            self.is_panning = False
        # Preserve functionality of parent's implementation
        super(QGraphicsViewZoom, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        Defines 'drag' portion of click-and-drag functionality on mouse move when left mouse button is pressed.
        """
        if self.is_panning:
            # calculate movement since initial LMB click
            move_pos = event.pos() - self.mouse_click_pos
            # updating the scrollbar positions updates the position of the image in the QGraphicsView
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - move_pos.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - move_pos.y())
            # update old position for future movement events
            self.mouse_click_pos = event.pos()
        # Preserve functionality of parent's implementation
        super(QGraphicsViewZoom, self).mouseMoveEvent(event)
