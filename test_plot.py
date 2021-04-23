from datetime import time
import sys, os, random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import mpl_finance as mpf
import json
import random
from pyupbit.quotation_api import get_ohlcv
import requests
import pandas as pd
import mpl_finance
import datetime
import pyupbit

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=12, height=8, dpi=100):
        # mpl.style.use(['dark_background'])
        plt.rcParams['axes.facecolor'] = '31363b'
        plt.rcParams['axes.edgecolor'] = 'ffffff'
        plt.rcParams['xtick.color'] = 'ffffff'
        plt.rcParams['ytick.color'] = 'ffffff'

        self.fig = Figure(figsize=(5, 3))
        self.fig.set_facecolor('#31363b')
        self.fig.set_edgecolor('#ffffff')
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

class AnimationWidget(QWidget):
    def __init__(self,parent = None):
        super().__init__(parent)
        vbox = QVBoxLayout()
        self.canvas = MyMplCanvas(self, width=10, height=8, dpi=100)
        self.count = 15
        self.coin = 'KRW-BTC'
        vbox.addWidget(self.canvas)
        hbox = QHBoxLayout()
        self.start_button = QPushButton("+", self)
        self.stop_button = QPushButton("-", self)
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.get_chart()
        self.canvas.draw
        self.ani = animation.FuncAnimation(self.canvas.fig, self.animate,interval=1000)


    # chart update
    def get_chart(self):
        df = get_ohlcv(ticker=self.coin, interval="minutes1", count=self.count, to=None)

        # url = "https://api.upbit.com/v1/candles/minutes/1"
        # querystring = {"market":"KRW-ADA","count": str(self.count)}

        # response = requests.request("GET", url, params=querystring)
        # jobject = json.loads(response.text)
        # df = pd.DataFrame(jobject)
        # df = df.sort_values(['candle_date_time_kst'])
        # df = df.set_index('candle_date_time_kst')
        # plt.xticks(df['candle_date_time_kst'])'
        # x = [datetime.datetime.strptime(x, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M") for x in df['candle_date_time_kst']]


        # x = np.array(x)
        # x = np.insert(x, 0, 0)
        # x = x[::2]
        # x.insert(0,0)
        #self.canvas.axes.set_xticklabels(x, minor=False, rotation = 45)

        # from matplotlib.ticker import MultipleLocator
        # # self.canvas.axes.xaxis.set_minor_locator(MultipleLocator(1))
        # self.canvas.axes.xaxis.set_major_locator(MultipleLocator(1))
        
        # mpl_finance.candlestick2_ohlc(self.canvas.axes, df['opening_price'], df['high_price'], df['low_price'], df['trade_price'], width=0.5, colorup='r', colordown='b')
        mpl_finance.candlestick2_ohlc(self.canvas.axes, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup='r', colordown='b')

    # animation function
    def animate(self, t):
        self.canvas.axes.clear()
        self.get_chart()

    def on_start(self):
        if self.count < 200:
            self.count += 5
    
    def on_stop(self):
        if self.count > 15:
            self.count -= 5

if __name__ == "__main__":
    qApp = QApplication(sys.argv)
    aw = AnimationWidget()
    aw.show()
    sys.exit(qApp.exec_())