import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            v = df["volume"].values
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std().values
            volr = (pd.Series(v) / pd.Series(v).rolling(20).mean()).values
            ts = pd.to_datetime(df["timestamp"])
            rp = df.get("debug_info.components.range_pos.last_history_value")
            for i in range(0, n - 7, 7):
                rows.append(dict(coin=coin, w=w, fwd=c[i+7]/c[i]-1,
                    p7=c[i]/c[i-7]-1 if i>=7 else np.nan,
                    p30=c[i]/c[i-30]-1 if i>=30 else np.nan,
                    vol=vol20[i], volr=volr[i], reg=df["regime"].iloc[i],
                    fc=df["forecast"].iloc[i], rp=rp.iloc[i] if rp is not None else np.nan,
                    alloc=df["postRebalance_current_allocation"].iloc[i],
                    year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def summ(grp):
        x = grp["ex"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))
    out = {}
    out["by_regime"] = g.groupby("reg").apply(summ)
    for col in ["p7","p30","vol","volr","rp"]:
        gg = g.dropna(subset=[col]).copy()
        gg["q"] = gg.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["by_"+col+"_quint"] = gg.groupby("q").apply(summ)
    out["by_coin_fc>0"] = g[g.fc>0].groupby("coin").apply(summ)
    out["by_coin_fc0"] = g[g.fc<=0].groupby("coin").apply(summ)
    out["by_year_fc>0"] = g[g.fc>0].groupby("year").apply(summ)
    # p30 quintile inside trending vs unknown
    gg = g.dropna(subset=["p30"]).copy()
    gg["q"] = gg.groupby("coin")["p30"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["p30q_x_regime"] = gg.groupby(["reg","q"]).apply(summ)
    # daily: next-day return by today's return quintile, weekday
    drows=[]
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.reset_index(drop=True)
            cr = d["coin_return"]
            drows.append(pd.DataFrame(dict(coin=coin, r=cr, nxt=cr.shift(-1), br=d["book_return"],
                wd=pd.to_datetime(d["day"]).dt.dayofweek, year=pd.to_datetime(d["day"]).dt.year)))
    D = pd.concat(drows)
    D["z"] = D["r"]/D.groupby("coin")["r"].transform("std")
    Dd = D.dropna(subset=["r","nxt"]).copy()
    Dd["q"] = Dd.groupby("coin")["r"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    def s2(x):
        x=x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x)))))
    out["nextday_by_today_quint"] = Dd.groupby("q")["nxt"].apply(s2).unstack()
    out["coinret_by_weekday"] = D.groupby("wd")["r"].apply(s2).unstack()
    out["bookret_by_weekday"] = D.groupby("wd")["br"].apply(s2).unstack()
    out["book_by_year"] = D.groupby("year")["br"].apply(s2).unstack()
    out["book_by_coin"] = D.groupby("coin")["br"].apply(s2).unstack()
    return out
