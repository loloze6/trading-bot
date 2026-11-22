def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            absmv = r.abs().rolling(180, min_periods=45).mean()
            sd = r.rolling(180, min_periods=45).std()
            sd_long = r.rolling(540, min_periods=90).std()
            # streak
            sgn = np.sign(r.fillna(0)).values
            streak = np.zeros(len(b)); s = 0
            for i in range(len(b)):
                if sgn[i] == 0: s = 0
                elif s != 0 and np.sign(s) == sgn[i]: s += sgn[i]
                else: s = sgn[i]
                streak[i] = s
            ret6 = c / c.shift(6) - 1
            ret18p = c / c.shift(18) - 1
            ret42 = c / c.shift(42) - 1
            ret180 = c / c.shift(180) - 1
            vrat = v.rolling(6).mean() / v.rolling(180, min_periods=45).mean()
            rng = (b["high"] - b["low"]) / c
            rngr = rng / rng.rolling(180, min_periods=45).mean()
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            d = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.values[idx], "fwd6": fwd6.values[idx],
                "z6": (ret6 / (sd * np.sqrt(6))).values[idx],
                "z18": (ret18p / (sd * np.sqrt(18))).values[idx],
                "z42": (ret42 / (sd * np.sqrt(42))).values[idx],
                "z180": (ret180 / (sd * np.sqrt(180))).values[idx],
                "volreg": (sd / sd_long).values[idx], "volabs": sd.values[idx],
                "streak": streak[idx], "vrat": vrat.values[idx], "rngr": rngr.values[idx],
                "hour": ts.dt.hour.values[idx], "wd": ts.dt.dayofweek.values[idx],
                "year": ts.dt.year.values[idx],
                "fc": b["forecast"].values[idx],
                "pos": b["postRebalance_current_allocation"].values[idx],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["fwd"])
    drift = D.groupby("coin")["fwd"].transform("mean")
    usual = D.groupby("coin")["fwd"].transform("std")
    D["ex"] = D["fwd"] - drift
    D["exs"] = D["ex"] / usual
    out = {}
    def grp(col, q=5):
        x = D.dropna(subset=[col])
        g = pd.qcut(x[col], q, duplicates="drop")
        a = x.groupby(g, observed=True)["exs"].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["ex_pct"] = x.groupby(g, observed=True)["ex"].mean() * 100
        return a.drop(columns="std").round(4)
    for col in ["z6", "z18", "z42", "z180", "volreg", "vrat", "rngr"]:
        out["by_" + col] = grp(col)
    def corr(col):
        x = D.dropna(subset=[col, "exs"])
        rr, p = stats.spearmanr(x[col], x["exs"])
        return pd.Series({"rho": rr, "p": p, "n": len(x)})
    out["spearman"] = pd.DataFrame({c: corr(c) for c in ["z6","z18","z42","z180","volreg","vrat","rngr","streak"]}).T.round(4)
    st = D.copy(); st["sk"] = st["streak"].clip(-6, 6)
    a = st.groupby("sk")["exs"].agg(["mean","count","std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["by_streak"] = a.drop(columns="std").round(4)
    for col in ["hour", "wd", "year"]:
        a = D.groupby(col)["exs"].agg(["mean","count","std"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
        out["by_" + col] = a.drop(columns="std").round(4)
    a = D.groupby("coin")[["exs"]].agg(["mean","count"]); out["by_coin"] = a.round(4)
    # z42 by coin rho
    out["z42_rho_by_coin"] = D.dropna(subset=["z42"]).groupby("coin").apply(lambda x: stats.spearmanr(x["z42"], x["exs"])[0]).round(4)
    out["z180_rho_by_coin"] = D.dropna(subset=["z180"]).groupby("coin").apply(lambda x: stats.spearmanr(x["z180"], x["exs"])[0]).round(4)
    # book: daily
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    DD["active"] = DD["book_return"].abs() > 1e-9
    out["book_active_share"] = float(DD["active"].mean())
    act = DD[DD["active"]]
    out["book_active_mean_vs_coin"] = pd.Series({"book": act["book_return"].mean(), "coin_same_days": act["coin_return"].mean(), "coin_all": DD["coin_return"].mean(), "n": len(act)})
    # largest book days: coin return the day before
    DD = DD.sort_values(["coin","win","day"])
    DD["coin_prev"] = DD.groupby(["coin","win"])["coin_return"].shift(1)
    DD["coin_prev3"] = DD.groupby(["coin","win"])["coin_return"].transform(lambda s: s.shift(1).rolling(3).sum())
    q = DD["book_return"].quantile([0.01, 0.99])
    big = pd.DataFrame({
        "worst1%": DD[DD["book_return"] <= q.iloc[0]][["book_return","coin_return","coin_prev","coin_prev3"]].mean(),
        "best1%": DD[DD["book_return"] >= q.iloc[1]][["book_return","coin_return","coin_prev","coin_prev3"]].mean()})
    out["book_extremes"] = big.round(4)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["mean","count","median"]).round(3)
    return out
