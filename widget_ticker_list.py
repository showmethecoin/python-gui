import time
import sys
from widget_orderbook import OrderbookWorker
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QListWidget
from PyQt5.QtGui import QPainter
#from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime
import pyupbit
from PyQt5.QtCore import QThread, pyqtSignal

# from pyside_dynamic import loadUi
# from PySide2.QtUiTools import QUiLoader
# from PySide2.QtWidgets import QMainWindow, QWidget
# from PySide2.QtWidgets import QTableWidgetItem, QProgressBar
# from PySide2.QtCore import QFile, Qt, QThread, QPropertyAnimation, Signal

class TickerlistWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        uic.loadUi("chart_list.ui", self)
        
        self.coin_list.itemClicked.connect(self.chkItemClicked)
        
        ticker = pyupbit.get_tickers(fiat = 'KRW')
        self.coin_list.addItems(ticker)
        self.order = None
        self.chart = None
        self.trade = None
    
    def setOrder(self, order):
        self.order = order
    
    def setChart(self, chart):
        self.chart = chart
    
    def setTrade(self, trade):
        self.trade = trade
    
    def chkItemClicked(self):
        coin = self.coin_list.currentItem().text().split("-")[1]
        self.order.ow.close()
        self.order.ow.wait()
        self.order.ow = OrderbookWorker(coin)
        self.order.ow.dataSent.connect(self.order.updateData)
        self.order.ow.start()
        self.chart.coin = 'KRW-' + coin
        self.trade.set_price('KRW-' + coin)

    


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    cw = TickerlistWidget()
    cw.show()
    exit(app.exec_())
