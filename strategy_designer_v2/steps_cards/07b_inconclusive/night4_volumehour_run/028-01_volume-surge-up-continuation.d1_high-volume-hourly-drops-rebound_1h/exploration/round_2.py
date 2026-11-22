import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [3, 6, 12, 24]
    rows = []
    drift = {}; usual = {}
    for coin in bars:
        for h in H:
            rs = []
            for w, df in bars[coin].items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs)
            drift[(coin, h)] = np.nanmean(rs); usual[(coin, h)] = np.nanstd(rs)
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; r = c.pct_change()
            sd = r.rolling(720, min_periods=120).std()
            vr = df["volume"] / df["volume"].rolling(720, min_periods=120).mean()
            zr = r / sd
            year = pd.to_datetime(df["timestamp"]).dt.year
            cv = c.values
            for h in H:
                fut = np.full(len(cv), np.nan); fut[:-h] = cv[h:] / cv[:-h] - 1
                rows.append(pd.DataFrame({"coin": coin, "win": w, "h": h, "pos": np.arange(len(cv)),
                    "zr": zr.values, "vr": vr.values, "s": (zr * vr).values, "year": year.values,
                    "fut": fut, "ex": fut - drift[(coin, h)], "u": usual[(coin, h)]}))
    A = pd.concat(rows, ignore_index=True).dropna(subset=["fut", "zr", "vr"])
    A["cell"] = A["pos"] // A["h"]
    def cases(mask):
        return A[mask].groupby(["coin", "win", "h", "cell"], sort=False).head(1)
    def summ(sub, keys, col="ex"):
        g = sub.assign(e=sub[col] * 100).groupby(keys, observed=True)["e"]
        out = g.agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        return out.drop(columns="std").round(3)
    res = {}
    up = cases((A["s"] > 2))
    up = up.assign(sb=pd.cut(up["s"], [2, 5, 10, 20, 1e9], labels=["2-5", "5-10", "10-20", ">20"]),
                   tot=up["fut"], st=up["ex"] / up["u"])
    res["up s buckets, excess % by h"] = summ(up, ["h", "sb"])
    u24 = up[up.h == 24]
    res["up s>5, h24 excess by coin"] = summ(u24[u24.s > 5], ["coin"])
    res["up s>5, h24 excess by year"] = summ(u24[u24.s > 5], ["year"])
    res["up s>5, h24 total %"] = summ(u24[u24.s > 5], ["h"], "tot")
    res["up s>5, h24 strength"] = round(float(u24[u24.s > 5]["st"].mean()), 4)
    x = u24["s"].clip(upper=50); y = u24["ex"]
    res["up h24 OLS slope ex on s, n"] = f"{np.polyfit(x, y, 1)[0]:.6f}, n={len(x)}, corr={np.corrcoef(x,y)[0,1]:.4f}"
    dn = cases((A["s"] < -5) & (A["s"] >= -10))
    res["drop -10..-5 h3 by year"] = summ(dn[dn.h == 3], ["year"])
    res["drop -10..-5 h3 by coin"] = summ(dn[dn.h == 3], ["coin"])
    return res
