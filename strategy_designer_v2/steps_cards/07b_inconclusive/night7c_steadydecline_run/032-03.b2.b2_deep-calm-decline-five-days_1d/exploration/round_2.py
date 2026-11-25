import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values.astype(float))
            v = pd.Series(df["volume"].values.astype(float))
            n = len(df)
            r28 = c / c.shift(28) - 1
            vol60 = c.pct_change().rolling(60, min_periods=20).std()
            vr = v.rolling(28).mean() / v.shift(28).rolling(90, min_periods=30).mean()
            fc = df["forecast"].values.astype(float)
            ts = df["timestamp"].astype(str)
            for H in [1, 3, 5]:
                for t in range(0, n - H, H):
                    rows.append(dict(coin=coin, w=w, H=H, fc=fc[t],
                                     ret=c.iloc[t+H]/c.iloc[t]-1, r28=r28.iloc[t],
                                     r28z=r28.iloc[t]/(vol60.iloc[t]*np.sqrt(28)) if vol60.iloc[t] > 0 else np.nan,
                                     vr=vr.iloc[t], day=ts.iloc[t][:10], year=ts.iloc[t][:4]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "H"])["ret"].transform("mean")
    d["un_s"] = -(d["ret"] - d["drift"])
    d["tot_s"] = -d["ret"]
    def tday(x):
        s = x.groupby("day")["un_s"].sum()
        return pd.Series(dict(n=len(x), days=len(s), mean=x["un_s"].mean(), tot=x["tot_s"].mean(),
                              t=s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s) > 2 else np.nan))
    out = {}
    cs = d[d.fc < 0].copy()
    c5 = cs[cs.H == 5].copy()
    out["cases_H5_by_year"] = c5.groupby("year").apply(tday)
    c5["vq"] = pd.qcut(c5["vr"].rank(method="first"), 3, labels=["lowest_vr", "mid_vr", "near1_vr"])
    out["cases_H5_by_volratio"] = c5.groupby("vq").apply(tday)
    lv = d[(d.vr < 1) & (d.r28 < 0)].copy()
    for H in [1, 3, 5]:
        x = lv[lv.H == H].dropna(subset=["r28z"]).copy()
        x["zq"] = pd.qcut(x["r28z"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "small"])
        out[f"lowvol_fall_by_volnormdepth_H{H}"] = x.groupby("zq").apply(tday)
        sl = stats.linregress(-x["r28z"], x["un_s"])
        out[f"slope_un_on_depthz_H{H}"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(x)}"
    c1 = cs[cs.H == 1].copy()
    c1["q"] = pd.qcut(c1["fc"].rank(method="first"), 4, labels=["deepest", "q2", "q3", "shallow"])
    out["cases_H1_by_fc_quartile"] = c1.groupby("q").apply(tday)
    return out
