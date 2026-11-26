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
            rng = hi60 / lo60 - 1
            past20 = cl / cl.shift(20) - 1
            past60 = cl / cl.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vol60 = r1.rolling(60).std()
            pos = (cl - lo60) / (hi60 - lo60)
            for h in (5, 20):
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if i + h >= len(b): continue
                    rows.append(dict(coin=c, w=w, h=h, fwd=fwd.iloc[i], rng=rng.iloc[i], past20=past20.iloc[i],
                                     past60=past60.iloc[i], volr=vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                                     vol20=vol20.iloc[i], pos=pos.iloc[i], r1=r1.iloc[i],
                                     newhi=cl.iloc[i] > hi60.iloc[i], newlo=cl.iloc[i] < lo60.iloc[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).weekday()))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    res = []
    for h in (5, 20):
        d = df[df.h == h]
        for f in ["rng", "past20", "past60", "volr", "vol20", "pos", "r1"]:
            dd = d.dropna(subset=[f, "ex"])
            dd = dd.assign(z=dd.groupby("coin")[f].rank(pct=True))
            q = pd.qcut(dd["z"], 5, labels=False)
            g = dd.groupby(q)["ex"].mean()
            top, bot = dd[q == 4]["ex"], dd[q == 0]["ex"]
            t = stats.ttest_ind(top, bot, equal_var=False).statistic
            res.append(dict(h=h, feat=f, n=len(dd), q1=g.iloc[0], q3=g.iloc[2], q5=g.iloc[4], t_q5_q1=t,
                            spear=stats.spearmanr(dd[f], dd["ex"]).correlation))
    out["quintiles"] = pd.DataFrame(res)
    for h in (5, 20):
        d = df[df.h == h]
        out[f"newhi_newlo_h{h}"] = pd.DataFrame({
            "newhi_mean": [d[d.newhi]["ex"].mean()], "newhi_n": [d.newhi.sum()],
            "newhi_t": [stats.ttest_1samp(d[d.newhi]["ex"].dropna(), 0).statistic],
            "newlo_mean": [d[d.newlo]["ex"].mean()], "newlo_n": [d.newlo.sum()],
            "newlo_t": [stats.ttest_1samp(d[d.newlo]["ex"].dropna(), 0).statistic]})
    # new lows graded by range (using every new-low bar's first in grid cell for h20)
    lo = df[(df.h == 20) & df.newlo].dropna(subset=["rng"])
    if len(lo) > 10:
        med = lo.groupby("coin")["rng"].transform("median")
        out["newlo_narrow_vs_wide"] = pd.Series({"narrow_mean": lo[lo.rng < med]["ex"].mean(),
            "wide_mean": lo[lo.rng > med]["ex"].mean(), "n": len(lo),
            "t": stats.ttest_ind(lo[lo.rng < med]["ex"], lo[lo.rng > med]["ex"], equal_var=False).statistic})
    d5 = df[df.h == 5]
    out["weekday_fwd5"] = d5.groupby("wd")["ex"].agg(["mean", "count"])
    # book
    days = data["days"]; br = []
    for c, ws in days.items():
        for w, d in ws.items():
            br.append(d.assign(coin=c, w=w))
    D = pd.concat(br)
    out["book_by_window"] = D.groupby("w")[["book_return", "coin_return"]].mean()
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean"])
    return out
