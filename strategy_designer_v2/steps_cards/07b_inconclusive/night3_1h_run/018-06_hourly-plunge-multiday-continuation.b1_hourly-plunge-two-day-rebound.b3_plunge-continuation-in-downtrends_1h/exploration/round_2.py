import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [96, 192]
    rows = []; drift = {}; usual = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, df in ws.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"]); n = len(c)
            ref = 0.0; last_cell = -1
            for t in range(n):
                if f[t] == 0:
                    ref = 0.0; continue
                if f[t] <= ref - 2:
                    cell = t // 96; ref = f[t]
                    if cell == last_cell or t + 96 >= n: continue
                    last_cell = cell
                    r = {"coin": coin, "year": ts.iloc[t].year, "fc": f[t],
                         "ret30": c[t]/c[t-720]-1 if t >= 720 else np.nan,
                         "ret60": c[t]/c[t-1440]-1 if t >= 1440 else np.nan,
                         "ret7": c[t]/c[t-168]-1 if t >= 168 else np.nan}
                    if t >= 720:
                        r["vol30"] = np.mean(np.abs(c[t-720+24:t+1:24]/c[t-720:t-23:24]-1))
                    for h in H:
                        if t + h < n:
                            r[f"u{h}"] = -(c[t+h]/c[t]-1-drift[(coin, h)])
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"u{h}"] = x.mean(); out[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    nx = d[d["year"] != 2018]
    res["excl2018"] = summ(nx).to_frame().T
    res["2018_by_coin"] = d[d["year"] == 2018].groupby("coin").apply(summ)
    d["r60bin"] = pd.qcut(d["ret60"], 4)
    res["by_ret60"] = d.groupby("r60bin").apply(summ)
    d["r60neg"] = d["ret60"] < 0
    res["by_ret60neg"] = d.dropna(subset=["ret60"]).groupby("r60neg").apply(summ)
    d["vbin"] = pd.qcut(d["vol30"], 4)
    res["by_vol30"] = d.groupby("vbin").apply(summ)
    d["r7bin"] = pd.qcut(d["ret7"], 4)
    res["by_ret7"] = d.groupby("r7bin").apply(summ)
    dd = d.dropna(subset=["ret60", "u96"])
    sl = stats.linregress(dd["ret60"], dd["u96"])
    res["slope_ret60"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(dd)}"
    dd = nx.dropna(subset=["ret30", "u96"])
    sl = stats.linregress(dd["ret30"], dd["u96"])
    res["slope_ret30_excl2018"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(dd)}"
    return res
