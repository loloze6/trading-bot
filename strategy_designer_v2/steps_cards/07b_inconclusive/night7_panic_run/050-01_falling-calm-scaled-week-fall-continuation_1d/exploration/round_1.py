import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    hs = [1, 3, 5, 7, 10]
    # drift per coin per horizon, non-overlapping
    drift = {}
    for coin, ws in bars.items():
        for h in hs:
            r = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                r += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(r)
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            lr = np.log(df["close"]).diff()
            sd30 = lr.rolling(30).std().values
            r7 = df["close"].pct_change(7).values
            inprof = (df["regime"] == "unknown").values
            fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in hs:
                for i in range(0, len(c) - h, h):
                    if not inprof[i] or np.isnan(r7[i]) or np.isnan(sd30[i]):
                        continue
                    ret = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], day=day[i], fc=fc[i],
                                     z=r7[i] / (sd30[i] * np.sqrt(7)), ex=ret - drift[(coin, h)]))
    d = pd.DataFrame(rows)
    out = {}
    def summ(g):
        n = len(g); m = g["sex"].mean()
        dd = g.groupby("day")["sex"].sum() - 0
        # day-clustered t
        gm = g.groupby("day")["sex"].sum()
        se = np.sqrt(((g.groupby("day")["sex"].apply(lambda s: (s - m).sum())) ** 2).sum()) / n if n > 1 else np.nan
        return pd.Series(dict(n=n, days=g["day"].nunique(), mean=m, t=m / se if se else np.nan))
    fall = d[d["z"] < 0].copy(); fall["sex"] = -fall["ex"]
    rise = d[d["z"] > 0].copy(); rise["sex"] = fall["ex"].mean() * 0 + rise["ex"]
    out["fall_by_h"] = fall.groupby("h").apply(summ)
    out["rise_by_h_long"] = rise.groupby("h").apply(summ)
    f3 = fall[fall.h == 3].copy()
    f3["q"] = pd.qcut(f3["z"], 4, labels=["q1_largest", "q2", "q3", "q4_smallest"])
    out["fall3_by_zq"] = f3.groupby("q").apply(summ)
    out["fall3_by_coin"] = f3.groupby("coin").apply(summ)
    out["fall3_by_window"] = f3.groupby("w").apply(summ)
    out["fall3_by_year"] = f3.groupby("yr").apply(summ)
    f7 = fall[fall.h == 7].copy()
    f7["q"] = pd.qcut(f7["z"], 4, labels=["q1_largest", "q2", "q3", "q4_smallest"])
    out["fall7_by_zq"] = f7.groupby("q").apply(summ)
    r3 = rise[rise.h == 3].copy()
    r3["q"] = pd.qcut(r3["z"], 4, labels=["q1_smallest", "q2", "q3", "q4_largest"])
    out["rise3_by_zq"] = r3.groupby("q").apply(summ)
    out["slope_fall_by_h"] = fall.groupby("h").apply(lambda g: pd.Series(dict(zip(["slope","t"], [stats.linregress(-g.z, g.sex).slope, stats.linregress(-g.z, g.sex).slope/stats.linregress(-g.z, g.sex).stderr]))))
    return out
