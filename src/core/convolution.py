import numpy as np


def stepwise_convolution(x, h):
    """
    Compute stepwise convolution using the shift-and-dot-product logic.

    Parameters:
        x : array-like
            Input signal
        h : array-like
            Impulse response / filter

    Returns:
        outputs : list
            Stepwise convolution values (each shift result)
        y_full : ndarray
            Full convolution using np.convolve for verification
    """
    x = np.asarray(x)
    h = np.asarray(h)

    n_x = len(x)
    n_h = len(h)
    n_out = n_x + n_h - 1  # length of convolution output

    outputs = []

    # Zero-pad input signal
    x_padded = np.pad(x, (0, n_out - n_x))

    for i in range(n_out):
        # Shift and pad h
        h_shifted = np.zeros(n_out)
        h_shifted[i : i + n_h] = h[: max(0, n_out - i)]

        # Stepwise convolution (dot product)
        y_step = np.dot(x_padded, h_shifted)
        outputs.append(y_step)

    # Full convolution using numpy for verification
    y_full = np.convolve(x, h, mode="full")

    return outputs, y_full
