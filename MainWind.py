from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QComboBox, QWidget, QLabel, \
    QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
from GenWind import GenWindow
from OptWind import OptWindow


class MainWindow(QMainWindow):
    """Класс создающий главное окно приложения, в котором можно посмотреть информацию по каждому отдельному почтовому
    отделению. Помимо этого, благодаря кнопкам в нижней панели, из главного окна возможен переходам к окнам генерации
    данных и оптимизации соответственно"""
    def __init__(self):
        """Метод создания окна и размещения виджетов на нём; разбит на три смысловые части"""
        super().__init__()
        self.data = None
        self.setWindowTitle("Post optimisation")
        self.setFixedSize(QSize(500, 530))
        self.container = QWidget()
        self.layout = QVBoxLayout()
        self.init_upper_part()
        self.init_central_part()
        self.init_bottom_part()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def init_upper_part(self):
        """Создание верхней части окна, где осуществляется спецификация отображаемой информации"""
        self.label = QLabel("Get information on the post")
        self.comb = QComboBox()
        self.comb.addItems(["---"])
        self.comb.currentIndexChanged.connect(self.post_changed)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.comb)

    def init_central_part(self):
        """Создание центральной части с информацией"""
        self.inf_box = QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        plt.rc("xtick", labelsize=6)
        plt.rc("ytick", labelsize=6)
        self.time_list = [f"{9 + i}:00" for i in range(14)]
        self.label1 = QLabel("Price: ---")
        self.label2 = QLabel("Distance: ---")
        self.inf_box.addWidget(self.canvas)
        self.inf_box.addWidget(self.label1)
        self.inf_box.addWidget(self.label2)
        self.layout.addLayout(self.inf_box)

    def init_bottom_part(self):
        """Создание нижней части окна с кнопками"""
        self.but_box = QHBoxLayout()
        self.button1 = QPushButton("Generate")
        self.button1.clicked.connect(self.genWind)
        self.button2 = QPushButton("Optimise")
        self.button2.clicked.connect(self.optimisation)
        self.but_box.addWidget(self.button1)
        self.but_box.addWidget(self.button2)
        self.layout.addLayout(self.but_box)

    def genWind(self):
        """Внутренний метод, создающий окно для генерации данных. Вызывается по нажатию на кнопку Generate"""
        self.genwind = GenWindow(self)
        self.genwind.show()

    def post_changed(self, i):
        """Внутренний метод для изменения отображаемой информации; срабатывает при изменении ComboBox"""
        if i == 0:
            self.label1.setText("Price: ---")
            self.label2.setText("Distance: ---")
            self.figure.clear()
            self.canvas.draw()
        elif i > 0:
            self.label1.setText(f"Price: {self.data.get_price(int(i) - 1)}")
            self.label2.setText(f"Distance: {self.data.get_dist(int(i) - 1)}")
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set(ylim=[0, 100], xlabel="Hours", ylabel="Load %")
            ax.yaxis.set_major_locator(MultipleLocator(10))
            ax.plot(self.time_list, self.data.get_load(int(i) - 1), "*-")
            self.canvas.draw()

    def optimisation(self):
        """Внутренний метод, создающий окно с оптимизацией. Вызывается нажатием кнопки Optimise"""
        if self.data:
            self.optwind = OptWindow(self)
            self.optwind.show()
        else:
            self.warning()

    def warning(self):
        """Внутренний метод, вызывающийся при нажатии кнопка Optimise когда никаких данных еще не сгенерировано"""
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning")
        dlg.setText("There's no data to optimise!")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.exec()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
