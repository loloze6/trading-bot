import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    hrs = []
    for coin, wins in bars.items():
        # pooled drift/std per horizon
        fw = {}
        for h in (24, 120):
            allr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                allr.append(c[idx + h] / c[idx] - 1)
            allr = np.concatenate(allr)
            fw[h] = (allr.mean(), allr.std(ddof=1))
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            z = r24 / r24.abs().rolling(720, min_periods=120).mean().shift(1)
            r1 = np.log(c).diff()
            vr = r1.rolling(24).std() / r1.rolling(720, min_periods=120).std()
            r120 = c / c.shift(120) - 1
            z120 = r120 / r120.abs().rolling(720, min_periods=120).mean().shift(1)
            r720 = c / c.shift(720) - 1
            n = len(c)
            for h in (24, 120):
                idx = np.arange(0, n - h, h)
                fr = c.values[idx + h] / c.values[idx] - 1
                s = (fr - fw[h][0]) / fw[h][1]
                rows.append(pd.DataFrame({"coin": coin, "h": h, "z": z.values[idx], "vr": vr.values[idx],
                                          "z120": z120.values[idx], "r720": r720.values[idx], "s": s}))
            fr1 = c.shift(-1) / c - 1
            hrs.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday, "r": fr1}))
    D = pd.concat(rows).dropna(subset=["s"])
    H = pd.concat(hrs).dropna()
    out = {}
    def agg(g):
        return pd.Series({"n": len(g), "mean_s": g["s"].mean(), "t": g["s"].mean() / (g["s"].std() / np.sqrt(len(g)))})
    for key in ("z", "vr", "z120", "r720"):
        d = D.dropna(subset=[key]).copy()
        d["b"] = d.groupby(["coin", "h"])[key].transform(lambda x: pd.qcut(x, 10, labels=False, duplicates="drop"))
        out[key + "_decile"] = d.groupby(["h", "b"]).apply(agg).reset_index()
    # spearman per coin z vs s at 120
    sp = []
    for (coin, h), g in D.dropna(subset=["z"]).groupby(["coin", "h"]):
        for key in ("z", "vr", "z120", "r720"):
            gg = g.dropna(subset=[key])
            rho, p = stats.spearmanr(gg[key], gg["s"])
            sp.append({"coin": coin, "h": h, "key": key, "rho": rho, "n": len(gg)})
    out["spearman"] = pd.DataFrame(sp).pivot_table(index=["key", "h"], columns="coin", values="rho")
    hh = H.groupby("hour")["r"].agg(["mean", "std", "count"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["hour_bps"] = (hh[["mean", "t"]] * [1e4, 1]).round(2)
    ww = H.groupby("wd")["r"].agg(["mean", "std", "count"])
    ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["count"]))
    out["wd_bps"] = (ww[["mean", "t"]] * [1e4, 1]).round(2)
    return out
