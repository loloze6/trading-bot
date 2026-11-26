import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows30, rows7, rows1 = [], [], []
    drift30, drift7 = {}, {}
    # normal drift per coin (non-overlapping grid over all windows)
    for coin, wins in bars.items():
        f30, f7 = [], []
        for w, df in wins.items():
            c = df["close"].reset_index(drop=True)
            for h, lst in ((30, f30), (7, f7)):
                for p in range(0, len(c) - h, h):
                    lst.append(c[p + h] / c[p] - 1)
        drift30[coin] = np.mean(f30); drift7[coin] = np.mean(f7)
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"]
            lr = np.log(c).diff()
            vol30 = lr.rolling(30).std()
            r30 = c / c.shift(30) - 1
            r7 = c / c.shift(7) - 1
            r1 = c.pct_change()
            reg = d["regime"]
            fv = d.get("debug_info.components.fall90.last_history_value")
            yr = pd.to_datetime(d["timestamp"]).dt.year
            for p in range(0, len(c) - 30, 30):
                rows30.append(dict(coin=coin, win=w, year=yr[p], fwd=c[p+30]/c[p]-1-drift30[coin],
                                   z30=r30[p]/(vol30[p]*np.sqrt(30)) if vol30[p] > 0 else np.nan,
                                   r30=r30[p], r7=r7[p], vol=vol30[p], reg=reg[p],
                                   f90=fv[p] if fv is not None else np.nan))
            for p in range(0, len(c) - 7, 7):
                rows7.append(dict(coin=coin, fwd=c[p+7]/c[p]-1-drift7[coin],
                                  z7=r7[p]/(vol30[p]*np.sqrt(7)) if vol30[p] > 0 else np.nan,
                                  z30=r30[p]/(vol30[p]*np.sqrt(30)) if vol30[p] > 0 else np.nan,
                                  vol=vol30[p], reg=reg[p]))
            wd = pd.to_datetime(d["timestamp"]).dt.dayofweek
            for p in range(1, len(c)):
                rows1.append(dict(wd=wd[p], r=r1[p]))
    A = pd.DataFrame(rows30); B = pd.DataFrame(rows7); C = pd.DataFrame(rows1)
    def summ(g):
        return pd.Series(dict(n=len(g), mean=g["fwd"].mean(),
                              t=g["fwd"].mean()/(g["fwd"].std()/np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out = {}
    a = A.dropna(subset=["z30"]).copy()
    a["q"] = pd.qcut(a["z30"], 5, labels=False)
    out["fwd30 excess by past30 z quintile"] = a.groupby("q").apply(summ)
    out["spearman z30 vs fwd30"] = str(stats.spearmanr(a["z30"], a["fwd"]))
    a["vq"] = a.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["fwd30 excess by vol tercile (within coin)"] = a.groupby("vq").apply(summ)
    b = B.dropna(subset=["z7"]).copy()
    b["q"] = pd.qcut(b["z7"], 5, labels=False)
    out["fwd7 excess by past7 z quintile"] = b.groupby("q").apply(summ)
    b2 = B.dropna(subset=["z30"]).copy(); b2["q"] = pd.qcut(b2["z30"], 5, labels=False)
    out["fwd7 excess by past30 z quintile"] = b2.groupby("q").apply(summ)
    r = A[A["reg"] == "mean_reversion"].copy()
    out["in-regime n"] = len(r)
    if len(r) > 5:
        r["r30q"] = pd.qcut(r["r30"], 3, labels=False, duplicates="drop")
        out["in-regime fwd30 by past r30 tercile"] = r.groupby("r30q").apply(summ)
        r["fq"] = pd.qcut(r["f90"], 3, labels=False, duplicates="drop")
        out["in-regime fwd30 by fall90 tercile(0=deepest)"] = r.groupby("fq").apply(summ)
        r["r7q"] = pd.qcut(r["r7"], 3, labels=False, duplicates="drop")
        out["in-regime fwd30 by past r7 tercile"] = r.groupby("r7q").apply(summ)
    out["fwd30 excess by year"] = A.groupby("year").apply(summ)
    out["daily return by weekday"] = C.groupby("wd")["r"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(s.count()))])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    T = pd.concat(tr)
    T["eq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 3, labels=False)
    out["trades by entry forecast tercile"] = T.groupby("eq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    return out
