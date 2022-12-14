import numpy as np
import datetime


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
    def __init__(self, count, price, dis):
        self.load = np.round(np.random.uniform(0.05, 0.95, (14, count)), 2)
        self.prices = np.random.randint(price[0], price[1], count)
        self.dist = np.random.randint(dis[0], dis[1], count)
        self._price = price[1]
        self._dist = dis[1]

    def get_load(self, n):
        """Метод для получения загруженности для конкретного отделения
        (нужен для построения графика в информационном блоке интерфейса)
        На вход получает номер отделения"""
        return (self.load[:, n] * 100).tolist()

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

    def optimise(self, time, prior):
        """Функция, вычисляющая наилучший день для похода, исходя из линейной оптимизации
        показателей загруженности, цены и удалённости
        На вход принимает кортеж оптимизирующих коэффицентов для соответствующих показателей
        + временные разметки для взятия среза по определенным часам
        Последовательность этапов рассчёта записывается в текстовый файл (по умолчанию - log.txt)
        На выходе возвращает кортеж из времени и номера отделения для оптимального похода"""
        self._normal_price = np.round(self.prices / self._price, 2)
        self._normal_dist = np.round(self.dist / self._dist, 2)
        self._load_cut = self.load[time].copy()
        self._linear_craft = self._load_cut * prior[0] + self._normal_price * prior[1] + self._normal_dist * prior[2]
        self._optim = np.unravel_index(self._linear_craft.argmin(), self._linear_craft.shape)
        self.log(time, prior)
        return time[self._optim[0]] + 9, self._optim[1] + 1

    def log(self, time, prior, file="log.txt"):
        """Функция для вывода последовательности рассчётов в log файл. Работает в связке с otimise"""
        with open(file, "w") as f:
            f.write(f"""Evaluation at {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
Input data:
--------
    Posts load:
{self.load}
    Price-vector:
{self.prices}
    Distance-vector:
{self.dist}
    Prioritysing coefficients:
{prior}
    Time-cut (rows to take):
{time}
--------
Linear Optimisation: 
1) Normalizing price-vector: 
    {self._normal_price}
2) Normalizing dist-vector: 
    {self._normal_dist}
3) Time-cutting load: 
{self._load_cut}
4) Applying prioritysing coefficients:
    {prior[0]} - for load:
{self._load_cut * prior[0]}
    {prior[1]} - for price:
{self._normal_price * prior[1]}
    {prior[2]} - for distance:
{self._normal_dist * prior[2]}
5) Linear convergence: 
{self._linear_craft}
6) Finding minimum index: {self._optim}
7) Returning to real indexes: Post №{self._optim[1] + 1}, Time {time[self._optim[0]] + 9}:00""")
