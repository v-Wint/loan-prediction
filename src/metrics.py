import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import make_scorer


def build_curve(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    order = np.argsort(y_pred)[::-1]
    y_true = y_true[order]
    y_pred = y_pred[order]

    cumsum = np.cumsum(y_true)
    counts = np.arange(1, len(y_true) + 1)
    return pd.DataFrame({
        'threshold': y_pred,
        'sum': cumsum,
        'mean': cumsum / counts,
    })


def curve_threshold(curve):
    return curve.threshold[curve['sum'].idxmax()]

def curve_max(curve):
    return curve['sum'].max()

def curve_base(curve):
    return curve['sum'].iloc[-1]

def curve_lift(curve):
    return curve_max(curve) / curve_base(curve)

def curve_net_improv(curve):
    return curve_max(curve) - curve_base(curve)


def plot_curve(curve, xline=0):
    curve.plot(x='threshold', y=['sum', 'mean'], secondary_y='mean')
    plt.axvline(x=xline, color='red', linestyle='--')
    threshold = curve_threshold(curve)
    plt.axvline(x=threshold, color='green', linestyle='--')
    print(f"Threshold: {threshold:.4f}\nLift: {curve_lift(curve):.4f} times\nNet improvement: ${curve_max(curve):e} - ${curve_base(curve):e} = ${curve_net_improv(curve):e}")


def lift_score(y_true, y_pred):
    curve = build_curve(y_true, y_pred)
    return curve_lift(curve)


lift_scorer = make_scorer(lift_score, greater_is_better=True)
