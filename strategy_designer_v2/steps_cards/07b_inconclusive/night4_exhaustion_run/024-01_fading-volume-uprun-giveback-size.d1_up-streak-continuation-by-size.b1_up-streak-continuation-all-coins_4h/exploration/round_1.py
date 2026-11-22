import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 18
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        rets = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        rets = np.array(rets)
        drift[coin] = np.nanmean(rets); usual[coin] = np.nanstd(rets)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            # streak length (up)
            sl = np.zeros(n, int)
            for i in range(1, n):
                sl[i] = sl[i-1] + 1 if r1[i] > 0 else 0
            low = f[0]; seen = set()
            for i in range(n):
                if f[i] - low >= 2:
                    low = f[i]
                    cell = i // H
                    if cell not in seen:
                        seen.add(cell)
                        L = sl[i]
                        volfade = np.nan
                        if L >= 2:
                            seg = v[i-L+1:i+1]
                            volfade = seg[-1] / np.mean(seg[:-1]) - 1
                        pre30 = c[i] / c[i-180] - 1 if i >= 180 else np.nan
                        out = {}
                        for h in (3, 6, 12, 18, 36):
                            out[f"r{h}"] = c[i+h] / c[i] - 1 if i + h < n else np.nan
                        rows.append(dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                         f=f[i], L=L, volfade=volfade, pre30=pre30, **out))
                else:
                    low = min(low, f[i])
    d = pd.DataFrame(rows)
    d["drift"] = d["coin"].map(drift)
    d["u"] = d["r18"] - d["drift"]
    def summ(g):
        x = g["u"].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    res = {}
    res["overall"] = summ(d).to_frame().T
    for h in (3, 6, 12, 18, 36):
        dr = d["drift"] * h / 18
        x = (d[f"r{h}"] - dr).dropna()
        res.setdefault("by_horizon", []).append({"h_bars": h, "n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    res["by_horizon"] = pd.DataFrame(res["by_horizon"])
    res["by_coin"] = d.groupby("coin").apply(summ)
    res["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 5, labels=False)
    res["by_forecast_quintile"] = d.groupby("fq").apply(summ).join(d.groupby("fq")["f"].mean())
    d["Lb"] = pd.cut(d["L"], [-1, 1, 2, 3, 4, 6, 100])
    res["by_streak_len"] = d.groupby("Lb").apply(summ)
    vv = d.dropna(subset=["volfade"]).copy()
    vv["vq"] = pd.qcut(vv["volfade"].rank(method="first"), 5, labels=False)
    res["by_volfade_quintile(low=fading)"] = vv.groupby("vq").apply(summ).join(vv.groupby("vq")["volfade"].mean())
    pp = d.dropna(subset=["pre30"]).copy()
    pp["pq"] = pd.qcut(pp["pre30"].rank(method="first"), 5, labels=False)
    res["by_prior30d_ret_quintile"] = pp.groupby("pq").apply(summ).join(pp.groupby("pq")["pre30"].mean())
    res["drift_usual_mean"] = pd.DataFrame({"drift": pd.Series(drift), "usual": pd.Series(usual)}).mean().to_frame().T
    return res
