def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            z = r / sd30
            nxt = c.shift(-1) / c - 1
            nxt3 = c.shift(-3) / c - 1
            tr60 = c / c.shift(60) - 1
            ag = sd30.rolling(120, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            rng = (b["high"] - b["low"]) / c / sd30
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            r5 = c / c.shift(5) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "z": z, "nxt": nxt, "nxt3": nxt3, "tr60": tr60, "ag": ag,
                               "falling_reg": (b["regime"] == "unknown"), "rng": rng, "clo": clo,
                               "r5z": r5 / (sd30 * np.sqrt(5)),
                               "alloc": b["postRebalance_current_allocation"], "sd30": sd30})
            df["year"] = df["ts"].dt.year
            df["wd"] = df["ts"].dt.dayofweek
            df["pos"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d = d.dropna(subset=["nxt", "z"])
    mu = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - mu
    d["exn"] = d["ex"] / d["sd30"]
    def summ(g):
        n = len(g); m = g["ex"].mean(); s = g["ex"].std()
        return pd.Series({"n": n, "mean_ex_%": 100*m, "t": m/(s/np.sqrt(n)) if n > 2 else np.nan,
                          "mean_exn": g["exn"].mean()})
    d["zb"] = pd.cut(d["z"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    d["prof"] = np.where(d["tr60"] > 0.10, "rising", np.where(d["tr60"] < -0.10, "falling", "choppy"))
    d.loc[d["tr60"].isna(), "prof"] = np.nan
    out = {}
    out["by_zbin_all"] = d.groupby("zb").apply(summ)
    dd = d.dropna(subset=["prof"])
    out["by_prof_zbin"] = dd.groupby(["prof", "zb"]).apply(summ)
    dd2 = dd.copy(); dd2["agit"] = np.where(dd2["ag"] > 0.5, "agit", "calm")
    dd2 = dd2.dropna(subset=["ag"])
    out["slope_z_on_exn_by_prof_agit"] = dd2.groupby(["prof", "agit"]).apply(
        lambda g: pd.Series({"n": len(g), "corr": g["z"].corr(g["exn"]),
                             "t": g["z"].corr(g["exn"]) * np.sqrt(len(g))}))
    out["by_weekday"] = d.groupby("wd").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["rngb"] = pd.qcut(d["rng"], 5, duplicates="drop")
    out["by_range_quint"] = d.groupby("rngb").apply(summ)
    d["clob"] = pd.cut(d["clo"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["by_closeloc"] = d.groupby("clob").apply(summ)
    d["r5b"] = pd.cut(d["r5z"], [-np.inf, -2, -1, 0, 1, 2, np.inf])
    out["by_5day_z"] = d.groupby("r5b").apply(summ)
    out["by_coin_zcorr"] = d.groupby("coin").apply(lambda g: pd.Series({"n": len(g), "corr": g["z"].corr(g["exn"])}))
    return out
