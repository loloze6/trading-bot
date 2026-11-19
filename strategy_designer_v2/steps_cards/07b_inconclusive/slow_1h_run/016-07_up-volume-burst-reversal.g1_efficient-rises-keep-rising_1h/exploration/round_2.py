def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            absd = np.abs(np.diff(c, prepend=np.nan))
            ers = np.full(n, np.nan)
            for i in range(72, n):
                s = np.nansum(absd[i-71:i+1])
                ers[i] = (c[i]-c[i-72])/s if s > 0 else np.nan
            for i in range(0, n, 72):
                rec = {"coin": coin, "win": w, "year": yr[i], "f": f[i]}
                rec["r72"] = c[i+72]/c[i]-1 if i+72 < n else np.nan
                rec["r120"] = c[i+120]/c[i]-1 if i+120 < n else np.nan
                if i >= 144:
                    rec["er_raw"] = ers[i]
                    past = ers[i-71:i+1]
                    mu, sd = np.nanmean(past), np.nanstd(past)
                    rec["er_z"] = (ers[i]-mu)/sd if sd > 0 else np.nan
                    rec["er_mu"] = mu
                    rec["ret72"] = c[i]/c[i-72]-1
                    rec["rise48"] = c[i] > c[i-48]
                else:
                    rec.update(er_raw=np.nan, er_z=np.nan, er_mu=np.nan, ret72=np.nan, rise48=False)
                rows.append(rec)
    d = pd.DataFrame(rows)
    for h in (72, 120):
        d[f"x{h}"] = d[f"r{h}"] - d.groupby("coin")[f"r{h}"].transform("mean")
    rise = d[(d.ret72 > 0) & d.rise48].dropna(subset=["er_raw", "x72"]).copy()
    def slope(g, x, y):
        g = g.dropna(subset=[x, y])
        if len(g) < 10: return (np.nan, np.nan, len(g))
        r = stats.linregress(g[x], g[y])
        return (r.slope, r.slope/r.stderr, len(g))
    out = {}
    out["raw_by_coin"] = pd.DataFrame({c: slope(g, "er_raw", "x72") for c, g in rise.groupby("coin")}, index=["slope", "t", "n"]).T
    out["raw_by_year"] = pd.DataFrame({y: slope(g, "er_raw", "x72") for y, g in rise.groupby("year")}, index=["slope", "t", "n"]).T
    out["ret72_only"] = pd.DataFrame({h: slope(rise, "ret72", f"x{h}") for h in (72, 120)}, index=["slope", "t", "n"]).T
    out["z_vs_raw"] = pd.DataFrame({k: slope(rise, k, "x72") for k in ("er_raw", "er_z", "er_mu")}, index=["slope", "t", "n"]).T
    out["corr_raw_z"] = float(rise[["er_raw", "er_z"]].corr().iloc[0, 1])
    rise["sq"] = pd.qcut(rise.ret72, 3, labels=False)
    out["raw_within_size_tercile"] = pd.DataFrame({s: slope(g, "er_raw", "x72") for s, g in rise.groupby("sq")}, index=["slope", "t", "n"]).T
    rise["rq"] = pd.qcut(rise.er_raw, 5, labels=False)
    out["share_pos_by_rawq"] = rise.groupby("rq").agg(x72=("x72", "mean"), pos=("x72", lambda s: (s > 0).mean()), sd=("x72", "std"), n=("x72", "count"))
    return out
