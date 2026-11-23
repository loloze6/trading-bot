import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [1, 3, 5, 10, 20]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rs.append(c[i + H] / c[i] - 1)
            drift[(coin, H)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            f = df["forecast"].fillna(0).values
            r = c.pct_change()
            vol20 = r.rolling(20).std()
            hi20 = c.shift(1).rolling(20).max()
            vol_rank = vol20.rolling(250, min_periods=60).rank(pct=True)
            ret20 = c / c.shift(20) - 1
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for g in range(0, n, 5):
                for i in range(g, min(g + 5, n)):
                    if f[i] <= -2:
                        if i + 5 >= n:
                            break
                        d = {"coin": coin, "w": w, "year": int(yr[i]), "f": f[i],
                             "vol20": vol20[i], "volrank": vol_rank[i], "ret20": ret20[i],
                             "depth": (hi20[i] - c[i]) / c[i] if pd.notna(hi20[i]) else np.nan}
                        for H in [1, 3, 5, 10, 20]:
                            if i + H < n:
                                tot = c[i + H] / c[i] - 1
                                m, s = drift[(coin, H)]
                                d[f"u{H}"] = -(tot - m)
                                d[f"t{H}"] = -tot
                            else:
                                d[f"u{H}"] = np.nan
                                d[f"t{H}"] = np.nan
                        rows.append(d)
                        break
    X = pd.DataFrame(rows)

    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["n_cases"] = len(X)
    out["forecast_values"] = X["f"].round(1).value_counts().head(10)
    out["by_coin"] = X.groupby("coin").apply(summ)
    out["by_year"] = X.groupby("year").apply(summ)
    hz = []
    for H in [1, 3, 5, 10, 20]:
        s = summ(X, f"u{H}")
        s2 = summ(X, f"t{H}")
        hz.append([H, s["n"], s["mean"], s["t"], s2["mean"], s2["t"]])
    out["by_horizon"] = pd.DataFrame(hz, columns=["H", "n", "unusual", "t_u", "total", "t_tot"])
    X["vol_q"] = pd.qcut(X["vol20"], 3, labels=["low", "mid", "high"])
    X["vrank_q"] = pd.qcut(X["volrank"], 3, labels=["low", "mid", "high"])
    X["depth_q"] = pd.qcut(X["depth"], 3, labels=["shallow", "mid", "deep"])
    X["ret20_q"] = pd.qcut(X["ret20"], 3, labels=["low", "mid", "high"])
    out["by_vol20_tercile"] = X.groupby("vol_q").apply(summ)
    out["by_own_vol_rank_tercile"] = X.groupby("vrank_q").apply(summ)
    out["by_depth_tercile"] = X.groupby("depth_q").apply(summ)
    out["by_ret20_tercile"] = X.groupby("ret20_q").apply(summ)
    out["by_vol_x_h10"] = X.groupby("vol_q").apply(lambda g: summ(g, "u10"))
    out["by_ret20_x_h10"] = X.groupby("ret20_q").apply(lambda g: summ(g, "u10"))
    return out
