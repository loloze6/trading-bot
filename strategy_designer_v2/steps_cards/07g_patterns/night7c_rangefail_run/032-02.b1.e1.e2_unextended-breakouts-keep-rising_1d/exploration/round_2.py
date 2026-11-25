import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    def rows_for(h, lb=60):
        rows = []
        for coin, ws in bars.items():
            allr = []
            for w, df in ws.items():
                c = df["close"].values
                for i in range(0, len(c)-h, h):
                    allr.append(c[i+h]/c[i]-1)
            mu = np.mean(allr); sd = np.std(allr, ddof=1)
            for w, df in ws.items():
                c = df["close"].reset_index(drop=True)
                ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
                mxp = c.shift(1).rolling(lb, min_periods=lb).max()
                mnp = c.shift(1).rolling(lb, min_periods=lb).min()
                mx = c.rolling(lb, min_periods=lb).max()
                mn = c.rolling(lb, min_periods=lb).min()
                pos = (c-mn)/(mx-mn)
                for i in range(0, len(c)-h, h):
                    if pd.isna(mxp[i]): continue
                    rows.append(dict(coin=coin, w=w, yr=ts[i].year, ex=(c[i+h]/c[i]-1-mu)/sd,
                                     exraw=c[i+h]/c[i]-1-mu, fwd=c[i+h]/c[i]-1,
                                     dhi=np.log(c[i]/mxp[i]), pos=pos[i]))
        return pd.DataFrame(rows)
    def qtab(d, col, y="ex", q=5):
        d = d.dropna(subset=[col, y]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        g = d.groupby("q")[y].agg(["mean","count","std"])
        g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
        g["xmean"] = d.groupby("q")[col].mean()
        r, p = stats.spearmanr(d[col], d[y]); g.loc["rho"] = [r, len(d), p, np.nan, np.nan]
        return g.round(4)
    for h in (5, 10, 20):
        d = rows_for(h)
        out[f"h{h} by range position (0 low,1 high)"] = qtab(d, "pos")
        if h == 10:
            d10 = d
    # robustness of position effect on h10: by year, by coin, spearman
    res = []
    for k, g in d10.groupby("yr"):
        r, p = stats.spearmanr(g["pos"], g["ex"]); res.append(("yr", k, r, len(g), np.mean(g.loc[g.pos>=g.pos.quantile(0.8),"exraw"])))
    for k, g in d10.groupby("coin"):
        r, p = stats.spearmanr(g["pos"], g["ex"]); res.append(("coin", k, r, len(g), np.mean(g.loc[g.pos>=g.pos.quantile(0.8),"exraw"])))
    out["h10 spearman pos vs ex, by year and coin (last: top-quintile mean excess)"] = pd.DataFrame(res, columns=["by","k","rho","n","topq_exraw"]).round(4)
    d5 = rows_for(5)
    top = d5[d5.pos >= 0.8]; mid = d5[(d5.pos > 0.2) & (d5.pos < 0.8)]
    t = stats.ttest_ind(top["exraw"], mid["exraw"], equal_var=False)
    out["h5 top(pos>=.8) minus mid exraw"] = pd.Series({"top_mean": top.exraw.mean(), "n_top": len(top), "mid_mean": mid.exraw.mean(), "n_mid": len(mid), "welch_t": t.statistic}).round(4)
    # weekday by year
    dl = []
    for coin, ws in days.items():
        for w, df in ws.items():
            d = df.dropna(subset=["coin_return"]).copy()
            dd = pd.to_datetime(d["day"]); d["wd"] = dd.dt.dayofweek; d["yr"] = dd.dt.year; d["coin"] = coin
            dl.append(d)
    D = pd.concat(dl)
    D["frisat"] = D.wd.isin([4,5])
    rr = []
    for k, g in D.groupby("yr"):
        a = g.loc[g.frisat, "coin_return"]; b = g.loc[~g.frisat, "coin_return"]
        rr.append((k, a.mean(), b.mean(), len(a), stats.ttest_ind(a, b, equal_var=False).statistic))
    out["Fri+Sat minus other days by year"] = pd.DataFrame(rr, columns=["yr","frisat","other","n_fs","t"]).round(5)
    rr = []
    for k, g in D.groupby("coin"):
        a = g.loc[g.frisat, "coin_return"]; b = g.loc[~g.frisat, "coin_return"]
        rr.append((k, a.mean(), b.mean(), stats.ttest_ind(a, b, equal_var=False).statistic))
    out["Fri+Sat minus other days by coin"] = pd.DataFrame(rr, columns=["coin","frisat","other","t"]).round(5)
    return out
