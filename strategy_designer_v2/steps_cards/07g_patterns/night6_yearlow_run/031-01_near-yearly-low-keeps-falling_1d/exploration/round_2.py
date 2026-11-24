import numpy as np, pandas as pd
from scipy import stats

def tstat(x):
    x = pd.Series(x).dropna()
    return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # weekday effect, cases of one day together (mean across coins per day)
    dd = []
    for c, ws in days.items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; t["win"] = w; dd.append(t)
    dd = pd.concat(dd)
    dd["day"] = pd.to_datetime(dd["day"])
    per_day = dd.groupby("day")[["coin_return","book_return"]].mean().reset_index()
    per_day["wd"] = per_day["day"].dt.weekday
    per_day["year"] = per_day["day"].dt.year
    out["weekday, per-day mean across coins"] = per_day.groupby("wd")["coin_return"].agg(
        ["count","mean", tstat])
    out["weekday diff Sat-other t (Welch)"] = float(stats.ttest_ind(
        per_day.loc[per_day.wd==5,"coin_return"].dropna(),
        per_day.loc[per_day.wd!=5,"coin_return"].dropna(), equal_var=False).statistic)
    sat = per_day[per_day.wd==5].groupby("year")["coin_return"].mean()
    oth = per_day[per_day.wd!=5].groupby("year")["coin_return"].mean()
    out["Saturday vs other by year"] = pd.DataFrame({"sat": sat, "other": oth, "diff": sat-oth})
    # per coin Saturday
    dd["wd"] = dd["day"].dt.weekday
    out["Saturday minus other, per coin"] = dd.groupby("coin").apply(
        lambda g: pd.Series({"sat": g.loc[g.wd==5,"coin_return"].mean(),
                             "other": g.loc[g.wd!=5,"coin_return"].mean(),
                             "t": stats.ttest_ind(g.loc[g.wd==5,"coin_return"].dropna(),
                                                  g.loc[g.wd!=5,"coin_return"].dropna(), equal_var=False).statistic}))
    # near-low x past 20d, graded, 20d and 10d grids, with day clustering
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            prox = b["debug_info.components.low_prox.last_history_value"].values
            past20 = pd.Series(cl).pct_change(20).values
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            for h in (10, 20):
                for i in range(0, n-h, h):
                    rows.append(dict(coin=c, h=h, prox=prox[i], past20=past20[i],
                                     fwd=cl[i+h]/cl[i]-1, day=ts[i]))
    df = pd.DataFrame(rows)
    df["ab"] = df["fwd"] - df.groupby(["coin","h"])["fwd"].transform("mean")
    for h in (10, 20):
        d = df[(df.h==h)].dropna(subset=["prox","past20"]).copy()
        d["pq"] = pd.qcut(d["prox"].rank(method="first"), 3, labels=["far","mid","near"])
        d["rq"] = pd.qcut(d["past20"].rank(method="first"), 3, labels=["down","flat","up"])
        g = d.groupby(["pq","rq"])["ab"]
        out[f"{h}d: prox tercile x past20 tercile"] = pd.DataFrame({"n": g.size(), "mean": g.mean(),
            "t_day": d.groupby(["pq","rq"]).apply(lambda x: tstat(x.groupby("day")["ab"].sum()))})
        # breaks: close at yearly low
        d["at_low"] = d["prox"] >= 0.99
        out[f"{h}d: at yearly low (prox>=0.99)"] = d.groupby("at_low")["ab"].agg(["count","mean", tstat])
        # interaction regression ab ~ prox_rank * past20_rank
        x1 = d["prox"].rank(pct=True); x2 = d["past20"].rank(pct=True)
        X = np.column_stack([np.ones(len(d)), x1, x2, x1*x2])
        y = d["ab"].values
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X@beta
        s2 = res@res/(len(y)-4)
        se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        out[f"{h}d: ab ~ prox_rank*past20_rank"] = pd.DataFrame({"beta": beta, "t": beta/se},
            index=["const","prox","past20","prox_x_past20"])
    return out
