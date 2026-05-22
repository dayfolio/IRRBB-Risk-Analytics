TENORS       = np.array([1/365, 0.25, 0.5, 1, 2, 3, 5, 7, 10])


def interp_rate(curve, tenor):
    """Linearly interpolate yield curve at given tenor (in years)."""
    if tenor <= 0:
        return float(curve[0])
    return float(np.interp(tenor, TENORS, curve))
