def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            mad = r1.abs().shift(1).rolling(60, min_periods=20).mean()
            z = r1 / mad
            pos = b["postRebalance_current_allocation"].astype(float)
            g = pos * (c.shift(-1) / c - 1)
            for h in (1, 2, 3, 5):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    if pd.isna(fwd.iloc[i]) or pd.isna(z.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, z=z.iloc[i], fwd=fwd.iloc[i],
                                     reg=b["regime"].iloc[i], yr=pd.to_datetime(b["timestamp"].iloc[i]).year,
                                     pos=pos.iloc[i], g=g.iloc[i]))
    df = pd.DataFrame(rows)
    df = df.join(df.groupby(["coin", "h"])["fwd"].mean().rename("mh"), on=["coin", "h"])
    df["ex"] = df["fwd"] - df["mh"]
    df["mr"] = df["reg"] == "mean_reversion"
    out["regime_share"] = df[df.h == 1].groupby("coin")["mr"].mean().round(3)
    def reg(g):
        if len(g) < 10: return pd.Series({"n": len(g)})
        zz = g["z"].clip(-5, 5)
        s = stats.linregress(zz, g["ex"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["ex_on_z_by_h_regime_coin"] = df.groupby(["h", "mr", "coin"]).apply(reg).round(4)
    # sign asymmetry: down days vs up days, magnitude regression
    df["side"] = np.where(df.z < 0, "down", "up")
    df["az"] = df.z.abs().clip(0, 5)
    def reg2(g):
        if len(g) < 10: return pd.Series({"n": len(g)})
        s = stats.linregress(g["az"], g["ex"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["ex_on_absz_by_side"] = df.groupby(["h", "mr", "side"]).apply(reg2).round(4)
    # large down days outside regime by year, h=1
    sub = df[(df.h == 1) & (~df.mr) & (df.z <= -2)]
    out["bigdown_h1_out_by_year"] = sub.groupby("yr")["ex"].agg(["count", "mean"]).round(4)
    sub3 = df[(df.h == 3) & (~df.mr) & (df.z >= 2)]
    out["bigup_h3_out_by_coin"] = sub3.groupby("coin")["ex"].agg(["count", "mean"]).round(4)
    # book gain by position side, h=1 rows
    d1 = df[df.h == 1].dropna(subset=["g"])
    d1["ps"] = np.sign(d1.pos)
    out["gain_by_pos_side"] = d1.groupby(["coin", "ps"])["g"].agg(["count", "mean", "sum"]).round(5)
    # book: day after largest gains/losses
    drows = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy().reset_index(drop=True)
            d["nxt"] = d["book_return"].shift(-1); d["coin"] = coin
            drows.append(d)
    D = pd.concat(drows).dropna(subset=["book_return", "nxt"])
    D["q"] = D.groupby("coin")["book_return"].transform(lambda x: pd.qcut(x.rank(method="first"), 10, labels=False))
    out["book_next_by_decile"] = D.groupby("q")["nxt"].agg(["count", "mean"]).round(5)
    out["book_autocorr"] = D.groupby("coin").apply(lambda x: x["book_return"].corr(x["nxt"])).round(4)
    return out
