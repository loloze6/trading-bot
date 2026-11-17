def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 14
    rows = []
    dayrows = []
    for coin, wins in data["bars"].items():
        # coin mean 14-bar return over all windows (grid)
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        cm = np.mean(allr)
        dmean = []
        for w, d in data["days"][coin].items():
            dmean += list(d["coin_return"].dropna())
        cdm = np.mean(dmean)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            share = b["debug_info.components.rsi_below_share.last_history_value"].values
            ret60 = pd.Series(c).pct_change(60).values
            ret30 = pd.Series(c).pct_change(30).values
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                rows.append(dict(coin=coin, win=w, f=b["forecast"].iloc[i], share=share[i],
                                 r=c[i + H] / c[i] - 1 - cm, r60=ret60[i], r30=ret30[i],
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
            pos = b["postRebalance_current_allocation"].shift(1)
            g = pos * (pd.Series(c).pct_change())
            for i in range(1, len(c)):
                dayrows.append(dict(coin=coin, win=w, pos=pos.iloc[i], g=g.iloc[i],
                                    mkt=pos.iloc[i] * cdm, r60=ret60[i - 1], fee_bar=b["postRebalance_total_value"].iloc[i] / b["total_portfolio_value"].iloc[i] - 1))
    df = pd.DataFrame(rows)
    dd = pd.DataFrame(dayrows).dropna(subset=["pos", "g"])
    a = df[df.f != 0].dropna(subset=["f", "r"])
    def slope(x, y):
        s = stats.linregress(x, y)
        return pd.Series(dict(slope=s.slope, t=s.slope / s.stderr, n=len(x)))
    out["slope by coin"] = a.groupby("coin").apply(lambda g: slope(g.f, g.r))
    a = a.copy()
    a["fq"] = pd.qcut(a.f, 5, labels=False, duplicates="drop")
    out["fwd ret by forecast quintile"] = a.groupby("fq").agg(f=("f", "mean"), share=("share", "mean"), r=("r", "mean"), n=("r", "size"))
    b2 = a.dropna(subset=["r60"])
    b2 = b2.assign(up=b2.r60 > 0)
    out["slope by 60d trend sign"] = b2.groupby("up").apply(lambda g: slope(g.f, g.r))
    b2["tq"] = pd.qcut(b2.r60, 3, labels=False)
    out["slope by 60d ret tercile"] = b2.groupby("tq").apply(lambda g: slope(g.f, g.r))
    out["slope by year"] = a.groupby("year").apply(lambda g: slope(g.f, g.r))
    dd["side"] = np.sign(dd.pos)
    out["gain by side"] = dd.groupby("side").agg(g=("g", "mean"), mkt=("mkt", "mean"), n=("g", "size"))
    dd["timing"] = dd.g - dd.mkt
    out["timing by 60d up"] = dd.dropna(subset=["r60"]).groupby([dd.r60 > 0, "side"]).agg(timing=("timing", "mean"), g=("g", "mean"), n=("g", "size"))
    out["fee per bar mean"] = float(dd.fee_bar.mean())
    out["mean gross gain"] = float(dd.g.mean())
    out["mean abs pos"] = float(dd.pos.abs().mean())
    return out
