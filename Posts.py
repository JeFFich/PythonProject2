import numpy as np


class Post:
    def __init__(self, count=7, price=(10, 100), dist=(150, 500)):
        self.load = np.round(np.random.random((14, count)), 2)
        self.prices = np.random.randint(price[0], price[1], count)
        self.dist = np.random.randint(dist[0], dist[1], count)
        self._price = price[1]
        self._dist = dist[1]

    def get_load(self, n):
        return self.load[n]

    def get_price(self, n):
        return self.prices[n]

    def get_dist(self, n):
        return self.dist[n]

    def optimise(self, time, prior=(1, 0.5, 0.25), file="log.txt"):
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
