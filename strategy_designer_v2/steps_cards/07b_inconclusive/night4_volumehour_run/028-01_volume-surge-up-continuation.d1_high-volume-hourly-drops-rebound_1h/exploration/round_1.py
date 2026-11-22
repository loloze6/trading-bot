import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [3, 6, 12, 24]
    rows = []
    drift = {}
    usual = {}
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = np.nanmean(rs)
            usual[(coin, h)] = np.nanstd(rs)
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sd = r.rolling(720, min_periods=120).std()
            vr = df["volume"] / df["volume"].rolling(720, min_periods=120).mean()
            zr = r / sd
            s = zr * vr
            year = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"].fillna(0).values
            cv = c.values
            for h in H:
                fut = np.full(len(cv), np.nan)
                fut[:-h] = cv[h:] / cv[:-h] - 1
                rows.append(pd.DataFrame({
                    "coin": coin, "win": w, "h": h, "pos": np.arange(len(cv)),
                    "zr": zr.values, "vr": vr.values, "s": s.values, "fc": fc,
                    "year": year.values, "fut": fut,
                    "ex": fut - drift[(coin, h)], "u": usual[(coin, h)]}))
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fut", "zr", "vr"])
    A["cell"] = A["pos"] // A["h"]

    def cases(mask):
        sub = A[mask]
        return sub.groupby(["coin", "win", "h", "cell"], sort=False).head(1)

    def summ(sub, keys, sign=1):
        g = sub.assign(e=sign * sub["ex"] * 100).groupby(keys)["e"]
        out = g.agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.drop(columns="std").round(3)

    res = {}
    # the brief's contrast: big moves with heavy vs ordinary volume, both sides; sign = continuation
    A["big"] = A["zr"].abs() >= 3
    A["vcls"] = pd.cut(A["vr"], [0, 1.5, 3, 1e9], labels=["vol<1.5", "vol1.5-3", "vol>3"])
    A["side"] = np.where(A["zr"] > 0, "up", "down")
    cb = cases(A["big"])
    cb = cb.assign(cont=np.where(cb["side"] == "up", 1, -1) * cb["ex"] * 100)
    g = cb.groupby(["h", "side", "vcls"], observed=True)["cont"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    res["big moves |z|>=3, continuation excess % by h/side/vol"] = g.drop(columns="std").round(3)
    # graded drops: by size of s (negative)
    A["sb"] = pd.cut(A["s"], [-1e9, -20, -10, -5, -2, 0], labels=["<-20", "-20..-10", "-10..-5", "-5..-2", "-2..0"])
    cd = cases(A["s"] < -2)
    res["drops by s bucket, rebound excess % (long)"] = summ(cd, ["h", "sb"])
    # recorded forecast cases by year at 24h and 6h
    cf = cases(A["fc"] > 0)
    res["fc>0 cases long excess by h, coin"] = summ(cf, ["h", "coin"])
    res["fc>0 cases long excess by h=24, year"] = summ(cf[cf.h == 24], ["year"])
    res["fc>0 cases long excess by h=6, year"] = summ(cf[cf.h == 6], ["year"])
    return res
