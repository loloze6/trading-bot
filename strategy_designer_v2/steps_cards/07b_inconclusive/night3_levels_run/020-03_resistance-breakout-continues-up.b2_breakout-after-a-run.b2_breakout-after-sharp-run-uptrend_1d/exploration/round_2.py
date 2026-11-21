import pandas as pd, numpy as np
from scipy import stats

def tt(x):
    x = pd.Series(x).dropna()
    return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

def explore(data):
    bars = data["bars"]
    rows = {5: [], 10: [], 20: []}
    usual = {}
    for coin, wins in bars.items():
        drift = {}; sd = {}
        for h in (5, 10, 20):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr); sd[h] = np.std(rr, ddof=1)
        usual[coin] = sd
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            r10 = pd.Series(c).pct_change(10).values
            r60 = pd.Series(c).pct_change(60).values
            r120 = pd.Series(c).pct_change(120).values
            for h in (5, 10, 20):
                lowest = 0.0; last_cell = -1
                for t in range(len(df)):
                    if f[t] <= 0:
                        lowest = 0.0
                        continue
                    if f[t] - lowest >= 2:
                        cell = t // h
                        if cell != last_cell:
                            last_cell = cell
                            if t + h < len(c):
                                u = c[t + h] / c[t] - 1 - drift[h]
                                rows[h].append(dict(coin=coin, year=ts[t].year, fc=f[t], r10=r10[t],
                                                    r60=r60[t], r120=r120[t], u=u, s=u / sd[h]))
                            lowest = f[t]
                    lowest = min(lowest, f[t])
    out = {}
    summ = []
    for h in (5, 10, 20):
        d = pd.DataFrame(rows[h])
        r = tt(d["u"]); r["strength"] = d["s"].mean(); r["h"] = h
        sl = stats.linregress(d["fc"], d["u"]); r["slope_t_fc"] = sl.slope / sl.stderr
        dd = d.dropna(subset=["r10"]); sl2 = stats.linregress(dd["r10"], dd["u"]); r["slope_t_r10"] = sl2.slope / sl2.stderr
        summ.append(r)
        d["r10_q"] = pd.qcut(d["r10"].rank(method="first"), 4, labels=False)
        out[f"h{h}_by_r10q"] = d.groupby("r10_q")["u"].apply(tt).unstack()
        out[f"h{h}_by_year"] = d.groupby("year")["u"].apply(tt).unstack()
        out[f"h{h}_by_coin"] = d.groupby("coin")["u"].apply(tt).unstack()
        d["r120_pos"] = np.where(d["r120"].isna(), "na", np.where(d["r120"] > 0, "pos", "neg"))
        out[f"h{h}_by_r120"] = d.groupby("r120_pos")["u"].apply(tt).unstack()
    out["summary"] = pd.DataFrame(summ)
    return out
