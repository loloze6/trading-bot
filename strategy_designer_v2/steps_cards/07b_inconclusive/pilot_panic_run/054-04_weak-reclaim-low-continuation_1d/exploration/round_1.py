import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            low30 = df["low"].rolling(30).min().shift(1)
            ev = (df["low"] < low30) & (df["close"] > low30)
            rng = (df["high"] - df["low"]).replace(0, np.nan)
            near = 1 - (df["close"] - low30) / rng
            depth = (low30 - df["low"]) / low30
            tr60 = df["close"] / df["close"].shift(60) - 1
            cl = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            for h in H:
                seen = set()
                for i in np.where(ev.values)[0]:
                    cell = i // h
                    if cell in seen or i + h >= len(cl):
                        continue
                    seen.add(cell)
                    r = cl[i + h] / cl[i] - 1
                    rows.append(dict(coin=c, win=w, h=h, year=ts[i].year, day=ts[i].normalize(),
                                     inprof=df["regime"].iloc[i] == "mean_reversion",
                                     regime=df["regime"].iloc[i],
                                     near=near.iloc[i], depth=depth.iloc[i],
                                     tr60=tr60.iloc[i],
                                     unus=r - drift[(c, h)], tot=r,
                                     strength=(r - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def summ(g):
        dd = g.groupby("day")["unus"].sum()
        n = len(dd)
        t = dd.mean() / (dd.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(cases=len(g), days=n, mean_unus_long=g["unus"].mean(),
                              mean_tot=g["tot"].mean(), strength=g["strength"].mean(), t_day=t))
    out = {}
    out["by_h_profile"] = d.groupby(["h", "inprof"]).apply(summ)
    d5 = d[d.h == 5].copy()
    out["regimes_5"] = d5.groupby("regime").apply(summ)
    d5["nq"] = pd.qcut(d5["near"], 3, labels=["far", "mid", "near"])
    out["near_terc_5_prof"] = d5.groupby(["inprof", "nq"]).apply(summ)
    d5["dq"] = pd.qcut(d5["depth"], 3, labels=["shallow", "mid", "deep"])
    out["depth_terc_5_prof"] = d5.groupby(["inprof", "dq"]).apply(summ)
    d5["trend"] = pd.cut(d5["tr60"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    out["trend_5"] = d5.groupby("trend").apply(summ)
    out["coin_5_prof"] = d5[d5.inprof].groupby("coin").apply(summ)
    out["year_5_prof"] = d5[d5.inprof].groupby("year").apply(summ)
    out["year_5_all"] = d5.groupby("year").apply(summ)
    p = d5[d5.inprof].dropna(subset=["near"])
    out["corr_near_unus_prof"] = float(stats.spearmanr(p["near"], p["unus"])[0])
    a = d5.dropna(subset=["near"])
    out["corr_near_unus_all"] = float(stats.spearmanr(a["near"], a["unus"])[0])
    out["corr_depth_unus_all"] = float(stats.spearmanr(a["depth"], a["unus"])[0])
    return out
