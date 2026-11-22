import numpy as np
import pandas as pd

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3 or x.std() == 0:
        return np.nan
    return x.mean() / (x.std() / np.sqrt(len(x)))

def _summ(g, col):
    return pd.Series({"n": g[col].notna().sum(), "mean_bps": g[col].mean()*1e4, "t": _t(g[col])})

def explore(data):
    out = {}
    h1, past = [], {}
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c.pct_change()
            sd = r1.rolling(720, min_periods=240).std()
            fwd1 = c.shift(-1) / c - 1
            h1.append(pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year, "hour": ts.dt.hour,
                                    "wd": ts.dt.weekday, "fwd": fwd1}))
            for L, H in ((24, 24), (72, 24), (24, 6), (72, 72)):
                key = f"p{L}_f{H}"
                idx = np.arange(0, len(b), H)
                pr = (c / c.shift(L) - 1) / (sd * np.sqrt(L))
                fw = c.shift(-H) / c - 1
                past.setdefault(key, []).append(pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year.values[idx],
                                                              "pz": pr.values[idx], "fwd": fw.values[idx]}))
    g = pd.concat(h1, ignore_index=True).dropna(subset=["fwd"])
    g["unus"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    g["late"] = g["hour"].isin([20, 21])
    g["early"] = g["hour"].isin([0, 1, 2])
    lt = g[g["late"]]
    out["h20_21_by_coin"] = lt.groupby("coin").apply(lambda x: _summ(x, "unus"))
    out["h20_21_by_year"] = lt.groupby("year").apply(lambda x: _summ(x, "unus"))
    out["h20_21_by_weekday"] = lt.groupby("wd").apply(lambda x: _summ(x, "unus"))
    wm = lt.groupby(["coin", "win"])["unus"].mean()
    out["h20_21_share_windows_pos"] = pd.Series({"windows": len(wm), "share_pos": (wm > 0).mean()})
    et = g[g["early"]]
    out["h0_2_by_year"] = et.groupby("year").apply(lambda x: _summ(x, "unus"))
    # hour 20-21 grouped together, 2h sum per day (non-overlapping by construction)
    for key, lst in past.items():
        p = pd.concat(lst, ignore_index=True).dropna(subset=["pz", "fwd"])
        p["unus"] = p["fwd"] - p.groupby("coin")["fwd"].transform("mean")
        p["q"] = pd.qcut(p["pz"], 10, labels=False)
        out[f"{key}_by_decile"] = p.groupby("q").apply(lambda x: _summ(x, "unus"))
        sl = np.polyfit(p["pz"].clip(-4, 4), p["unus"], 1)[0]
        out[f"{key}_slope_bps_per_unit"] = sl * 1e4
        if key == "p24_f24":
            lo = p[p["q"] <= 1]
            out["p24_f24_low2dec_by_coin"] = lo.groupby("coin").apply(lambda x: _summ(x, "unus"))
            out["p24_f24_low2dec_by_year"] = lo.groupby("year").apply(lambda x: _summ(x, "unus"))
    return out
