import numpy as np
import pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std(ddof=1) == 0:
        return (n, np.nan, np.nan)
    return (n, x.mean(), x.mean() / (x.std(ddof=1) / np.sqrt(n)))

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        g3 = []
        frames = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            d = pd.DataFrame({
                "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values,
                "r1": r1.values,
                "r2": (c / c.shift(2) - 1).values,
                "f1": (c.shift(-1) / c - 1).values,
                "f2": (c.shift(-2) / c - 1).values,
                "f3": (c.shift(-3) / c - 1).values,
                "f6": (c.shift(-6) / c - 1).values,
                "mabs": r1.abs().rolling(20).mean().shift(1).values,
                "vol20": r1.rolling(20).std().values,
                "vratio": (b["volume"].rolling(20).mean().shift(2) /
                           b["volume"].rolling(2).mean()).values,
                "fc": b["forecast"].values,
            })
            d["coin"] = coin
            d["w"] = w
            frames.append(d)
            g3.append((c.iloc[::3].shift(-1) / c.iloc[::3] - 1).dropna())
        g3 = pd.concat(g3)
        drift, usual = g3.mean(), g3.std(ddof=1)
        D = pd.concat(frames)
        D["u3"] = (D["f3"] - drift) / usual
        D["u1"] = (D["f1"] - drift / 3) / usual
        D["u6"] = (D["f6"] - 2 * drift) / usual
        D["z"] = D["r1"] / D["mabs"]
        D["vrank"] = D["vol20"].rank(pct=True)
        rows.append(D)
    A = pd.concat(rows).dropna(subset=["r1", "u3", "z"])
    A["fade3"] = -np.sign(A["r1"]) * A["u3"]
    A["fade1"] = -np.sign(A["r1"]) * A["u1"]
    A["fade6"] = -np.sign(A["r1"]) * A["u6"]
    A["fade2d"] = -np.sign(A["r2"]) * A["u3"]

    out = {}
    names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    res = []
    for wd in range(7):
        s = A[A["wd"] == wd]
        n, m, t = _t(s["fade3"])
        _, m1, t1 = _t(s["fade1"])
        _, m6, t6 = _t(s["fade6"].dropna())
        sl = stats.linregress(s["z"].clip(-6, 6), -s["u3"])
        res.append([names[wd], n, round(m, 4), round(t, 2), round(m1, 4), round(t1, 2),
                    round(m6, 4), round(t6, 2), round(sl.slope, 4), round(sl.slope / sl.stderr, 2)])
    out["fade strength by weekday of move (u=usual 3d move)"] = pd.DataFrame(
        res, columns=["day", "n", "fade3", "t3", "fade1d", "t1d", "fade6d", "t6d", "slope_z", "t_slope"])

    S = A[A["wd"] == 6].copy()
    S["zq"] = pd.qcut(S["z"].abs(), 5, labels=False)
    out["Sunday fade3 by |z| quintile"] = S.groupby("zq")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])
    S["sign"] = np.where(S["r1"] > 0, "rise", "fall")
    out["Sunday fade3 by sign"] = S.groupby("sign")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])
    S["vq"] = pd.qcut(S["vrank"], 3, labels=["lowvol", "midvol", "highvol"])
    out["Sunday fade3 by vol tercile"] = S.groupby("vq")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])
    out["Sunday fade3 by year"] = S.groupby("year")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])
    S["vrq"] = pd.qcut(S["vratio"], 3, labels=["heavy", "mid", "thin"])
    out["Sunday fade3 by thinness tercile"] = S.groupby("vrq")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])
    out["Sunday: fade of 2-day weekend move"] = pd.Series(_t(S["fade2d"]), index=["n", "mean", "t"])

    W = A[A["wd"] < 5].copy()
    W["vq"] = pd.qcut(W["vrank"], 3, labels=["lowvol", "midvol", "highvol"])
    out["Weekday(Mon-Fri) fade3 by vol tercile"] = W.groupby("vq")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])
    W["zq"] = pd.qcut(W["z"].abs(), 5, labels=False)
    out["Weekday(Mon-Fri) fade3 by |z| quintile"] = W.groupby("zq")["fade3"].agg(["count", "mean", lambda x: _t(x)[2]])

    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd = d.copy()
            dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
            bd.append(dd[["wd", "book_return", "coin_return"]])
    bd = pd.concat(bd).dropna()
    out["book & coin daily return by weekday"] = bd.groupby("wd").agg(
        n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t[["side", "net_profit_loss_percent"]])
    tr = pd.concat(tr)
    out["trades by side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
