import numpy as np


class TimeAxis:
    """Time Engine"""

    def __init__(self, t_min=-5.0, t_max=5.0, dt=0.001, signal_mode="Continuous"):
        self.t_min = t_min
        self.t_max = t_max
        self.dt = dt
        self.signal_mode = signal_mode

    def generate(self):
        if self.signal_mode == "Discrete":
            num_points = int((self.t_max - self.t_min) / self.dt)
            num_points = min(max(num_points, 10), 500)  # clamp
            return np.linspace(self.t_min, self.t_max, num_points)

        return np.arange(self.t_min, self.t_max + self.dt, self.dt)

    def update(self, t_min=None, t_max=None, dt=None):
        if t_min is not None:
            self.t_min = t_min
        if t_max is not None:
            self.t_max = t_max
        if dt is not None:
            self.dt = dt
