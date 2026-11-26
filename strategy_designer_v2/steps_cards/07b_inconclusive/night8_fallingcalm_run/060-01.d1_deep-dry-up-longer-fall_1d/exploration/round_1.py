def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for H in [5, 10, 20, 40]:
        for coin, wins in bars.items():
            # coin mean H-return over all windows' grid
            allr = []
            cells = []
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                raw = df.get("debug_info.components.vol_dryup.last_history_value")
                fc = df["forecast"].values
                v = df["volume"].values
                vs = pd.Series(v)
                rec = np.log(vs.rolling(30).mean() / vs.shift(30).rolling(30).mean()).values
                rawv = raw.values if raw is not None else np.full(len(df), np.nan)
                ret60 = pd.Series(c).pct_change(20).values
                n = len(df)
                for t in range(0, n - H, H):
                    r = c[t + H] / c[t] - 1
                    allr.append(r)
                    cells.append(dict(H=H, coin=coin, w=w, r=r, regime=df["regime"].iloc[t],
                                      raw=rawv[t] if not np.isnan(rawv[t]) else rec[t],
                                      fc=fc[t], yr=pd.Timestamp(df["timestamp"].iloc[t]).year,
                                      past20=ret60[t]))
            m = np.mean(allr)
            for cc in cells:
                cc["ex_short"] = -(cc["r"] - m)
                cc["tot_short"] = -cc["r"]
                rows.append(cc)
    d = pd.DataFrame(rows)
    f = d[d.regime == "unknown"].dropna(subset=["raw"])
    def summ(g):
        x = g["ex_short"]
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "mean_tot": g["tot_short"].mean()})
    f["dry"] = np.where(f.raw < 0, "shrunk", "grew")
    out["falling_by_H_dry"] = f.groupby(["H", "dry"]).apply(summ)
    # raw-slope grading within shrunk, and across all falling
    res = []
    for H in [5, 10, 20, 40]:
        g = f[f.H == H]
        s = stats.linregress(-g.raw, g.ex_short)
        gs = g[g.raw < 0]
        s2 = stats.linregress(-gs.raw, gs.ex_short)
        gf = gs[gs.fc < 0]
        s3 = stats.linregress(-gf.fc, gf.ex_short) if len(gf) > 5 else None
        res.append(dict(H=H, slope_t_rawall=s.slope/s.stderr, n_all=len(g), slope_t_raw_shrunk=s2.slope/s2.stderr,
                        n_shrunk=len(gs), slope_t_fc=(s3.slope/s3.stderr if s3 else np.nan), n_fc=len(gf)))
    out["slopes"] = pd.DataFrame(res)
    g20 = f[f.H == 20].copy()
    g20["q"] = pd.qcut(g20.raw, 5, labels=False)
    out["H20_raw_quintile"] = g20.groupby("q").apply(summ).join(g20.groupby("q").raw.mean())
    out["H20_shrunk_by_coin"] = g20[g20.raw < 0].groupby("coin").apply(summ)
    out["H20_shrunk_by_year"] = g20[g20.raw < 0].groupby("yr").apply(summ)
    out["H20_grew_by_year"] = g20[g20.raw >= 0].groupby("yr").apply(summ)
    nf = d[(d.H == 20) & (d.regime != "unknown")].dropna(subset=["raw"]).copy()
    nf["dry"] = np.where(nf.raw < 0, "shrunk", "grew")
    out["H20_notfalling_dry"] = nf.groupby("dry").apply(summ)
    return out
