def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in (3, 7, 14):
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol = r1.rolling(30).std() * np.sqrt(7)
            z = (c / c.shift(7) - 1) / vol
            prof = (b["regime"] == "unknown").values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for h in (3, 7, 14):
                m, s = drift[(coin, h)]
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    if np.isnan(z.iloc[i]) or np.isnan(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, win=w, h=h, prof=prof[i], year=yr[i],
                                     z=z.iloc[i], fwd=fwd.iloc[i], unus=fwd.iloc[i] - m, usual=s))
    df = pd.DataFrame(rows)
    out = {}
    def summ(g):
        x = g["unus"]
        t = x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series({"n": len(x), "mean_unus": x.mean(), "t": t, "mean_total": g["fwd"].mean(),
                          "strength": (x / g["usual"]).mean()})
    df["side"] = np.where(df["z"] < 0, "fall", "rise")
    df["zbin"] = pd.cut(df["z"], [-np.inf, -1.5, -0.75, 0, 0.75, 1.5, np.inf])
    p = df[df.prof]
    out["prof_by_h_side"] = p.groupby(["h", "side"]).apply(summ)
    out["prof_h7_by_zbin"] = p[p.h == 7].groupby("zbin").apply(summ)
    out["all_h7_by_zbin"] = df[df.h == 7].groupby("zbin").apply(summ)
    pf = p[(p.h == 7) & (p.side == "fall")]
    out["prof_fall_h7_by_year"] = pf.groupby("year").apply(summ)
    out["prof_fall_h7_by_coin"] = pf.groupby("coin").apply(summ)
    for h in (3, 7, 14):
        q = p[p.h == h]
        out[f"corr_z_unus_prof_h{h}"] = float(stats.spearmanr(q["z"], q["unus"])[0])
        q2 = df[(df.h == h) & ~df.prof]
        out[f"corr_z_unus_nonprof_h{h}"] = float(stats.spearmanr(q2["z"], q2["unus"])[0])
    out["prof_share"] = float(df[df.h == 7]["prof"].mean())
    return out
