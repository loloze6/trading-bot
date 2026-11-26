import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H_list = [1, 3, 5, 10, 20]
    rows = []
    allret = {h: [] for h in H_list}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values; hi = df["high"].values
            n = len(df)
            prior_low = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            tr60 = pd.Series(c).pct_change(60).values * 100
            r = pd.Series(c).pct_change()
            vol30 = r.rolling(30).std()
            volpct = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True).values
            for h in H_list:
                for i in range(0, n - h, h):
                    allret[h].append(c[i + h] / c[i] - 1)
            for h in H_list:
                seen = set()
                for i in range(n - h):
                    if np.isnan(prior_low[i]):
                        continue
                    if lo[i] < prior_low[i] and c[i] >= prior_low[i]:
                        cell = i // h
                        if cell in seen:
                            continue
                        seen.add(cell)
                        depth = (prior_low[i] - lo[i]) / prior_low[i] * 100
                        clpos = (c[i] - lo[i]) / (hi[i] - lo[i]) if hi[i] > lo[i] else np.nan
                        rows.append(dict(coin=coin, w=w, h=h, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                         year=str(df["timestamp"].iloc[i])[:4],
                                         depth=depth, tr=tr60[i], volp=volpct[i], clpos=clpos,
                                         ret=c[i + h] / c[i] - 1))
    ev = pd.DataFrame(rows)
    drift = {h: np.mean(allret[h]) for h in H_list}
    sd = {h: np.std(allret[h], ddof=1) for h in H_list}
    ev["unus_short"] = -(ev["ret"] - ev["h"].map(drift))
    ev["prof"] = np.where(ev["tr"] > 10, "rising", np.where(ev["tr"] < -10, "falling", np.where(ev["tr"].isna(), "na", "choppy")))
    ev["agit"] = np.where(ev["volp"] > 0.5, "agit", np.where(ev["volp"].isna(), "na", "calm"))

    def summ(g):
        dd = g.groupby("day")["unus_short"].sum()
        m = g["unus_short"].mean()
        G = len(dd)
        se = np.sqrt((dd - dd.mean() * 0).pow(2).sum() * 0 + ((g.groupby("day")["unus_short"].apply(lambda x: (x - m).sum())) ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean_short=m, t=m / se if se > 0 else np.nan))

    out = {}
    out["drift_sd"] = pd.DataFrame({"drift": drift, "sd": sd})
    out["by_h_profile"] = ev.groupby(["h", "prof"]).apply(summ)
    r10 = ev[(ev.h == 10) & (ev.prof == "rising")].copy()
    out["rising10_by_coin"] = r10.groupby("coin").apply(summ)
    out["rising10_by_year"] = r10.groupby("year").apply(summ)
    out["rising10_by_agit"] = r10.groupby("agit").apply(summ)
    r10["dq"] = pd.qcut(r10["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["rising10_by_depth"] = r10.groupby("dq").apply(summ)
    r10["cq"] = pd.qcut(r10["clpos"].rank(method="first"), 3, labels=["lowclose", "midclose", "highclose"])
    out["rising10_by_closepos"] = r10.groupby("cq").apply(summ)
    for h in [5, 10, 20]:
        g = ev[(ev.h == h) & (ev.prof == "rising")]
        if len(g) > 5:
            out[f"slope_depth_h{h}"] = float(stats.linregress(g["depth"], g["unus_short"]).slope)
    allr = ev[ev.h == 10]
    out["all10_by_profagit"] = allr.groupby(["prof", "agit"]).apply(summ)
    return out
