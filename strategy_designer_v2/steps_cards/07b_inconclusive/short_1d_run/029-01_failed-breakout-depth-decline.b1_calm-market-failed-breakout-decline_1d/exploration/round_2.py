import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [5, 10]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            f = df["forecast"].fillna(0).values
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            vol_rank_w = vol20.expanding(min_periods=20).rank(pct=True)
            vol120 = r.rolling(120, min_periods=40).std()
            hi20 = c.shift(1).rolling(20).max()
            raw = df.get("debug_info.components.failed_bo_calm.last_history_value")
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for g in range(0, n, 5):
                for i in range(g, min(g + 5, n)):
                    if f[i] <= -2:
                        if i + 5 >= n:
                            break
                        d = {"coin": coin, "w": w, "year": int(yr[i]),
                             "vol20": vol20[i], "vrw": vol_rank_w[i],
                             "vratio": vol20[i] / vol120[i] if pd.notna(vol120[i]) else np.nan,
                             "depth": (hi20[i] - c[i]) / c[i] if pd.notna(hi20[i]) else np.nan,
                             "raw": raw[i] if raw is not None else np.nan}
                        for H in [5, 10]:
                            d[f"u{H}"] = -(c[i + H] / c[i] - 1 - drift[(coin, H)]) if i + H < n else np.nan
                        rows.append(d)
                        break
    X = pd.DataFrame(rows)

    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    X["vol_q_coin"] = X.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["within_coin_vol_tercile_u5"] = X.groupby("vol_q_coin").apply(summ)
    out["within_coin_vol_tercile_u10"] = X.groupby("vol_q_coin").apply(lambda g: summ(g, "u10"))
    X["vol_q"] = pd.qcut(X["vol20"], 3, labels=False)
    out["global_low_vol_coin_mix"] = pd.crosstab(X["coin"], X["vol_q"])
    out["global_low_vol_by_year_u10"] = X[X["vol_q"] == 0].groupby("year").apply(lambda g: summ(g, "u10"))
    X["vrw_q"] = pd.qcut(X["vrw"], 3, labels=False)
    out["window_vol_rank_tercile_u10"] = X.groupby("vrw_q").apply(lambda g: summ(g, "u10"))
    X["vratio_q"] = pd.qcut(X["vratio"], 3, labels=False)
    out["vol_ratio_tercile_u5"] = X.groupby("vratio_q").apply(summ)
    out["vol_ratio_tercile_u10"] = X.groupby("vratio_q").apply(lambda g: summ(g, "u10"))
    X["raw_q"] = pd.qcut(X["raw"].rank(method="first"), 3, labels=False)
    out["raw_component_tercile_u5"] = X.groupby("raw_q").apply(summ)
    out["raw_component_tercile_u10"] = X.groupby("raw_q").apply(lambda g: summ(g, "u10"))
    out["raw_nonnull"] = int(X["raw"].notna().sum())
    out["corr_vol20_u10_spearman"] = float(X[["vol20", "u10"]].corr(method="spearman").iloc[0, 1])
    out["corr_depth_u5_spearman"] = float(X[["depth", "u5"]].corr(method="spearman").iloc[0, 1])
    return out
