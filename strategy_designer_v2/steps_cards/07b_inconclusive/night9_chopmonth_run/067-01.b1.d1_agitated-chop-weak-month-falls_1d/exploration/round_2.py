import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    H = [1, 2, 3, 5, 7]
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            for i in range(0, len(c), 7):
                if not (f[i] < 0):
                    continue
                r = {"coin": coin, "win": w, "fc": f[i]}
                for h in H:
                    if i + h < len(c):
                        r[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[(coin, h)])
                rows.append(r)
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "median": x.median(), "share_pos": (x > 0).mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["u7_all"] = tt(d["u7"])
    out["u7_without_w16"] = tt(d.loc[d.win != "w16", "u7"])
    x = d[d.win != "w16"].dropna(subset=["u7"])
    sl = stats.linregress(x["fc"], x["u7"])
    out["slope_t_u7_on_fc_without_w16"] = float(sl.slope / sl.stderr)
    out["short_horizons"] = pd.DataFrame({h: tt(d[f"u{h}"]) for h in H}).T
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["fc_tercile_without_w16"] = d[d.win != "w16"].groupby("fq").apply(lambda g: tt(g["u7"]))
    out["leave_one_window_out_mean_u7"] = pd.Series({w: d.loc[d.win != w, "u7"].mean() for w in d.win.unique()})
    return out
