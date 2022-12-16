from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QLabel, QSpinBox, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QListWidget, QAbstractItemView, QMessageBox


class OptWindow(QWidget):
    """Класс, создающий окно для оптимизации

    Параметры, задаваемые в данном окне:
    - Приоритеты учёта отдельных показателей (загруженность, цена, расстояние) -
      от 1 до 3 по убыванию (чем больше число, тем меньше приоритет)
    - Временные кванты, задействованные при оптимизации (для этого их надо выделять в ListWidget)

    При нажатии на кнопку Evaluate выведется небольшое окно, в котором и будет написан оптимальный варионт для похода,
    при заданных параметрах"""
    def __init__(self, parent):
        super().__init__()
        self.setFixedSize(QSize(350, 165))
        self.parent = parent
        self.setWindowTitle("Optimisation Window")

        layout = QVBoxLayout()
        active_part = QHBoxLayout()

        grid = QGridLayout()
        grid.addWidget(QLabel("Optimisation"), 0, 0)
        grid.addWidget(QLabel("priorities:"), 0, 1)
        labels = ["Load:", "Price:", "Distance:"]
        k = 1
        self.load_spin = QSpinBox()
        self.price_spin = QSpinBox()
        self.dist_spin = QSpinBox()
        for item in [self.load_spin, self.price_spin, self.dist_spin]:
            item.setFixedSize(QSize(33, 25))
            item.setMinimum(1)
            item.setMaximum(3)
            item.setValue(k)
            grid.addWidget(item, k, 1)
            grid.addWidget(QLabel(labels[k-1]), k, 0)
            k += 1
        active_part.addLayout(grid)

        hbox = QVBoxLayout()
        self.combo_box = QListWidget()
        self.combo_box.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.combo_box.addItems(self.parent.time_list)
        hbox.addWidget(QLabel("Available hours:"))
        hbox.addWidget(self.combo_box)
        active_part.addLayout(hbox)

        self.button = QPushButton("Evaluate")
        self.button.clicked.connect(self.optim)
        layout.addLayout(active_part)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def optim(self):
        """Внутренний метод, запускающий оптимизационные рассчёты при нажатии пользователем кнопки Evaluate"""
        selection = self.combo_box.selectedItems()
        if selection:
            priors = [0.5 ** self.load_spin.value(), 0.5 ** self.price_spin.value(), 0.5 ** self.dist_spin.value()]
            rows = [int(item.text().split(':')[0]) - 9 for item in self.combo_box.selectedItems()]
            rows.sort()
            answ = self.parent.data.optimise(rows, priors)
            self.dialog("Result", f"The optimal variant is to go to Post №{answ[1]} at {answ[0]}:00",
                        QMessageBox.Icon.Information)
        else:
            self.dialog("Warning", "No hours were chosen!", QMessageBox.Icon.Critical)

    def dialog(self, title, text, icon):
        """Внутренний метод, автоматически вызывающийся сразу после оптимизации и выводящий её реультат на экран;
        если не были выбраны временные интервалы, то выведет ошибку"""
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(text)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(icon)
        dlg.exec()
