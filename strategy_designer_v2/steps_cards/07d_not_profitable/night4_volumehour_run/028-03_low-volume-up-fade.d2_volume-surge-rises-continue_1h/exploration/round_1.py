import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = [1, 2, 6, 12, 24]
    rows = []
    book = []
    for coin, wins in data["bars"].items():
        # coin's normal drift per horizon over all windows
        drift = {}
        sd = {}
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[h] = rs.mean(); sd[h] = rs.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            z = r / r.rolling(720, min_periods=120).std().shift(1)
            vr = b["volume"] / b["volume"].rolling(720, min_periods=120).mean().shift(1)
            n = len(b)
            # sample each 6-bar grid cell's first bar (non-overlapping, per h=6 grid) -- use every bar but grid by 24 to keep independence of 24h
            for h in H:
                idx = np.arange(0, n - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                df = pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx],
                                   "vr": vr.values[idx], "u": (fwd - drift[h]) / sd[h], "um": fwd - drift[h],
                                   "fc": b["forecast"].values[idx]})
                rows.append(df)
            a = b["postRebalance_current_allocation"].fillna(0)
            gross = a * (c.shift(-1) / c - 1)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            book.append(pd.DataFrame({"coin": coin, "w": w, "gross": gross, "fee": fee,
                                      "turn": b["allocation_change"].abs() if "allocation_change" in b else np.nan}))
    D = pd.concat(rows)
    D = D.dropna(subset=["z", "vr", "u"])
    D["zb"] = pd.cut(D["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    D["vb"] = pd.cut(D["vr"], [0, 1, 2, 3, 5, np.inf])
    res = []
    for h in [2, 6, 24]:
        s = D[D.h == h]
        g = s.groupby(["zb", "vb"], observed=True)["u"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g = g[g["count"] >= 30].reset_index(); g["h"] = h
        res.append(g[["h", "zb", "vb", "mean", "count", "t"]])
    out["strength by zbin x volbin (h=2,6,24)"] = pd.concat(res).round(3).iloc[:40]
    # simple signed effect: corr of u with sign(z)*vr etc per horizon
    eff = []
    for h in H:
        s = D[D.h == h]
        big = s[s.z.abs() > 2]
        x = np.sign(big.z) * big.u
        eff.append({"h": h, "n_big": len(big), "cont_strength_big": x.mean(),
                    "t": x.mean() / (x.std() / np.sqrt(len(x))),
                    "cont_big_volhi": (np.sign(big.z) * big.u)[big.vr > 3].mean(),
                    "n_volhi": (big.vr > 3).sum(),
                    "cont_big_vollo": (np.sign(big.z) * big.u)[big.vr <= 1.5].mean(),
                    "n_vollo": (big.vr <= 1.5).sum()})
    out["continuation after |z|>2 by horizon (strength units)"] = pd.DataFrame(eff).round(4)
    B = pd.concat(book)
    gb = B.groupby("coin")[["gross", "fee"]].sum()
    out["book gross vs fee sums per coin (bar shares)"] = gb.round(4)
    out["mean gross per bar, mean fee per bar"] = pd.Series({"gross": B.gross.mean(), "fee": B.fee.mean(),
                                                             "share bars in position": (B.gross != 0).mean()}).round(6)
    # by year for book days
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["year"] = pd.to_datetime(d["day"]).dt.year; d["coin"] = coin; dl.append(d)
    Dd = pd.concat(dl)
    out["book by year"] = Dd.groupby("year")[["book_return", "coin_return"]].mean().round(5)
    return out
