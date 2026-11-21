def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 168
    rows = []
    for coin, wins in bars.items():
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rr.extend(list(c[idx + H] / c[idx] - 1))
        rr = np.array(rr); dr, sd = rr.mean(), rr.std()
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            hi = df["high"].values
            n = len(c); low = 0.0; seen = set()
            for i in range(n):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cell = i // H; low = f[i]
                    if cell in seen: continue
                    seen.add(cell)
                    if i + H >= n: continue
                    r = {"coin": coin, "fc": f[i], "u": c[i+H]/c[i]-1-dr, "z": (c[i+H]/c[i]-1-dr)/sd}
                    r["ret2160"] = c[i]/c[i-2160]-1 if i >= 2160 else np.nan
                    r["ret1440"] = c[i]/c[i-1440]-1 if i >= 1440 else np.nan
                    r["near_hi"] = c[i]/hi[max(0, i-720):i+1].max() if i >= 720 else np.nan
                    r["ret168"] = c[i]/c[i-168]-1 if i >= 168 else np.nan
                    rows.append(r)
                else:
                    low = min(low, f[i])
    d = pd.DataFrame(rows)

    def summ(g):
        x = g["u"].dropna()
        s = pd.Series({"n": len(x), "mean%": 100*x.mean(),
                       "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
        gg = g.dropna(subset=["u", "ret168"])
        if len(gg) > 10:
            sl = np.polyfit(gg["ret168"], gg["u"], 1)[0]
            s["slope_u_on_wk"] = sl
            s["corr"] = np.corrcoef(gg["ret168"], gg["u"])[0, 1]
        return s
    out = {}
    d["t90"] = np.where(d["ret2160"].isna(), "na", np.where(d["ret2160"] > 0, "90d_up", "90d_down"))
    out["by_90d"] = d.groupby("t90").apply(summ)
    d["t60"] = np.where(d["ret1440"].isna(), "na", np.where(d["ret1440"] > 0, "60d_up", "60d_down"))
    out["by_60d"] = d.groupby("t60").apply(summ)
    d["nh"] = pd.qcut(d["near_hi"], 4, labels=["far", "q2", "q3", "at_high"])
    out["by_near_30d_high"] = d.groupby("nh").apply(summ)
    out["all"] = summ(d).to_frame().T
    d["r90q"] = pd.qcut(d["ret2160"], 4, labels=["q1", "q2", "q3", "q4"])
    out["by_90d_quartile"] = d.groupby("r90q").apply(summ)
    return out
