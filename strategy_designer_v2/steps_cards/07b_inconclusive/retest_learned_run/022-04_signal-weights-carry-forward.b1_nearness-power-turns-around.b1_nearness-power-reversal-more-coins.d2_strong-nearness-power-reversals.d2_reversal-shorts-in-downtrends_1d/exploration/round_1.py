def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for H in [1, 3, 5, 10, 20]:
        for coin, wins in bars.items():
            allr, cases = [], []
            for w, df in wins.items():
                c = df["close"].values
                f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"])
                for i in range(0, len(df) - H, H):
                    r = c[i + H] / c[i] - 1
                    allr.append(r)
                    if f[i] <= -2:
                        r20 = c[i] / c[i - 20] - 1 if i >= 20 else np.nan
                        cases.append((w, ts.iloc[i].year, abs(f[i]), r, r20))
            if len(allr) < 3:
                continue
            m = np.mean(allr)
            sd = np.std(allr, ddof=1)
            for w, y, fa, r, r20 in cases:
                rows.append(dict(H=H, coin=coin, w=w, year=y, f=fa,
                                 ex=-(r - m), tot=-r, st=-(r - m) / sd,
                                 wex=-(r - m) * fa / 10, r20=r20))
    d = pd.DataFrame(rows)

    def summ(g):
        n = len(g)
        s = g.ex.std(ddof=1) if n > 1 else np.nan
        ws = g.wex.std(ddof=1) if n > 1 else np.nan
        return pd.Series(dict(
            n=n,
            mean_ex=g.ex.mean(),
            t_ex=g.ex.mean() / (s / np.sqrt(n)) if n > 2 and s > 0 else np.nan,
            t_weighted=g.wex.mean() / (ws / np.sqrt(n)) if n > 2 and ws > 0 else np.nan,
            mean_tot=g.tot.mean(),
            strength=g.st.mean(),
            share_pos=(g.ex > 0).mean(),
        ))

    d5 = d[d.H == 5].copy()
    d5["f_quint"] = pd.qcut(d5.f.rank(method="first"), 5, labels=False)
    d5r = d5.dropna(subset=["r20"]).copy()
    d5r["r20_quart"] = pd.qcut(d5r.r20.rank(method="first"), 4, labels=False)
    trim = d5[(d5.ex > d5.ex.quantile(0.02)) & (d5.ex < d5.ex.quantile(0.98))]
    wins_t = d5.groupby("w").apply(summ)

    return {
        "by_horizon": d.groupby("H").apply(summ),
        "h5_by_coin": d5.groupby("coin").apply(summ),
        "h5_by_year": d5.groupby("year").apply(summ),
        "h5_by_forecast_quintile": d5.groupby("f_quint").apply(summ).join(
            d5.groupby("f_quint").f.agg(["min", "max"])),
        "h5_by_r20_quartile": d5r.groupby("r20_quart").apply(summ).join(
            d5r.groupby("r20_quart").r20.agg(["min", "max"])),
        "h5_trimmed_2pct_tails": summ(trim),
        "h5_windows": pd.Series(dict(n_windows=len(wins_t),
                                     share_windows_pos=(wins_t.mean_ex > 0).mean())),
    }
