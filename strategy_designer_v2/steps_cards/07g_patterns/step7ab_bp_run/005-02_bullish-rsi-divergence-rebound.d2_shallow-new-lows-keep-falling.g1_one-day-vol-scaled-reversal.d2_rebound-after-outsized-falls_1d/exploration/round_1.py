import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        drift1 = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=20).std()
            z = r1 / sd
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(c)),
                               "z": z, "sd": sd, "r20": c / c.shift(20) - 1,
                               "r5": c / c.shift(5) - 1,
                               "wd": ts.dt.dayofweek, "year": ts.dt.year,
                               "fc": b["forecast"].astype(float)})
            for h in (1, 3, 5, 10):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)

    def tab(key, h, nq=5):
        g = d[d["pos"] % h == 0].dropna(subset=[key, f"f{h}"]).copy()
        g["q"] = g.groupby("coin")[key].transform(lambda s: pd.qcut(s, nq, labels=False, duplicates="drop"))
        res = g.groupby("q")[f"f{h}"].agg(["mean", "std", "count"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        res["keymean"] = g.groupby("q")[key].mean()
        return res.round(5)

    for h in (1, 3, 5, 10):
        out[f"z1 quintile -> fwd {h}d"] = tab("z", h)
    for h in (5, 10):
        out[f"r20 quintile -> fwd {h}d"] = tab("r20", h)
        out[f"r5 quintile -> fwd {h}d"] = tab("r5", h)
        out[f"vol20 tercile -> fwd {h}d"] = tab("sd", h, 3)
    g = d.dropna(subset=["f1"])
    wd = g.groupby("wd")["f1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday -> next day"] = wd.round(5)
    # z extreme falls by year
    g = d.dropna(subset=["z", "f1"])
    big = g[g["z"] < -1.5]
    yr = big.groupby("year")["f1"].agg(["mean", "count"])
    out["z<-1.5 next day by year"] = yr.round(5)
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; bd.append(x)
    bd = pd.concat(bd)
    out["book daily mean/std/n"] = bd["book_return"].agg(["mean", "std", "count"]).round(6)
    out["coins"] = ",".join(data["bars"].keys())
    return out
