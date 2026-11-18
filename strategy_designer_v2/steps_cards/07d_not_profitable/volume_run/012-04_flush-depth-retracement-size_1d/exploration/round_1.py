def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    # book summary
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            g = a * (b["close"].shift(-1) / b["close"] - 1)
            d = days[c][w]
            rows.append(dict(coin=c, bars=len(b), held=(a.abs() > 1e-9).sum(),
                             flush=(b["regime"] == "mean_reversion").sum(),
                             fpos=(b["forecast"] > 0).sum(),
                             gain=g.sum(), book=d["book_return"].sum(),
                             ntr=len(trades[c][w]) if trades[c][w] is not None else 0))
    r = pd.DataFrame(rows)
    out["by_coin"] = r.groupby("coin")[["bars", "held", "flush", "fpos", "gain", "book", "ntr"]].sum()
    # trades
    tl = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; tl.append(t)
    T = pd.concat(tl)
    out["trades"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
                                          mean_net=("net_profit_loss_percent", "mean"),
                                          mean_gross=("profit_loss_percent", "mean"),
                                          dur_h=("duration_minutes", lambda x: x.mean() / 60))
    # recompute situations and forward returns at several horizons
    H = [1, 2, 3, 5, 10]
    rec = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl, op, hi, lo, v = b["close"], b["open"], b["high"], b["low"], b["volume"]
            r1 = cl.pct_change()
            z = r1 / r1.rolling(20).std()
            vr = v / v.shift(1).rolling(20).mean()
            rng = (hi - lo).replace(0, np.nan)
            wick = (np.minimum(op, cl) - lo) / rng
            drop = (op - lo) / op
            df = pd.DataFrame(dict(z=z, vr=vr, wick=wick, drop=drop, coin=c, win=w,
                                   reg=b["regime"], fc=b["forecast"],
                                   alloc=b["postRebalance_current_allocation"]))
            for h in H:
                df[f"f{h}"] = cl.shift(-h) / cl - 1
            rec.append(df)
    D = pd.concat(rec, ignore_index=True)
    # coin mean returns per horizon (non-overlap approx: use all bars mean)
    for h in H:
        D[f"x{h}"] = D[f"f{h}"] - D.groupby("coin")[f"f{h}"].transform("mean")
    def summ(mask, name):
        s = {}
        for h in H:
            x = D.loc[mask, f"x{h}"].dropna()
            s[f"x{h}"] = x.mean(); s[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        s["n"] = mask.sum()
        return pd.Series(s, name=name)
    m_reg = D["reg"] == "mean_reversion"
    S = [summ(m_reg, "flush_regime"),
         summ((D.z <= -2), "z<=-2"),
         summ((D.z <= -2) & (D.vr >= 2), "z<=-2&vol"),
         summ((D.z <= -2) & (D.vr < 2), "z<=-2&novol"),
         summ((D.z <= -1.5) & (D.vr >= 1.5) & (D.wick >= 0.3), "loose"),
         summ((D.z <= -1.5) & (D.vr >= 1.5), "z<=-1.5&vr>=1.5"),
         summ((D.z <= -1) & (D.wick >= 0.5), "z<=-1&wick>=.5"),
         summ((D.wick >= 0.6), "wick>=.6"),
         summ((D.z <= -3), "z<=-3")]
    out["fwd_by_situation"] = pd.DataFrame(S)
    # graded: z bins
    D["zb"] = pd.cut(D.z, [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    out["z_bins"] = D.groupby("zb")[["x1", "x3", "x5", "x10"]].mean().assign(n=D.groupby("zb").size())
    D["wb"] = pd.cut(D.wick, [0, .1, .2, .3, .4, .5, .6, .8, 1.0])
    out["wick_bins_negz"] = D[D.z < -1].groupby("wb")[["x1", "x3", "x5", "x10"]].mean().assign(n=D[D.z < -1].groupby("wb").size())
    # held position length
    out["held_frac"] = float((D.alloc.abs() > 1e-9).mean())
    return out
