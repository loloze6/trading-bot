import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            col = "debug_info.components.grind_fall.last_history_value"
            raw = df[col].values.astype(float) if col in df else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            lr = np.r_[np.nan, np.diff(np.log(c))]
            for i in range(0, n, 72):
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "f": f[i], "raw": raw[i]}
                r["fwd72"] = c[i+72]/c[i]-1 if i+72 < n else np.nan
                r["fwd168"] = c[i+168]/c[i]-1 if i+168 < n else np.nan
                r["past72"] = c[i]/c[i-72]-1 if i >= 72 else np.nan
                r["past720"] = c[i]/c[i-720]-1 if i >= 720 else np.nan
                if i >= 72:
                    x = lr[i-71:i+1]
                    loss = -x[x < 0]
                    if len(loss) > 3 and loss.sum() > 0:
                        r["myshare"] = 1 - np.sort(loss)[-3:].sum()/loss.sum()
                    else:
                        r["myshare"] = np.nan
                else:
                    r["myshare"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)
    for h in (72, 168):
        d["ex%d" % h] = d["fwd%d" % h] - d.groupby("coin")["fwd%d" % h].transform("mean")
    a = d[(d.f < 0) & d.fwd72.notna()].copy()
    a["gain"] = a.f/10*a.ex72
    def tm(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["f_dist"] = a.f.describe()
    out["gain_ex2018"] = tm(a[a.year != 2018].gain)
    out["ex72_ex2018"] = tm(a[a.year != 2018].ex72)
    a["share_q"] = pd.qcut(a.myshare, 5, labels=False)  # 4 = most grind
    out["share_q_ex72"] = a.groupby("share_q").agg(n=("ex72","size"), share=("myshare","mean"), ex72=("ex72","mean"), ex168=("ex168","mean"), past72=("past72","mean"))
    a["trend"] = np.sign(a.past720)
    dn = a[a.trend < 0]
    out["down30_share_q_ex72"] = dn.groupby(pd.qcut(dn.myshare, 3, labels=False)).ex72.apply(tm).unstack()
    up = a[a.trend > 0]
    out["up30_share_q_ex72"] = up.groupby(pd.qcut(up.myshare, 3, labels=False)).ex72.apply(tm).unstack()
    out["spearman_share_ex72"] = pd.Series(stats.spearmanr(a.myshare, a.ex72, nan_policy="omit")[:2], index=["rho","p"])
    out["spearman_share_ex72_down30"] = pd.Series(stats.spearmanr(dn.myshare, dn.ex72, nan_policy="omit")[:2], index=["rho","p"])
    out["spearman_past72_ex72"] = pd.Series(stats.spearmanr(a.past72, a.ex72, nan_policy="omit")[:2], index=["rho","p"])
    out["down30_by_year_ex72"] = dn.groupby("year").ex72.apply(tm).unstack()
    # all grid bars (any sign) by 30d trend
    b = d[d.fwd72.notna() & d.past720.notna()]
    out["allbars_ex72_by_30d"] = b.groupby(np.sign(b.past720)).ex72.apply(tm).unstack()
    out["spearman_past720_ex72_all"] = pd.Series(stats.spearmanr(b.past720, b.ex72)[:2], index=["rho","p"])
    return out
