from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QPushButton, QGridLayout
from Posts import Post


class GenWindow(QWidget):
    """Класс, создающий окно генерации данных

    Параметры, задаваемые в данном окне:
    - общее число отделений
    - диапазон цен (с обязательной разницей в 1)
    - диапазон расстояний (с обязательной разницей в 1)

    При нажатии на кнопку Generate создаётся новый объект класса Post, на котором производится оптимизация дня похода
    Также очищащается информативное поле в центре главного окна"""
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(QSize(250, 120))
        self.parent = parent
        self.setWindowTitle("Generating Window")

        self.spin_amount = QSpinBox()
        self.spin_amount.setFixedSize(QSize(33, 25))
        self.spin_amount.setMinimum(1)
        self.spin_amount.setMaximum(25)
        self.spin_amount.setValue(5)

        self.price_min_spin = QSpinBox()
        self.price_min_spin.setFixedSize(QSize(47, 25))
        self.price_min_spin.setMinimum(1)
        self.price_min_spin.setMaximum(99)
        self.price_min_spin.setValue(10)
        self.price_min_spin.valueChanged.connect(self.min_price_changed)
        self.price_max_spin = QSpinBox()
        self.price_max_spin.setFixedSize(QSize(47, 25))
        self.price_max_spin.setMinimum(11)
        self.price_max_spin.setMaximum(10000)
        self.price_max_spin.setValue(100)
        self.price_max_spin.valueChanged.connect(self.max_price_changed)

        self.dist_min_spin = QSpinBox()
        self.dist_min_spin.setFixedSize(QSize(47, 25))
        self.dist_min_spin.setMinimum(100)
        self.dist_min_spin.setMaximum(999)
        self.dist_min_spin.setValue(100)
        self.dist_min_spin.setSingleStep(10)
        self.dist_min_spin.valueChanged.connect(self.min_dist_changed)
        self.dist_max_spin = QSpinBox()
        self.dist_max_spin.setFixedSize(QSize(47, 25))
        self.dist_max_spin.setMinimum(101)
        self.dist_max_spin.setMaximum(100000)
        self.dist_max_spin.setValue(1000)
        self.dist_max_spin.setSingleStep(10)
        self.dist_max_spin.valueChanged.connect(self.max_dist_changed)

        self.gen_but = QPushButton("Generate")
        self.gen_but.clicked.connect(self.generate)

        layout = QGridLayout()
        layout.addWidget(QLabel("Amount of Posts:"), 0, 0)
        layout.addWidget(self.spin_amount, 0, 1)
        layout.addWidget(QLabel("Price range:"), 1, 0)
        layout.addWidget(self.price_min_spin, 1, 1)
        layout.addWidget(QLabel(" -- "), 1, 2)
        layout.addWidget(self.price_max_spin, 1, 3)
        layout.addWidget(QLabel("Distance range: "), 2, 0)
        layout.addWidget(self.dist_min_spin, 2, 1)
        layout.addWidget(QLabel(" -- "), 2, 2)
        layout.addWidget(self.dist_max_spin, 2, 3)
        layout.addWidget(self.gen_but, 3, 0)
        self.setLayout(layout)

    def min_price_changed(self):
        """Динамический внутренний метод изменения нижней границы SpinBox с максимальной ценой"""
        self.price_max_spin.setMinimum(self.price_min_spin.value() + 1)

    def max_price_changed(self):
        """Динамический внутренний метод изменения верхней границы SpinBox с минимальной ценой"""
        self.price_min_spin.setMaximum(self.price_max_spin.value() - 1)

    def min_dist_changed(self):
        """Динамический внутренний метод изменения нижней границы SpinBox с максимальным расстоянием"""
        self.dist_max_spin.setMinimum(self.dist_min_spin.value() + 1)

    def max_dist_changed(self):
        """Динамический внутренний метод изменения верхней границы SpinBox с минимальным расстоянием"""
        self.dist_min_spin.setMaximum(self.dist_max_spin.value() - 1)

    def generate(self):
        """Внутренний метод генерации данных, вызывается при нажатии пользователем кнопки Generate"""
        self.parent.data = Post(count=self.spin_amount.value(),
                                price=(self.price_min_spin.value(), self.price_max_spin.value()),
                                dis=(self.dist_min_spin.value(), self.dist_max_spin.value()))
        self.parent.comb.clear()
        self.parent.figure.clear()
        self.parent.canvas.draw()
        self.parent.comb.addItems(["---"] + [str(i) for i in range(1, self.spin_amount.value() + 1)])
