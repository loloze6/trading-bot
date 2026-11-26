def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allgrid = {}
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    allgrid.setdefault((coin, h), []).append(c[i + h] / c[i] - 1)
            vol = df["volume"].values
            r20 = pd.Series(c).pct_change(20).values
            v30 = pd.Series(vol).rolling(30).mean()
            vr = np.log(v30 / v30.shift(30)).values
            d1 = pd.Series(c).pct_change()
            sw = (d1.rolling(30).std() / d1.rolling(60).std()).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, year=yr[i], h=h,
                        fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                        fwd=c[i + h] / c[i] - 1, r20=r20[i], vr=vr[i], sw=sw[i]))
    R = pd.DataFrame(rows)
    mu = {k: np.mean(v) for k, v in allgrid.items()}
    R["ex"] = R["fwd"] - [mu[(a, b)] for a, b in zip(R.coin, R.h)]
    R["prod"] = R["ex"] * R["fc"] / 10
    R["sx"] = -R["ex"]
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    act = R[(R.fc < 0)]
    out = {}
    out["by_h_prod"] = act.groupby("h").apply(lambda g: summ(g, "prod"))
    a5 = act[act.h == 5].copy()
    out["by_coin"] = a5.groupby("coin").apply(lambda g: summ(g, "prod"))
    out["by_year"] = a5.groupby("year").apply(lambda g: summ(g, "prod"))
    out["by_window"] = a5.groupby("w").apply(lambda g: summ(g, "sx"))
    a5["fq"] = pd.qcut(a5.fc, 3, labels=["strong", "mid", "weak"])
    out["by_fc_tercile_shortexcess"] = a5.groupby("fq").apply(lambda g: summ(g, "sx"))
    a5["r20b"] = pd.cut(a5.r20, [-0.2, -0.1, -0.05, 0], labels=["-20..-10", "-10..-5", "-5..0"])
    out["by_r20_shortexcess"] = a5.groupby("r20b").apply(lambda g: summ(g, "sx"))
    a5["swb"] = np.where(a5.sw > 1, "swing_up", "swing_down")
    out["by_swing_shortexcess"] = a5.groupby("swb").apply(lambda g: summ(g, "sx"))
    tr = R[(R.h == 5) & (R.reg == "trending")].copy()
    tr["side"] = np.where(tr.fc < 0, "shrink", "growth")
    out["regime_shrink_vs_growth"] = tr.groupby("side").apply(lambda g: summ(g, "sx"))
    out["corr_fc_ex_spearman"] = float(stats.spearmanr(a5.fc, a5.ex).correlation)
    out["corr_vr_ex_in_regime"] = float(stats.spearmanr(tr.vr, tr.ex, nan_policy="omit").correlation)
    # top-heavy: share of sum of prod from top 10 cases
    p = a5["prod"].sort_values(ascending=False)
    out["top10_share_of_sum"] = float(p.head(10).sum() / p.sum())
    out["median_prod"] = float(p.median())
    return out
