def apply_shock(base_curve, shock_bp):
    """Apply shock vector (bp) to base curve; floor at zero."""
    return np.maximum(base_curve + shock_bp / 10000, 0.0)

SCENARIOS = {
    "Parallel Up (+250bp)":     np.full(9,  250),
    "Parallel Down (-250bp)":   np.full(9, -250),
    "Steepener":                np.array([-100, -80, -50, -20,   0,  20,  50,  80, 100]),
    "Flattener":                np.array([ 100,  80,  50,  20,   0, -20, -50, -80,-100]),
    "Short Rate Up (+300bp)":   np.array([ 300, 250, 200, 150,  75,  30,  10,   5,   0]),
    "Short Rate Down (-300bp)": np.array([-300,-250,-200,-150, -75, -30, -10,  -5,   0]),
}
