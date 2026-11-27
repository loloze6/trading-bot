import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [2, 5, 10, 20]
    rows = []
    # drift per coin per horizon, non-overlapping grid over all windows
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs, ddof=1)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r = c.pct_change()
            sma = c.rolling(20).mean()
            vol = r.rolling(20).std()
            stretch = ((c - sma) / sma) / vol
            ret60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            agit = vol30 > vol30.rolling(365, min_periods=120).median()
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").astype(str)
            for h in H:
                for i in range(0, len(c) - h, 10):
                    if np.isnan(ret60.iloc[i]) or abs(ret60.iloc[i]) > 0.10: continue
                    s = stretch.iloc[i]
                    if np.isnan(s): continue
                    fr = c.iloc[i + h] / c.iloc[i] - 1 - drift[(coin, h)]
                    rows.append(dict(coin=coin, w=w, h=h, s=s, f=df["forecast"].iloc[i],
                                     un=fr, unz=fr / usual[(coin, h)], agit=bool(agit.iloc[i]),
                                     yr=day.iloc[i][:4], day=day.iloc[i], r60=ret60.iloc[i]))
    d = pd.DataFrame(rows)
    out = {}
    def slope(g):
        if len(g) < 10: return pd.Series(dict(n=len(g)))
        sl = stats.linregress(g["s"], g["un"])
        dirm = (np.sign(g["s"]) * g["un"])
        return pd.Series(dict(n=len(g), slope=sl.slope, t=sl.slope / sl.stderr,
                              dir_mean=dirm.mean(), dir_t=dirm.mean() / (dirm.std() / np.sqrt(len(g)))))
    out["by_h"] = d.groupby("h").apply(slope)
    d10 = d[d.h == 10].copy()
    d10["side"] = np.where(d10.s > 0, "above", "below")
    d10["q"] = pd.qcut(d10.s, 6, labels=False)
    out["q10_bucket"] = d10.groupby("q").agg(n=("un", "size"), s=("s", "mean"), un=("un", "mean"), unz=("unz", "mean"))
    for h in [5, 20]:
        dh = d[d.h == h].copy(); dh["q"] = pd.qcut(dh.s, 6, labels=False)
        out[f"q{h}_bucket"] = dh.groupby("q").agg(n=("un", "size"), s=("s", "mean"), un=("un", "mean"))
    out["by_side_h"] = d.assign(side=np.where(d.s > 0, "above", "below")).groupby(["h", "side"]).apply(slope)
    out["by_agit_h10"] = d10.groupby("agit").apply(slope)
    out["by_agit_side_h10"] = d10.groupby(["agit", "side"]).apply(slope)
    out["by_coin_h10"] = d10.groupby("coin").apply(slope)
    out["by_window_h10"] = d10.groupby("w").apply(slope)
    out["by_r60sign_h10"] = d10.groupby(np.sign(d10.r60)).apply(slope)
    out["corr_f_s"] = float(d10[["s", "f"]].corr().iloc[0, 1])
    return out
