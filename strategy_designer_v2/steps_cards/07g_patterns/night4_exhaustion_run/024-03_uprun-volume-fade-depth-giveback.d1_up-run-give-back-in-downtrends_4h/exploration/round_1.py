def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    barrows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            fwd = c.shift(-H) / c - 1
            mabs = r1.abs().rolling(180, min_periods=60).mean()
            sma = c.rolling(180, min_periods=60).mean()
            dev = c / sma - 1
            ret6 = c / c.shift(6) - 1
            ret18 = c / c.shift(18) - 1
            vol30 = r1.rolling(180, min_periods=60).std()
            vol6 = r1.rolling(6, min_periods=6).std()
            # streak
            sgn = np.sign(r1.fillna(0)).values
            streak = np.zeros(len(b)); sgain = np.zeros(len(b))
            for i in range(1, len(b)):
                if sgn[i] != 0 and sgn[i] == sgn[i-1] and streak[i-1] != 0:
                    streak[i] = streak[i-1] + sgn[i]
                elif sgn[i] != 0:
                    streak[i] = sgn[i]
            n = np.abs(streak).astype(int)
            logc = np.log(c.values)
            for i in range(len(b)):
                if n[i] > 0 and i - n[i] >= 0:
                    sgain[i] = logc[i] - logc[i - n[i]]
            vfade = np.log(v.rolling(3).mean() / v.rolling(18).mean())
            hr = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "fwd": fwd, "r1n": r1.shift(-1),
                               "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                               "z_streak": sgain / mabs, "streak": streak, "dev": dev,
                               "z6": ret6 / (mabs * np.sqrt(6)), "z18": ret18 / (mabs * np.sqrt(18)),
                               "volratio": vol6 / vol30, "vfade": vfade, "r1": r1,
                               "hour": hr.dt.hour, "wd": hr.dt.weekday, "year": hr.dt.year})
            barrows.append(df)
    A = pd.concat(barrows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["ufwd"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0)].dropna(subset=["ufwd"])
    def tab(g, key, q=5):
        g = g.dropna(subset=[key]).copy()
        g["b"] = pd.qcut(g[key].rank(method="first"), q, labels=False)
        out = g.groupby("b")["ufwd"].agg(["mean", "count", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["key_mean"] = g.groupby("b")[key].mean()
        return out.drop(columns="std").round(5)
    res = {}
    res["fc_active_vs_flat"] = G.assign(act=G.fc < 0).groupby("act")["ufwd"].agg(["mean", "count", "std"]).round(5)
    res["z18_past3d_quint"] = tab(G, "z18")
    res["z6_past1d_quint"] = tab(G, "z6")
    res["dev_sma_quint"] = tab(G, "dev")
    res["volratio_quint"] = tab(G, "volratio")
    res["streak_z_quint"] = tab(G, "z_streak")
    up = G[(G.streak >= 3)]; dn = G[(G.streak <= -3)]
    res["uprun3_vfade_quint"] = tab(up, "vfade", 3)
    res["dnrun3_vfade_quint"] = tab(dn, "vfade", 3)
    res["z18_below_sma"] = tab(G[G.dev < 0], "z18")
    res["z18_above_sma"] = tab(G[G.dev > 0], "z18")
    # hour/weekday on 1-bar returns, non-overlapping naturally
    B = A.dropna(subset=["r1n"])
    hh = B.groupby("hour")["r1n"].agg(["mean", "count", "std"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    res["next_bar_by_hour"] = hh.round(6)
    B2 = A.dropna(subset=["r1"])
    wd = B2.groupby("wd")["r1"].agg(["mean", "count", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    res["bar_ret_by_weekday"] = wd.round(6)
    yy = G.groupby(["year"])["ufwd"].agg(["mean", "count"])
    res["by_year_uncond"] = yy.round(5)
    # book
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin, w=w))
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    res["book_by_window"] = bk.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count")).round(5)
    act = A[A.alloc.abs() > 0]
    res["active_short_gain"] = pd.Series({"bars": len(act), "share_bars": len(act) / len(A),
                                          "mean_gain_bar": (act.alloc * act.r1n).mean(),
                                          "mean_alloc": act.alloc.mean()})
    return res
