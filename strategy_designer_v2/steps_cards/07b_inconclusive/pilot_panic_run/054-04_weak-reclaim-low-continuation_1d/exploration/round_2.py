import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10]
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
            ret = df["close"].pct_change()
            sw30 = ret.rolling(30).std()
            sw_rel = sw30 / sw30.expanding(30).median()
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
                                     near=near.iloc[i], depth=depth.iloc[i], tr60=tr60.iloc[i],
                                     swrel=sw_rel.iloc[i],
                                     unus=r - drift[(c, h)], tot=r,
                                     strength=(r - drift[(c, h)]) / usual[(c, h)]))
    d = pd.DataFrame(rows)
    def summ(g):
        dd = g.groupby("day")["unus"].sum()
        n = len(dd)
        t = dd.mean() / (dd.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(cases=len(g), days=n, mean_unus_long=g["unus"].mean(),
                              mean_tot=g["tot"].mean(), strength=g["strength"].mean(), t_day=t))
    d["trend"] = pd.cut(d["tr60"], [-9, -0.1, 0.1, 9], labels=["falling", "choppy", "rising"])
    d["agit"] = np.where(d["swrel"] > 1, "agit", "calm")
    out = {}
    out["trend_prof_h"] = d.groupby(["h", "trend", "inprof"]).apply(summ)
    out["trend_agit_h"] = d.groupby(["h", "trend", "agit"]).apply(summ)
    nf = d[(d.trend != "falling") & d.trend.notna()]
    out["notfalling_year_10"] = nf[nf.h == 10].groupby("year").apply(summ)
    out["notfalling_coin_10"] = nf[nf.h == 10].groupby("coin").apply(summ)
    for h in H:
        a = nf[nf.h == h].dropna(subset=["tr60"])
        out[f"spear_tr60_unus_notfalling_h{h}"] = float(stats.spearmanr(a["tr60"], a["unus"])[0])
        a2 = d[(d.h == h)].dropna(subset=["tr60"])
        out[f"spear_tr60_unus_all_h{h}"] = float(stats.spearmanr(a2["tr60"], a2["unus"])[0])
        p = d[(d.h == h) & d.inprof].dropna(subset=["near"])
        out[f"spear_near_unus_prof_h{h}"] = float(stats.spearmanr(p["near"], p["unus"])[0])
    d10 = d[d.h == 10].dropna(subset=["tr60"]).copy()
    d10["tq"] = pd.qcut(d10["tr60"], 4, labels=["q1low", "q2", "q3", "q4high"])
    out["tr60_quart_10"] = d10.groupby("tq").apply(summ)
    return out
