"""The size of an idea (definition: common/measures.md, "The size of an idea"), measured on a backtest record from its
prices and its forecast only: no position, no cost. Used by step 5 next to its verdict.

  from idea_size import size; size(record_dir, horizon)

Why this can't leak: it reads a finished record after the fact; it changes no decision.
"""
import math, pathlib
import numpy as np
import pandas as pd
from bets import bets, band_of


def size(record, H):
    """Cases, the unusual move (mean), the coin's normal drift in the cases' direction (mean), the total move (mean),
    the coin's usual move (median over coins) and the strength (mean), over every coin and window of the record."""
    record = pathlib.Path(record); band = band_of(record)
    unusual, drift_part, total, strength, usual = [], [], [], [], []
    for coin in sorted(p for p in record.iterdir() if p.is_dir()):
        frames = [pd.read_csv(f, usecols=["close", "forecast"]) for f in sorted(coin.glob("w*/bars.csv.gz"))]
        stretches = []
        for fr in frames:
            c = fr["close"].to_numpy(float)
            if len(c) > H:
                stretches.append(c[H::H] / c[:len(c[H::H]) * H:H] - 1)
        r = np.concatenate(stretches) if stretches else np.array([])
        if len(r) < 3:
            continue
        drift, sd = float(r.mean()), float(r.std(ddof=1))
        if not sd > 0:
            continue
        usual.append(sd)
        for fr in frames:
            c = fr["close"].to_numpy(float); fc = fr["forecast"].fillna(0).to_numpy(float); seen = set()
            for t in bets(fc, band):
                if t + H >= len(c) or t // H in seen:
                    continue
                seen.add(t // H); s = 1.0 if fc[t] > 0 else -1.0; m = c[t + H] / c[t] - 1
                unusual.append(s * (m - drift)); drift_part.append(s * drift); total.append(s * m)
                strength.append(s * (m - drift) / sd)
    if not unusual:
        return {"horizon_bars": H, "cases": 0}
    mean = lambda x: float(np.mean(x))
    return {"horizon_bars": H, "cases": len(unusual), "unusual_move": mean(unusual), "normal_drift": mean(drift_part),
            "total_move": mean(total), "usual_move": float(np.median(usual)), "strength": mean(strength)}
