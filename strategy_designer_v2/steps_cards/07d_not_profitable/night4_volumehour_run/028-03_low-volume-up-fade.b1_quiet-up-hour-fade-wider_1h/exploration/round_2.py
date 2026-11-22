import numpy as np, pandas as pd

def explore(data):
    H = [6, 12]
    rows = []
    mk = []
    for coin, ws in data["bars"].items():
        drift = {}
        for h in H + [24]:
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            drift[h] = np.concatenate(allr).mean()
        d1 = drift[24]
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            f = b["forecast"].fillna(0).values
            a = b["postRebalance_current_allocation"].fillna(0).values
            r1 = pd.Series(c).pct_change()
            mabs = r1.abs().rolling(720, min_periods=240).mean()
            z = (r1 / mabs).values
            r72 = pd.Series(c).pct_change(72).values
            hour = pd.to_datetime(b["timestamp"]).dt.hour.values
            grid = np.arange(n) // 6
            seen = set()
            for i in np.where(f <= -2)[0]:
                if grid[i] in seen: continue
                seen.add(grid[i])
                rec = {"coin": coin, "z": z[i], "r72": r72[i], "hour": hour[i],
                       "usd": 6 * mabs.values[i]}
                for h in H:
                    if i + h < n:
                        rec[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[h])
                        rec[f"t{h}"] = -(c[i + h] / c[i] - 1)
                    else:
                        rec[f"u{h}"] = np.nan; rec[f"t{h}"] = np.nan
                rows.append(rec)
            # market part of position gain per bar
            g = a[:-1] * (c[1:] / c[:-1] - 1)
            mk.append({"coin": coin, "mean_alloc": a.mean(), "gain_bar": g.mean(),
                       "share_short": (a < 0).mean(), "turn": np.abs(np.diff(a)).mean()})
    df = pd.DataFrame(rows)

    def summ(g):
        o = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna(); y = g[f"t{h}"].dropna()
            o[f"u{h}%"] = 100 * x.mean(); o[f"t_u{h}"] = x.mean() / (x.std() / np.sqrt(len(x)))
            o[f"tot{h}%"] = 100 * y.mean(); o[f"t_tot{h}"] = y.mean() / (y.std() / np.sqrt(len(y)))
        return pd.Series(o)
    res = {}
    df["r72q"] = pd.qcut(df["r72"], 5, duplicates="drop")
    res["by_prior3d"] = df.groupby("r72q").apply(summ)
    df["hb"] = df["hour"] // 4
    res["xmr_by_hour4"] = df[df.coin == "XMRUSD"].groupby("hb").apply(summ)
    res["hour0_by_coin"] = df[df.hb == 0].groupby("coin").apply(summ)
    df["zq"] = pd.qcut(df["z"], 5, duplicates="drop")
    res["hour0_by_z"] = df[df.hb == 0].groupby("zq").apply(summ)
    M = pd.DataFrame(mk)
    res["position"] = M.groupby("coin").agg(mean_alloc=("mean_alloc", "mean"), gain_bar=("gain_bar", "mean"),
                                           share_short=("share_short", "mean"), turnover_bar=("turn", "mean"))
    return res
