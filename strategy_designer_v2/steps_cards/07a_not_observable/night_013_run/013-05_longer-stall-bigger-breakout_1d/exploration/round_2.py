import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            n = len(df)
            tr = (df["regime"] == "trending").values
            c = df["close"].values
            yr = pd.to_datetime(df["timestamp"].iloc[0]).year
            g = [i for i in range(0, n, 30) if i + 30 < n]
            rows.append(dict(coin=coin, window=w, wn=int(w[1:]), year=yr,
                             grid_full=len(g), trend_grid=int(sum(tr[i] for i in g)),
                             trend_bars=int(tr.sum()),
                             trend_bars_fwd=int(sum(tr[i] for i in range(n - 30)))))
    R = pd.DataFrame(rows)
    out = {}
    out["per window index"] = R.groupby("wn")[["year", "grid_full", "trend_grid", "trend_bars", "trend_bars_fwd"]].agg(
        {"year": "min", "grid_full": "sum", "trend_grid": "sum", "trend_bars": "sum", "trend_bars_fwd": "sum"})
    out["per coin grid"] = R.groupby("coin")[["grid_full", "trend_grid", "trend_bars_fwd"]].sum()
    out["per year grid"] = R.groupby("year")[["grid_full", "trend_grid", "trend_bars_fwd"]].sum()
    tot = R["grid_full"].sum()
    out["rate trend grid per full grid bar"] = R["trend_grid"].sum() / tot
    out["rate trend bar per bar with fwd"] = R["trend_bars_fwd"].sum() / (R["grid_full"].sum() * 30)
    out["coin-windows"] = len(R)
    out["grid per coin-window"] = tot / len(R)
    return out
