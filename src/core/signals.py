import re

import numpy as np


# Compatibility helper: some NumPy builds may not expose `np.trapz`.
# Provide a small fallback implementation using the composite trapezoidal rule.
def _trapz(y, x):
    try:
        return np.trapz(y, x)
    except AttributeError:
        y = np.asarray(y)
        x = np.asarray(x)
        if y.size < 2:
            return 0.0
        dx = np.diff(x)
        return np.sum((y[:-1] + y[1:]) * 0.5 * dx)


class Signal:
    """Core Signal Class"""

    def __init__(self, func, name, formula, params=None):
        self.func = func
        self.name = name
        self._base_formula = formula
        self.params = params or {}

        # Transformation state
        self._time_shift = 0.0  # τ
        self._time_scale = 1.0  # a
        self._fold = False  # x(-t)

    @property
    def formula(self):
        """Dynamic formula reflecting transformations"""
        t_str = "t"

        # Fold (inversion)
        if self._fold:
            t_str = f"-{t_str}"  # no extra parentheses if not needed

        # Time scale
        if self._time_scale != 1.0:
            t_str = f"{self._time_scale}*{t_str}"

        # Time shift
        if self._time_shift != 0.0:
            sign = "-" if self._time_shift > 0 else "+"
            t_str = f"{t_str}{sign}{abs(self._time_shift)}"

        # Replace standalone t in base formula
        formula_str = re.sub(r"\bt\b", t_str, self._base_formula)

        return f"{formula_str}"

    def evaluate(self, t):
        # shift
        t_shifted = t - self._time_shift

        # time scale
        t_scaled = self._time_scale * t_shifted

        # fold
        if self._fold:
            t_final = -t_scaled
        else:
            t_final = t_scaled

        return self.func(t_final, **self.params)

    # -------- Transformations --------
    def time_shift(self, tau):
        self._time_shift += tau
        return self

    def time_scale(self, a):
        self._time_scale *= a
        return self

    def fold(self):
        self._fold = not self._fold
        return self

    # -------- Algebra --------
    def __add__(self, other):
        return Signal(
            lambda t: self.evaluate(t) + other.evaluate(t),
            name=f"({self.name}+{other.name})",
            formula=f"({self.formula}) + ({other.formula})",
        )

    def __mul__(self, other):
        # Support scalar multiplication and Signal * Signal
        if isinstance(other, (int, float, np.number)):
            return Signal(
                lambda t: self.evaluate(t) * other,
                name=f"({self.name}*{other})",
                formula=f"{other}·({self.formula})",
            )

        # Signal * Signal
        if isinstance(other, Signal):
            return Signal(
                lambda t: self.evaluate(t) * other.evaluate(t),
                name=f"({self.name}*{other.name})",
                formula=f"({self.formula}) · ({other.formula})",
            )

        return NotImplemented

    def __rmul__(self, other):
        # Support scalar * Signal
        return self.__mul__(other)

    def energy(self, t):
        """
        Approximate signal energy over a finite interval:
        E ≈ ∫_{t_min}^{t_max} |x(t)|² dt
        """
        x = self.evaluate(t)

        if len(t) < 2:
            return 0.0

        y = np.abs(x) ** 2

        if np.any(np.isnan(y)) or np.any(np.isinf(y)):
            return np.inf

        return _trapz(y, t)

    def power(self, t):
        """
        Approximate average power over a finite interval:
        P ≈ (1/T) ∫_{t_min}^{t_max} |x(t)|² dt

        NOTE: True definition is as T → ∞
        """
        x = self.evaluate(t)

        if len(t) < 2:
            return 0.0

        T = t[-1] - t[0]
        if T <= 0:
            return 0.0

        y = np.abs(x) ** 2

        if np.any(np.isnan(y)) or np.any(np.isinf(y)):
            return np.inf

        return _trapz(y, t) / T

    def classify_signal(self, t):
        """
        Robust classification using convergence behavior.
        """

        x = self.evaluate(t)

        if len(t) < 2:
            return "Undefined", 0.0, 0.0

        dt = t[1] - t[0]
        N = len(x)

        # Edge case: zero signal
        if np.all(x == 0):
            return "Zero Signal", 0.0, 0.0

        # Progressive window sizes
        splits = np.linspace(N // 5, N - 1, 5).astype(int)

        energies = []
        for s in splits:
            E = np.sum(np.abs(x[:s]) ** 2) * dt
            energies.append(E)

        energies = np.array(energies)

        # ---- Classification logic ----

        # Case 1: Energy stabilizes → Energy Signal
        if np.all(np.abs(np.diff(energies)) < 1e-2):
            return "Energy Signal", energies[-1], 0.0

        # Case 2: Energy keeps growing → Power Signal
        elif np.all(np.diff(energies) > 0):
            T = t[splits[-1]] - t[0]
            P = energies[-1] / T if T > 0 else 0.0
            return "Power Signal", np.inf, P

        # Case 3: Neither
        else:
            T = t[-1] - t[0]
            P = energies[-1] / T if T > 0 else 0.0
            return "Neither", energies[-1], P


# Signal Factory Functions
# -----------------------------------------------------------------------


def unit_impulse():
    return Signal(
        func=lambda t: np.where(np.isclose(t, 0), 1.0, 0.0),
        name="Unit Impulse",
        formula="δ(t)",
    )


def unit_step(constant=1.0):
    return Signal(
        func=lambda t, constant=constant: np.where(t >= 0, constant, 0.0),
        name="Unit Step",
        formula="u(t)",
        params={"constant": constant},
    )


def ramp():
    return Signal(
        func=lambda t: np.where(t >= 0, t, 0.0),
        name="Ramp",
        formula="t × u(t)",
    )


def exponential(c=1.0, a=1.0):
    return Signal(
        func=lambda t, c=c, a=a: c * np.exp(a * t) * (t >= 0),
        name="Exponential",
        formula=f"{c}e^({a}t)",
        params={"a": a},
    )


def sinusoid(amplitude=1.0, frequency=1.0, phase=0.0):
    return Signal(
        func=lambda t, amplitude=amplitude, frequency=frequency, phase=phase: amplitude
        * np.sin(2 * np.pi * frequency * t + phase),
        name="Sinusoid",
        formula=f"{amplitude}·sin(2π{frequency}t+{phase})",
        params={
            "amplitude": amplitude,
            "frequency": frequency,
            "phase": phase,
        },
    )


def sinc_signal(amplitude=1.0):
    return Signal(
        func=lambda t, amplitude=amplitude: amplitude * np.sinc(t),
        name="Sinc",
        formula="sin(πt)/(πt)",
        params={"amplitude": amplitude},
    )


def signum_signal():
    return Signal(
        func=lambda t: np.sign(t),
        name="Signum",
        formula="sgn(t)",
    )


def rectangular_pulse(start=-1.0, end=1.0, amplitude=1.0):
    return Signal(
        func=lambda t, start=start, end=end, amplitude=amplitude: np.where(
            (t >= start) & (t <= end), amplitude, 0.0
        ),
        name="Rectangular Pulse",
        formula=f"{amplitude}·rect(t)",
        params={"start": start, "end": end, "amplitude": amplitude},
    )


def triangular_wave(start=0.0, end=1.0, amplitude=1.0):
    def tri(t, start=start, end=end, amplitude=amplitude):
        x = 1 - np.abs(2 * (t - start) / (end - start) - 1)
        x[x < 0] = 0
        return amplitude * x

    return Signal(
        func=tri,
        name="Triangular",
        formula=f"{amplitude}·tri(t)",
        params={"start": start, "end": end, "amplitude": amplitude},
    )


# Registry
# ==============================
SIGNAL_REGISTRY = {
    "unit_impulse": unit_impulse,
    "unit_step": unit_step,
    "ramp": ramp,
    "exponential": exponential,
    "Sinusoidal": sinusoid,
    "sinc": sinc_signal,
    "signum": signum_signal,
    "rectangular": rectangular_pulse,
    "triangular": triangular_wave,
}


def get_available_signals():
    """Return all registered signal names in display format (title case with spaces)"""
    display_names = []
    for key in SIGNAL_REGISTRY.keys():
        # Replace underscores with space and capitalize each word
        name = key.replace("_", " ").title()
        display_names.append(name)
    return display_names


def get_signal_modes():
    return ("Continuous", "Discrete")
