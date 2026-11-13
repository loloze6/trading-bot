def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        allfwd = []
        tmp = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            fwd = pd.Series(c).shift(-10).values / c - 1
            allfwd.append(fwd[~np.isnan(fwd)])
            ret200 = pd.Series(c).pct_change(60).values
            raw = b["debug_info.components.sma_cross_down.last_history_value"].values
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b), 10):
                if np.isnan(fwd[i]): continue
                tmp.append(dict(coin=coin, win=w, year=ts.iloc[i].year, f=b["forecast"].iloc[i],
                                fwd=fwd[i], raw=raw[i], mom60=ret200[i]))
        hold = np.mean(np.concatenate(allfwd))
        for r in tmp:
            r["hold"] = hold
            rows.append(r)
    d = pd.DataFrame(rows)
    d["ex"] = -(d["fwd"] - d["hold"])
    s = d[d["f"] < 0].copy()
    s["w"] = s["f"].abs()
    def agg(g):
        w = g["w"]; x = g["ex"]; m = (w*x).sum()/w.sum(); n=len(g)
        se = np.sqrt((w**2*(x-m)**2).sum()*n/max(n-1,1))/w.sum()
        return pd.Series(dict(n=n, wmean=m, mean=x.mean(), median=x.median(), sd=x.std(), t=m/se if se>0 else np.nan, hit=(x>0).mean()))
    out = {}
    out["all"] = agg(s).to_frame().T
    out["by_coin"] = s.groupby("coin").apply(agg)
    out["by_year"] = s.groupby("year").apply(agg)
    s["terc"] = pd.qcut(s["w"].rank(method="first"), 3, labels=["lo","mid","hi"])
    out["by_terc"] = s.groupby("terc").apply(agg)
    s["rawq"] = pd.qcut(s["raw"].rank(method="first"), 4, labels=["deepest","q2","q3","shallow"])
    out["by_raw_spread_q"] = s.groupby("rawq").apply(agg)
    s["mom"] = np.where(s["mom60"] < 0, "60d_down", "60d_up")
    out["by_60d_mom"] = s.groupby("mom").apply(agg)
    # market move: BTC fwd return same window/case approx via year grouping of coin fwd
    out["share_active"] = float((d["f"]<0).mean())
    out["fwd_dist"] = s["fwd"].describe()
    # inactive bars excess (as long baseline)
    fl = d[d["f"]==0]
    out["flat_bars_fwd_minus_hold"] = pd.Series(dict(n=len(fl), mean=(fl["fwd"]-fl["hold"]).mean()))
    win_m = s.groupby(["coin","win"])["ex"].mean()
    out["coinwindow_share_pos"] = pd.Series(dict(n=len(win_m), share_pos=(win_m>0).mean(), mean=win_m.mean(), median=win_m.median()))
    return out
