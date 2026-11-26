import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    sdall = {}
    for coin, wins in bars.items():
        allsd = []
        for w, b in wins.items():
            r = b["close"].astype(float).reset_index(drop=True).pct_change()
            allsd.append(r.rolling(30, min_periods=30).std())
        sdall[coin] = pd.concat(allsd).median()
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=30).std()
            z = r / sd
            tr = c / c.shift(60) - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year
            fwd = c.shift(-5) / c - 1
            for i in range(0, len(b), 5):
                rows.append(dict(coin=coin, w=w, year=yr[i], z=z[i], fwd=fwd[i], sd=sd[i],
                                 agit=(sd[i] > sdall[coin]) if pd.notna(sd[i]) else np.nan,
                                 tr=tr[i], day=pd.to_datetime(b["timestamp"].iloc[i]).normalize()))
    G = pd.DataFrame(rows)
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["un"] = G["fwd"] - G["drift"]
    G["uns"] = G["un"] / G.groupby("coin")["fwd"].transform("std")
    G = G.dropna(subset=["z", "un", "agit"])
    U = G[G.z > 0].copy()
    U["trend"] = pd.cut(U.tr, [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    U["zbin"] = pd.cut(U.z, [0, 0.5, 1, 1.5, 2, 99], labels=["0-0.5", "0.5-1", "1-1.5", "1.5-2", ">2"])
    out = {}
    def summ(g):
        n = len(g)
        if n < 5: return pd.Series(dict(n=n))
        sl = stats.linregress(g.z, g.un) if g.z.nunique() > 2 else None
        d = g.groupby("day")["un"].sum()
        D = len(d)
        se = np.sqrt((d ** 2).sum() * D / (D - 1)) / n
        return pd.Series(dict(n=n, un=g.un.mean(), t_daypooled=g.un.mean() / se, strength=g.uns.mean(),
                              slope=sl.slope if sl else np.nan,
                              t_slope=sl.slope / sl.stderr if sl else np.nan))
    out["up days by agitation"] = U.groupby("agit").apply(summ)
    out["up days by zbin x agit"] = U.groupby(["agit", "zbin"]).apply(summ)
    out["calm up days by year"] = U[U.agit == False].groupby("year").apply(summ)
    out["agitated up days by year"] = U[U.agit == True].groupby("year").apply(summ)
    out["calm up days by trend"] = U[U.agit == False].groupby("trend").apply(summ)
    out["calm up days by coin"] = U[U.agit == False].groupby("coin").apply(summ)
    # down days in calm, mirror (continuation down = negative slope sign on z)
    Dn = G[(G.z < 0) & (G.agit == False)]
    out["calm down days"] = summ(Dn).to_frame().T
    return out
