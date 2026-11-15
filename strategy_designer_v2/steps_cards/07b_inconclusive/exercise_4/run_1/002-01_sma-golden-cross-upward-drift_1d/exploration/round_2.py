def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            r20 = pd.Series(c).pct_change(20).values
            r60 = pd.Series(c).pct_change(60).values
            h = 10
            for i in range(0, len(df) - h, h):
                rows.append(dict(coin=coin, w=w, f=f[i], r20=r20[i], r60=r60[i],
                                 year=ts[i].year, ret=c[i+h]/c[i]-1))
    S = pd.DataFrame(rows)
    S["ex"] = S["ret"] - S.groupby("coin")["ret"].transform("mean")
    S = S.dropna(subset=["r20"])
    def sl(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 10: return pd.Series(dict(slope=np.nan, t=np.nan, n=len(d)))
        r = stats.linregress(d[x], d["ex"])
        return pd.Series(dict(slope=r.slope, t=r.slope/r.stderr, n=len(d)))
    out = {}
    on = S[S.f > 0]; off = S[S.f == 0]
    out["r20_slope_on_vs_off"] = pd.DataFrame({"on": sl(on, "r20"), "off": sl(off, "r20"), "all": sl(S, "r20")}).T
    out["r60_slope_on_vs_off"] = pd.DataFrame({"on": sl(on, "r60"), "off": sl(off, "r60")}).T
    a = on[on.r20 > 0]["ex"]; b = on[on.r20 <= 0]["ex"]
    out["on_up_minus_on_down"] = pd.Series(dict(up=a.mean(), down=b.mean(), diff=a.mean()-b.mean(),
        t=stats.ttest_ind(a, b, equal_var=False).statistic, n_up=len(a), n_down=len(b)))
    a2 = off[off.r20 > 0]["ex"]; b2 = off[off.r20 <= 0]["ex"]
    out["off_up_minus_off_down"] = pd.Series(dict(up=a2.mean(), down=b2.mean(), diff=a2.mean()-b2.mean(),
        t=stats.ttest_ind(a2, b2, equal_var=False).statistic, n_up=len(a2), n_down=len(b2)))
    on = on.copy()
    on["q"] = pd.qcut(on.r20, 4, labels=["q1","q2","q3","q4"])
    out["on_r20_quartiles"] = on.groupby("q")["ex"].agg(["mean","count"])
    out["on_r20_by_coin"] = on.groupby("coin").apply(lambda g: sl(g, "r20"))
    out["on_r20_by_year"] = on.groupby("year").apply(lambda g: sl(g, "r20"))
    # interaction: product f*r20 on all
    S["fr"] = S.f * S.r20
    out["f_x_r20_slope_all"] = sl(S, "fr")
    return out
