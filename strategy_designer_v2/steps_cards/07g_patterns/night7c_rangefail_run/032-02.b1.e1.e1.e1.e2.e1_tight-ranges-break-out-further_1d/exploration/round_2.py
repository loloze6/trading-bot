def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r1 = cl.pct_change()
            hi60 = cl.shift(1).rolling(60, min_periods=60).max()
            lo60 = cl.shift(1).rolling(60, min_periods=60).min()
            pos = (cl - lo60) / (hi60 - lo60)
            hi20 = cl.shift(1).rolling(20, min_periods=20).max()
            lo20 = cl.shift(1).rolling(20, min_periods=20).min()
            pos20 = (cl - lo20) / (hi20 - lo20)
            vol60 = r1.rolling(60).std()
            past60 = cl / cl.shift(60) - 1
            for h in (3, 5, 10):
                fwd = cl.shift(-h) / cl - 1
                for i in range(0, len(b), h):
                    if i + h >= len(b): continue
                    rows.append(dict(coin=c, w=w, h=h, fwd=fwd.iloc[i], pos=pos.iloc[i], pos20=pos20.iloc[i],
                                     vol60=vol60.iloc[i], past60=past60.iloc[i],
                                     yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    res = []
    for h in (3, 5, 10):
        for f in ["pos", "pos20"]:
            d = df[df.h == h].dropna(subset=[f, "ex"])
            q = pd.qcut(d.groupby("coin")[f].rank(pct=True), 5, labels=False)
            g = d.groupby(q)["ex"].mean()
            res.append(dict(h=h, f=f, n=len(d), q1=g.iloc[0], q2=g.iloc[1], q3=g.iloc[2], q4=g.iloc[3], q5=g.iloc[4],
                            t=stats.ttest_ind(d[q == 4]["ex"], d[q == 0]["ex"], equal_var=False).statistic,
                            spear=stats.spearmanr(d[f], d["ex"]).correlation))
    out["pos_quintiles"] = pd.DataFrame(res)
    d = df[(df.h == 5)].dropna(subset=["pos", "ex"])
    inside = d[(d.pos >= 0) & (d.pos <= 1)]
    out["pos_inside_range_h5"] = pd.Series({"n": len(inside),
        "spear": stats.spearmanr(inside.pos, inside.ex).correlation,
        "t_top_half_minus_bottom": stats.ttest_ind(inside[inside.pos > .5].ex, inside[inside.pos <= .5].ex, equal_var=False).statistic,
        "top_half_mean": inside[inside.pos > .5].ex.mean(), "bottom_half_mean": inside[inside.pos <= .5].ex.mean()})
    def sp(g):
        return pd.Series({"n": len(g), "spear": stats.spearmanr(g.pos, g.ex).correlation,
                          "hi_minus_lo": g[g.pos > g.pos.median()].ex.mean() - g[g.pos <= g.pos.median()].ex.mean()})
    out["pos_h5_by_coin"] = d.groupby("coin").apply(sp)
    out["pos_h5_by_year"] = d.groupby("yr").apply(sp)
    d["volhi"] = d.vol60 > d.groupby("coin").vol60.transform("median")
    out["pos_h5_by_vol"] = d.groupby("volhi").apply(sp)
    d["up60"] = d.past60 > 0
    out["pos_h5_by_trend"] = d.groupby("up60").apply(sp)
    # book's largest days
    br = []
    for c, ws in data["days"].items():
        for w, dd in ws.items():
            br.append(dd.assign(coin=c, w=w))
    D = pd.concat(br)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B = B[B.book_return != 0].dropna()
    out["book_nonzero_days"] = pd.Series({"n": len(B), "mean": B.book_return.mean(),
        "top10_share_of_sum": B.book_return.nlargest(10).sum() / B.book_return.sum(),
        "bottom10_sum": B.book_return.nsmallest(10).sum(), "corr_with_coin": B.book_return.corr(B.coin_return)})
    return out
