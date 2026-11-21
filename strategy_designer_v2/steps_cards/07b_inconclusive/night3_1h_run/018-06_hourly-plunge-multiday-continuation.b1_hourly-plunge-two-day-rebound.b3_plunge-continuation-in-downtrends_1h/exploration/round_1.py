import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [24, 48, 96, 192, 240]
    rows = []
    drift = {}
    usual = {}
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
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            ref = 0.0; last_cell = -1
            for t in range(n):
                if f[t] == 0:
                    ref = 0.0
                    continue
                if f[t] <= ref - 2:
                    cell = t // 96
                    ref = f[t]
                    if cell == last_cell:
                        continue
                    if t + 96 >= n:
                        continue
                    last_cell = cell
                    r = {"coin": coin, "window": w, "year": ts.iloc[t].year, "fc": f[t],
                         "ret30": c[t] / c[t - 720] - 1 if t >= 720 else np.nan,
                         "ret24": c[t] / c[t - 24] - 1 if t >= 24 else np.nan}
                    for h in H:
                        if t + h < n:
                            r[f"u{h}"] = -(c[t + h] / c[t] - 1 - drift[(coin, h)])
                            r[f"s{h}"] = r[f"u{h}"] / usual[(coin, h)]
                            r[f"tot{h}"] = -(c[t + h] / c[t] - 1)
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"u{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["tot96"] = g["tot96"].mean()
        return pd.Series(out)
    res = {}
    res["all"] = summ(d).to_frame().T
    res["by_coin"] = d.groupby("coin").apply(summ)
    res["by_year"] = d.groupby("year").apply(summ)
    d["fcbin"] = pd.cut(d["fc"], [-20.1, -19.9, -10, -5, 0])
    res["by_fc"] = d.groupby("fcbin").apply(summ)
    d["r30bin"] = pd.qcut(d["ret30"], 4)
    res["by_ret30"] = d.groupby("r30bin").apply(summ)
    d["r24bin"] = pd.qcut(d["ret24"], 4)
    res["by_ret24"] = d.groupby("r24bin").apply(summ)
    dd = d.dropna(subset=["ret30", "u96"])
    sl = stats.linregress(dd["ret30"], dd["u96"])
    res["slope_ret30"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(dd)}"
    dd = d.dropna(subset=["fc", "u96"])
    sl = stats.linregress(dd["fc"], dd["u96"])
    res["slope_fc"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(dd)}"
    res["strength96"] = d["s96"].mean()
    # window-level consistency
    wm = d.groupby(["coin", "window"])["u96"].mean()
    res["share_coinwindows_pos"] = float((wm > 0).mean())
    return res
