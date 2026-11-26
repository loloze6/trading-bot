import numpy as np, pandas as pd
from scipy import stats

def tday(g, col):
    s = g.groupby("day")[col].sum()
    n = len(s)
    return pd.Series({"cases": len(g), "days": n, "mean%": g[col].mean()*100,
                      "t_day": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            nxt3 = c.shift(-3) / c - 1
            tr60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            pct = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            clpos = (c - b["low"]) / hl
            hi20 = b["high"].rolling(20).max(); lo20 = b["low"].rolling(20).min()
            rpos = (c - lo20) / (hi20 - lo20).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "nxt": nxt, "nxt3": nxt3, "tr60": tr60, "pct": pct,
                               "clpos": clpos, "rpos": rpos, "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                               "rng": hl / c, "rngrel": (hl / c) / (hl / c).rolling(20).mean()})
            # grid for 3-day
            df["g3"] = (np.arange(len(df)) % 3 == 0)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d["ex3"] = d["nxt3"] - d.groupby("coin")["nxt3"].transform("mean")
    d = d.dropna(subset=["nxt", "tr60", "pct"])
    d["trend"] = np.where(d.tr60 > 0.1, "rising", np.where(d.tr60 < -0.1, "falling", "choppy"))
    d["agit"] = np.where(d.pct > 0.5, "agitated", "calm")
    out = {}
    # close location fade: signal = 0.5 - clpos (long near low)
    d["cl_sig"] = 0.5 - d["clpos"]
    d["cl_pay"] = np.sign(d["cl_sig"]) * d["ex"]
    dc = d.dropna(subset=["cl_sig"])
    out["closeloc_fade_by_profile"] = dc.groupby(["trend", "agit"]).apply(lambda g: tday(g, "cl_pay"))
    dc2 = dc.copy(); dc2["cb"] = pd.cut(dc2.clpos, [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["closeloc_bins_calm"] = dc2[dc2.agit == "calm"].groupby("cb", observed=True).apply(lambda g: tday(g, "ex"))
    out["closeloc_bins_by_window_extremes"] = dc2[dc2.clpos.le(.2) | dc2.clpos.ge(.8)].assign(
        side=lambda x: np.where(x.clpos <= .2, "low", "high")).groupby(["w", "side"])["ex"].mean().unstack()*100
    # close loc x wide range (calm)
    dc2["wide"] = pd.qcut(dc2.rngrel, 3, labels=["narrow", "mid", "wide"])
    out["closeloc_fade_calm_by_width"] = dc2[dc2.agit == "calm"].groupby("wide", observed=True).apply(lambda g: tday(g, "cl_pay"))
    out["closeloc_fade_short_high_calm"] = dc2[(dc2.agit == "calm") & (dc2.clpos >= .8)].groupby("wide", observed=True).apply(lambda g: tday(g.assign(p=-g.ex), "p"))
    # brief theme: 20-day range position, 3-day, choppy calm
    g3 = d[d.g3].dropna(subset=["rpos", "nxt3"]).copy()
    g3["rb"] = pd.cut(g3.rpos, [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["rangepos20_3d_by_trend_agit"] = g3[g3.trend == "choppy"].groupby(["agit", "rb"], observed=True).apply(lambda g: tday(g, "ex3"))
    out["weekday_by_window_mon_tue"] = d[d.wd.isin([0, 1, 3])].groupby(["w", "wd"])["ex"].mean().unstack()*100
    return out
