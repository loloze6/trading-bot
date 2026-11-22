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
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for g in range(0, n, 5):
                for i in range(g, min(g + 5, n)):
                    if f[i] <= -2:
                        if i + 5 >= n:
                            break
                        d = {"coin": coin, "w": w, "year": int(yr[i]), "vol20": vol20[i]}
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
    X["q"] = X.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    low = X[X["q"] == 0]
    out["low_by_coin_u5"] = low.groupby("coin").apply(summ)
    out["low_by_year_u5"] = low.groupby("year").apply(summ)
    out["low_year_mix"] = low["year"].value_counts().sort_index()
    out["all_by_year_count"] = X["year"].value_counts().sort_index()
    X["lv"] = np.log(X["vol20"])
    X["lv_dm"] = X["lv"] - X.groupby("coin")["lv"].transform("mean")
    sp = X[["lv_dm", "u5", "u10"]].corr(method="spearman")
    out["spearman_demeaned_logvol"] = sp.loc["lv_dm", ["u5", "u10"]]
    X["q5"] = X.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["within_coin_vol_quintile_u5"] = X.groupby("q5").apply(summ)
    out["low_minus_high_u5_welch"] = float(
        (low["u5"].mean() - X[X["q"] == 2]["u5"].mean()) /
        np.sqrt(low["u5"].var() / len(low) + X[X["q"] == 2]["u5"].var() / (X["q"] == 2).sum()))
    return out
