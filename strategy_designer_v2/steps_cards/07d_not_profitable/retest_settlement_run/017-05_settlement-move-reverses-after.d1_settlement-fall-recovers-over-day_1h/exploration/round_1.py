def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    drift = {}
    usual = {}
    # coin drift / usual move over 24 bars on non-overlapping grid
    for c, wins in data["bars"].items():
        r = []
        for w, b in wins.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            r.append(cl[idx + 24] / cl[idx] - 1)
        r = np.concatenate(r)
        drift[c] = r.mean(); usual[c] = r.std()
    for c, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            hr = ts.dt.hour.values
            n = len(b)
            r2 = cl / cl.shift(2) - 1
            sc = r2 / r2.abs().rolling(720, min_periods=100).mean()
            ret7 = cl / cl.shift(168) - 1
            ret3 = cl / cl.shift(72) - 1
            vol30 = (cl.pct_change()).rolling(720, min_periods=100).std()
            vol7 = (cl.pct_change()).rolling(168, min_periods=50).std()
            f24 = cl.shift(-24) / cl - 1
            f48 = cl.shift(-48) / cl - 1
            f72 = cl.shift(-72) / cl - 1
            settle = np.isin(hr, [23, 15])
            df = pd.DataFrame({"pos": np.arange(n), "hr": hr, "fc": b["forecast"].values,
                               "sc": sc.values, "r2": r2.values, "ret7": ret7.values, "ret3": ret3.values,
                               "vr": (vol7 / vol30).values,
                               "f24": f24.values, "f48": f48.values, "f72": f72.values,
                               "year": ts.dt.year.values})
            df = df[settle].copy()
            df["cell"] = df["pos"] // 24
            df["coin"] = c; df["win"] = w
            df["sig"] = df["fc"] > 0
            df = df.dropna(subset=["f24"])
            # first signal per cell; for non-signal first non-signal per cell
            s = df[df.sig].groupby("cell").head(1)
            ns = df[~df.sig].groupby("cell").head(1)
            rows.append(s); rows.append(ns)
    D = pd.concat(rows)
    D["d"] = D["coin"].map(drift); D["u"] = D["coin"].map(usual)
    D["ex24"] = D["f24"] - D["d"]
    D["ex48"] = D["f48"] - 2 * D["d"]
    D["ex72"] = D["f72"] - 3 * D["d"]
    S = D[D.sig].copy()
    def summ(g, col="ex24"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_ex%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "total%": 100 * (g["f24"].mean()) if col == "ex24" else np.nan})
    S["fq"] = pd.qcut(S["fc"].rank(method="first"), 5, labels=False)
    out["by_forecast_quintile"] = S.groupby("fq").apply(summ)
    out["by_hour"] = S.groupby("hr").apply(summ)
    out["by_coin"] = S.groupby("coin").apply(summ)
    out["by_year"] = S.groupby("year").apply(summ)
    S["t7"] = pd.qcut(S["ret7"].rank(method="first"), 3, labels=["down", "mid", "up"])
    D["t7"] = pd.qcut(D["ret7"].rank(method="first"), 3, labels=["down", "mid", "up"])
    out["sig_by_7d_trend"] = S.groupby("t7").apply(summ)
    out["nosig_by_7d_trend"] = D[~D.sig].groupby("t7").apply(summ)
    S["vq"] = pd.qcut(S["vr"].rank(method="first"), 3, labels=["calm", "mid", "hot"])
    D["vq"] = pd.qcut(D["vr"].rank(method="first"), 3, labels=["calm", "mid", "hot"])
    out["sig_by_volratio"] = S.groupby("vq").apply(summ)
    out["nosig_by_volratio"] = D[~D.sig].groupby("vq").apply(summ)
    hz = {}
    for col in ["ex24", "ex48", "ex72"]:
        x = S[col].dropna(); hz[col] = [len(x), 100 * x.mean(), x.mean() / (x.std() / np.sqrt(len(x)))]
    out["sig_horizons"] = pd.DataFrame(hz, index=["n", "mean%", "t"]).T
    top = S[S.fq == 4]
    hz = {}
    for col in ["ex24", "ex48", "ex72"]:
        x = top[col].dropna(); hz[col] = [len(x), 100 * x.mean(), x.mean() / (x.std() / np.sqrt(len(x)))]
    out["topq_horizons"] = pd.DataFrame(hz, index=["n", "mean%", "t"]).T
    # book
    dd = []
    for c, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = c; d["win"] = w; dd.append(d)
    DD = pd.concat(dd)
    DD["wn"] = DD["win"].str[1:].astype(int)
    B = DD.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().dropna().sort_index()
    out["book_vs_hold"] = pd.DataFrame({"mean%": 100 * B.mean(), "sd%": 100 * B.std(),
                                        "sharpe": B.mean() / B.std() * np.sqrt(365)})
    v = (1 + B["book_return"]).cumprod(); dpk = v / v.cummax() - 1
    out["book_maxdd"] = float(dpk.min())
    out["book_by_window"] = B.groupby(level=0).apply(lambda g: pd.Series({"book%": 100 * g.book_return.mean(), "hold%": 100 * g.coin_return.mean()})).T
    # allocation & trades
    al = []
    for c, wins in data["bars"].items():
        for w, b in wins.items():
            al.append(b["postRebalance_current_allocation"].values)
    al = np.concatenate(al)
    out["alloc"] = pd.Series({"mean": al.mean(), "share_nonzero": (np.abs(al) > 1e-6).mean(), "mean_when_on": al[np.abs(al) > 1e-6].mean()})
    T = pd.concat([t.assign(coin=c) for c, wins in data["trades"].items() for w, t in wins.items()])
    out["trades"] = pd.Series({"n": len(T), "mean_pl%": T["profit_loss_percent"].mean(), "mean_net%": T["net_profit_loss_percent"].mean(),
                               "mean_dur_h": T["duration_minutes"].mean() / 60, "median_dur_h": T["duration_minutes"].median() / 60})
    return out
