def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats as st
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"])})
            d["ret1"] = c.pct_change()
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c - 1
            rng = (b["high"] - b["low"]) / c
            d["width"] = rng / rng.rolling(20, min_periods=20).mean()
            d["volr"] = b["volume"] / b["volume"].shift(1).rolling(20, min_periods=20).mean()
            d["clpos"] = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            d["vol30"] = d["ret1"].rolling(30, min_periods=20).std()
            d["vmed"] = d["vol30"].rolling(120, min_periods=60).median()
            d["agit"] = d["vol30"] > d["vmed"]
            d["tr60"] = c / c.shift(60) - 1
            d["falling"] = b["regime"].isin(["mean_reversion", "unknown"])
            d["sd20"] = d["ret1"].rolling(20, min_periods=20).std()
            d["zret"] = d["ret1"] / d["sd20"]
            rows.append(d)
    X = pd.concat(rows, ignore_index=True)
    X["day"] = X["ts"].dt.floor("D")
    mu = X.groupby("coin")["f1"].mean()
    X["u1"] = X["f1"] - X["coin"].map(mu)
    X["u2"] = X["f2"] - 2 * X["coin"].map(mu)

    def stat(df, col, sign=1.0):
        df = df.dropna(subset=[col])
        if len(df) < 5:
            return pd.Series({"n": len(df), "mean%": np.nan, "t": np.nan, "days": 0})
        v = sign * df[col]; n = len(v); m = v.mean()
        ds = (v - m).groupby(df["day"]).sum()
        se = np.sqrt((ds ** 2).sum()) / n
        return pd.Series({"n": n, "mean%": 100 * m, "t": m / se if se > 0 else np.nan, "days": ds.size})

    out = {}
    F = X[X["falling"]]
    up = F[(F["ret1"] > 0)].dropna(subset=["width", "u1"]).copy()
    up["q"] = pd.qcut(up["width"], 5, labels=False)
    up["ag"] = up["agit"].map({True: "agit", False: "calm"})
    out["fall_up_width_q_by_agit"] = up.groupby(["ag", "q"]).apply(lambda g: stat(g, "u1"))
    up["wq"] = pd.qcut(up["width"], 3, labels=False)
    up["vq"] = pd.qcut(up["volr"], 3, labels=False)
    out["fall_up_width_x_vol"] = up.groupby(["wq", "vq"]).apply(lambda g: stat(g, "u1"))
    up["cq"] = pd.qcut(up["clpos"], 3, labels=False)
    out["fall_up_width_x_closepos"] = up.groupby(["wq", "cq"]).apply(lambda g: stat(g, "u1"))
    out["fall_up_width_q_u2"] = up.groupby("q").apply(lambda g: stat(g, "u2"))
    # by zscore of up day
    up["zq"] = pd.qcut(up["zret"], 5, labels=False)
    out["fall_up_zret_q_u1"] = up.groupby("zq").apply(lambda g: stat(g, "u1"))
    # rising vs choppy
    R = X[(X["tr60"] > 0.10) & (X["ret1"] > 0)].dropna(subset=["width", "u1"]).copy()
    R["q"] = pd.qcut(R["width"], 5, labels=False)
    out["rising_up_width_q_u1"] = R.groupby("q").apply(lambda g: stat(g, "u1"))
    # falling down days: width x agit (rebound family check)
    dn = F[F["ret1"] < 0].dropna(subset=["zret", "u1"]).copy()
    dn["zq"] = pd.qcut(dn["zret"], 5, labels=False)
    dn["ag"] = dn["agit"].map({True: "agit", False: "calm"})
    out["fall_dn_zret_q_by_agit"] = dn.groupby(["ag", "zq"]).apply(lambda g: stat(g, "u1"))
    # rank correlation width vs u1 in falling up days, per window then pooled
    r = st.spearmanr(up["width"], up["u1"])
    out["spearman_width_u1_fall_up"] = pd.Series({"rho": r.correlation, "p": r.pvalue, "n": len(up)})
    out["by_window_wide_minus_narrow"] = up.groupby("win").apply(
        lambda g: pd.Series({"n": len(g), "wide_top40_mean%": 100*g.loc[g["q"]>=3,"u1"].mean(),
                             "narrow_bot40_mean%": 100*g.loc[g["q"]<=1,"u1"].mean()}))
    return out
