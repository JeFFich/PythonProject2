import numpy as np


class Post:
    """Класс, реализующий внутреннюю работу программы

    Поля класса:
    load - матрица (14 x n - кол-во почтовых отделений) случайных десятичных дробей от 0 до 1;
           является матрицей показателей загруженности отделений по квантам времени(часам)
    prices - n-мерный вектор случайных целых чисел в диапазоне price;
            является вектором цены для каждого соответствующего отделения
    dist - n-мерный вектор случайных целых чисел в диапазоне dis;
            является вектором расстояний до каждого соответсвующего отделения
    _price - целое число; верхний порог цены (нужно для нормализации вектора цен при оптимизации)
    _dist - целое число; верхний порог расстояния (нужно для нормализации вектора расстояний при оптимизации)"""
    def __init__(self, count=7, price=(10, 100), dis=(150, 500)):
        self.load = np.round(np.random.uniform(0.05, 0.95, (14, count)), 2)
        self.prices = np.random.randint(price[0], price[1], count)
        self.dist = np.random.randint(dis[0], dis[1], count)
        self._price = price[1]
        self._dist = dis[1]

    def get_load(self, n):
        """Метод для получения загруженности для конкретного отделения
        (нужен для построения графика в информационном блоке интерфейса)
        На вход получает номер отделения"""
        return self.load[n]

    def get_price(self, n):
        """Метод для получения цены в конкретном отделении
        (нужен для отображения в информационном блоке интерфейса)
        На вход получает номер отделения"""
        return self.prices[n]

    def get_dist(self, n):
        """Метод для получения удаленности конкретного отделения
        (нужен для отображения в информационном блоке интерфейса)
        На вход получает номер отделения"""
        return self.dist[n]

    def optimise(self, time, prior=(1, 0.5, 0.25), file="log.txt"):
        """Функция, вычисляющая наилучший день для похода, исходя из линейной оптимизации
        показателей загруженности, цены и удалённости
        На вход принимает кортеж оптимизирующих коэффицентов для соответствующих показателей
        + временные разметки для взятия среза по определенным часам
        Последовательность этапов рассчёта записывается в текстовый файл (по умолчанию - log.txt)
        На выходе возвращает кортеж из времени и номера отделения для оптимального похода"""
        _normal_price = np.round(self.prices / self._price, 2)
        print(f"Normalized price-vector: {self.prices} -> {_normal_price}")
        _normal_dist = np.round(self.dist / self._dist, 2)
        print(f"Normalized dist-vector: {self.dist} -> {_normal_dist}")
        _load_cut = self.load[time].copy()
        print(f"Time-cut load: {self.load} -> {_load_cut}")
        _linear_craft = _load_cut * prior[0] + _normal_price * prior[1] + _normal_dist * prior[2]
        print(f"Linear optimisation, according to priorities: {_linear_craft}")
        with open(file, "w") as f:
            f.write(f"""Normalized price-vector: 
{self.prices} -> {_normal_price}
Normalized dist-vector: 
{self.dist} -> {_normal_dist}
Time-cut load: 
{self.load} 
(Getting rows {time})
{_load_cut}
Linear optimisation, according to prioritysing coefficients ({prior[0]} - for load, {prior[1]} - for price, {prior[2]} - for distance): 
{_linear_craft}""")
        _optim = np.unravel_index(_linear_craft.argmin(), _linear_craft.shape)
        return time[_optim[0]] + 9, _optim[1] + 1
