def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            r = pd.Series(c).pct_change()
            s14 = r.rolling(14).std()
            s90 = r.shift(14).rolling(90).std()
            ratio = s14 / s90 - 1
            ret60 = pd.Series(c).pct_change(60)
            n = len(df)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, h=h, ts=df["timestamp"].iloc[i],
                                     fc=float(df["forecast"].iloc[i]) if pd.notna(df["forecast"].iloc[i]) else np.nan,
                                     reg=df["regime"].iloc[i], ratio=ratio.iloc[i], ret60=ret60.iloc[i],
                                     fwd=c[i + h] / c[i] - 1))
    X = pd.DataFrame(rows)
    X["drift"] = X.groupby(["coin", "h"])["fwd"].transform("mean")
    X["ex"] = X["fwd"] - X["drift"]
    X["rising"] = X["reg"] == "unknown"

    def ct(d, wcol=None):
        if len(d) < 5: return pd.Series(dict(n=len(d), mean=np.nan, t=np.nan))
        w = d[wcol] if wcol else pd.Series(1.0, index=d.index)
        m = (d["ex"] * w).sum() / w.sum()
        dev = ((d["ex"] - m) * w).groupby(d["ts"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() / w.sum() ** 2 * G / max(G - 1, 1))
        return pd.Series(dict(n=len(d), days=G, mean=m, t=m / se if se > 0 else np.nan))

    out = {}
    hor = []
    for h in (1, 3, 5, 10):
        d = X[(X.h == h) & X.rising & (X.fc > 0)]
        s = ct(d, "fc"); s["h"] = h; hor.append(s)
        d0 = X[(X.h == h) & X.rising & (X.fc <= 0)]
        s0 = ct(d0); s0["h"] = -h; hor.append(s0)
    out["horizons_fc>0_weighted (h<0: rising fc0)"] = pd.DataFrame(hor)
    G3 = X[X.h == 3]
    R = G3[G3.rising]
    out["by_coin_fc>0"] = R[R.fc > 0].groupby("coin").apply(lambda d: ct(d, "fc"))
    out["by_coin_fc0"] = R[R.fc <= 0].groupby("coin").apply(ct)
    out["by_window_fc>0"] = R[R.fc > 0].groupby("win").apply(lambda d: ct(d, "fc"))
    R = R.copy()
    pos = R[R.fc > 0]
    R["bucket"] = np.where(R.fc <= 0, "0", np.where(R.fc <= pos.fc.median(), "pos_low", "pos_high"))
    out["rising_fc_buckets"] = R.groupby("bucket").apply(ct)
    # ratio quintiles, rising vs outside
    G3 = G3.dropna(subset=["ratio"]).copy()
    G3["rq"] = pd.qcut(G3["ratio"], 5, labels=False)
    out["ratio_quintile_rising"] = G3[G3.rising].groupby("rq").apply(ct)
    out["ratio_quintile_notrising"] = G3[~G3.rising].groupby("rq").apply(ct)
    # trend strength inside rising
    Rp = R[R.fc > 0].dropna(subset=["ret60"]).copy()
    Rp["trq"] = pd.qcut(Rp["ret60"], 3, labels=["weak", "mid", "strong"])
    out["fc>0_by_trend_strength"] = Rp.groupby("trq").apply(lambda d: ct(d, "fc"))
    out["share_rising_grid"] = float(X[X.h == 3].rising.mean())
    return out
