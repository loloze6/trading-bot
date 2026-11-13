def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allfwd = []
        tmp = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values)
            fwd = (c.shift(-10) / c - 1).values
            allfwd.append(fwd[~np.isnan(fwd)])
            sma200 = c.rolling(200, min_periods=50).mean().values
            f = b["forecast"].values
            since = np.full(len(b), np.nan); cnt = np.nan
            for i in range(len(b)):
                if f[i] < 0:
                    cnt = 0 if (i == 0 or not f[i-1] < 0 or np.isnan(cnt)) else cnt + 1
                    if i == 0: cnt = np.nan
                else:
                    cnt = np.nan
                since[i] = cnt
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D")
            for i in range(len(b)):
                if np.isnan(fwd[i]): continue
                tmp.append(dict(coin=coin, win=w, ts=ts.iloc[i], idx=i, f=f[i], fwd=fwd[i],
                                below200=c.iloc[i] < sma200[i] if not np.isnan(sma200[i]) else np.nan,
                                since=since[i], year=ts.iloc[i].year))
        hold = np.mean(np.concatenate(allfwd))
        for r in tmp:
            r["hold"] = hold; rows.append(r)
    d = pd.DataFrame(rows)
    mkt = d.groupby("ts")["fwd"].mean().rename("mkt")
    d = d.join(mkt, on="ts")
    btc = d[d.coin == "BTCUSD"].set_index("ts")
    d = d.join(btc["f"].rename("btc_f"), on="ts").join(btc["fwd"].rename("btc_fwd"), on="ts")
    d["ex"] = -(d["fwd"] - d["hold"])
    d["ex_mkt"] = -(d["fwd"] - d["mkt"])
    s = d[(d.f < 0) & (d.idx % 10 == 0)].copy()
    s["w"] = s.f.abs()
    def agg(g, col="ex"):
        w = g["w"]; x = g[col]; m = (w*x).sum()/w.sum(); n = len(g)
        se = np.sqrt((w**2*(x-m)**2).sum()*n/max(n-1,1))/w.sum()
        return pd.Series(dict(n=n, wmean=m, t=m/se if se > 0 else np.nan, hit=(x > 0).mean()))
    out = {}
    out["ex_vs_hold"] = agg(s).to_frame().T
    out["ex_vs_mkt_xsec"] = agg(s, "ex_mkt").to_frame().T
    out["mkt_var_share"] = pd.Series(dict(corr_fwd_mkt=s[["fwd","mkt"]].corr().iloc[0,1],
                                          r2=s[["fwd","mkt"]].corr().iloc[0,1]**2))
    out["ex_mkt_by_year"] = s.groupby("year").apply(lambda g: agg(g, "ex_mkt"))
    s["age"] = pd.cut(s["since"], [-1, 20, 60, 150, 10000], labels=["0-20","21-60","61-150",">150"])
    out["by_age"] = s.groupby("age").apply(agg)
    out["by_age_mkt"] = s.groupby("age").apply(lambda g: agg(g, "ex_mkt"))
    out["by_below200"] = s.groupby("below200").apply(agg)
    s["btc_state"] = np.where(s.btc_f < 0, "btc_short", "btc_flat")
    out["by_btc_state"] = s[s.coin != "BTCUSD"].groupby("btc_state").apply(agg)
    out["by_btc_state_mkt"] = s[s.coin != "BTCUSD"].groupby("btc_state").apply(lambda g: agg(g, "ex_mkt"))
    s["bdir"] = np.where(s.btc_fwd < 0, "btc_fell", "btc_rose")
    out["by_btc_fwd_dir"] = s.groupby("bdir").apply(agg)
    return out
