def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    rows = []; pos = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values; n = len(c)
            s = pd.Series(c); r1 = s.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std().values
            ts = pd.to_datetime(df["timestamp"])
            al = df["postRebalance_current_allocation"].astype(float).values
            nxt = np.append(c[1:]/c[:-1]-1, np.nan)
            pos.append(pd.DataFrame(dict(coin=coin, al=al, nxt=nxt, fc=df["forecast"].astype(float).values)))
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, fwd=c[i+H]/c[i]-1, r1=r1.iloc[i], vol=vol20[i],
                                 r1z=r1.iloc[i]/vol20[i] if vol20[i]==vol20[i] and vol20[i]>0 else np.nan,
                                 wd=ts.iloc[i].dayofweek, fc=df["forecast"].iloc[i], year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean(); usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift); g["z"] = g["ex"]/g["coin"].map(usual)
    g["volr"] = g.groupby("coin")["vol"].rank(pct=True)
    g["volt"] = pd.cut(g["volr"], [0,1/3,2/3,1], labels=False, include_lowest=True)
    def slope(col, d):
        d = d.dropna(subset=[col,"z"])
        x = d.groupby("coin")[col].transform(lambda v:(v-v.mean())/v.std())
        r = stats.linregress(x, d["z"])
        return pd.Series(dict(slope=r.slope, t=r.slope/r.stderr, n=len(d)))
    out = {}
    calm = g[g.volt <= 1]
    out["r1_calm_by_coin"] = pd.DataFrame({c: slope("r1", calm[calm.coin==c]) for c in g.coin.unique()}).T
    out["r1_calm_by_year"] = pd.DataFrame({y: slope("r1", calm[calm.year==y]) for y in sorted(g.year.unique())}).T
    out["r1z_by_vol"] = pd.DataFrame({k: slope("r1z", g[g.volt==k]) for k in [0,1,2]}).T
    d = calm.dropna(subset=["r1"]).copy()
    d["b"] = d.groupby("coin")["r1"].transform(lambda v: pd.qcut(v.rank(method="first"),5,labels=False))
    a = d.groupby("b")["ex"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["r1_calm_quint_ex"] = a
    # weekday by year halves
    g["half"] = np.where(g.year <= 2021, "early", "late")
    g["monTue"] = g.wd.isin([0,1])
    a = g.groupby(["half","monTue"])["ex"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["montue_by_half"] = a
    # forecast slope by side
    out["fc_slope_pos"] = slope("fc", g[g.fc>0]); out["fc_slope_neg"] = slope("fc", g[g.fc<0])
    # book gain long vs short
    P = pd.concat(pos).dropna()
    P["gain"] = P.al*P.nxt
    P["side"] = np.where(P.al>0,"long",np.where(P.al<0,"short","flat"))
    cm = P.groupby("coin")["nxt"].mean()
    P["mkt"] = P.al*P.coin.map(cm)
    out["book_by_side"] = P.groupby("side")[["gain","mkt"]].agg(["mean","sum","count"])
    return out
