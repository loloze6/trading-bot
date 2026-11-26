import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 20
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            n = len(df)
            for i in range(0, n - H, H):
                lo = np.nanmin(c[max(0, i-364):i+1])
                rows.append(dict(coin=coin, w=w, i=i, ret=c[i+H]/c[i]-1, af=abs(f[i]),
                                 dist=c[i]/lo-1))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby("coin")["ret"].transform("mean")
    d["sg"] = -(d["ret"] - d["drift"])
    out = {}
    # window-demeaned slope (removes the market's own per-window move)
    d["sg_wd"] = d["sg"] - d.groupby(["coin", "w"])["sg"].transform("mean")
    r = stats.linregress(d["af"], d["sg"]); out["pooled_slope_t"] = r.slope / r.stderr
    r2 = stats.linregress(d["af"], d["sg_wd"]); out["within_coin_window_slope_t"] = r2.slope / r2.stderr
    out["within_coin_window_slope"] = r2.slope
    # top fifth spread
    thr = d["af"].quantile(0.8)
    d["top"] = d["af"] >= thr
    def tstat(x):
        return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    out["top_by_coin"] = d[d.top].groupby("coin")["sg"].agg(["size", "mean", tstat])
    out["top_by_window"] = d[d.top].groupby("w")["sg"].agg(["size", "mean"])
    out["top_share_windows_positive"] = (d[d.top].groupby("w")["sg"].mean() > 0).mean()
    # distance buckets
    d["db"] = pd.cut(d["dist"], [-0.001, 0.02, 0.05, 0.10, 0.25, 0.5, 1, np.inf])
    out["by_distance"] = d.groupby("db")["sg"].agg(["size", "mean", tstat])
    # top fifth vs rest, within coin-window
    out["top_minus_rest_withinCW"] = pd.Series(dict(
        top=d.loc[d.top, "sg_wd"].mean(), rest=d.loc[~d.top, "sg_wd"].mean(),
        t=stats.ttest_ind(d.loc[d.top, "sg_wd"], d.loc[~d.top, "sg_wd"], equal_var=False).statistic))
    out["pooled_top_minus_rest"] = pd.Series(dict(
        diff=d.loc[d.top, "sg"].mean() - d.loc[~d.top, "sg"].mean(),
        t=stats.ttest_ind(d.loc[d.top, "sg"], d.loc[~d.top, "sg"], equal_var=False).statistic))
    return out
