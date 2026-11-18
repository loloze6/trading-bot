def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vsr = (c / c.shift(10) - 1) / (r1.rolling(20).std() * np.sqrt(10))
            rng = (b["high"] - b["low"]) / c
            comp = rng.rolling(10).mean() / rng.rolling(60, min_periods=30).mean()
            volr = b["volume"].rolling(10).mean() / b["volume"].rolling(60, min_periods=30).mean()
            vol20 = r1.rolling(20).std()
            vol20r = vol20 / r1.rolling(120, min_periods=60).std()
            ret1 = r1
            fwd3 = c.shift(-3) / c - 1
            idx = np.arange(0, len(b), 3)
            g = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["forecast"].values[idx],
                "vsr": vsr.values[idx],
                "comp": comp.values[idx],
                "volr": volr.values[idx],
                "vol20r": vol20r.values[idx],
                "r1": ret1.values[idx],
                "fwd3": fwd3.values[idx],
                "absfwd3": np.abs(fwd3.values[idx]),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx],
                "year": pd.to_datetime(b["timestamp"]).dt.year.values[idx],
            })
            rows.append(g)
    G = pd.concat(rows).dropna(subset=["fwd3"])
    G["ex"] = G["fwd3"] - G.groupby("coin")["fwd3"].transform("mean")
    G["absn"] = G["absfwd3"] / G.groupby("coin")["absfwd3"].transform("mean")

    def tab(col, q=5, val="ex"):
        d = G.dropna(subset=[col]).copy()
        d["q"] = pd.qcut(d[col], q, labels=False, duplicates="drop")
        a = d.groupby("q")[val].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["lo"] = d.groupby("q")[col].min()
        return a.round(4)

    out["vsr_quint_ex"] = tab("vsr")
    out["r1_quint_ex"] = tab("r1")
    out["comp_quint_absn"] = tab("comp", val="absn")
    out["comp_quint_ex"] = tab("comp")
    out["volr_quint_ex"] = tab("volr")
    out["vol20r_quint_ex"] = tab("vol20r")
    out["vol20r_quint_absn"] = tab("vol20r", val="absn")
    wd = G.groupby("wd")["ex"].agg(["mean", "count"]); wd["t"] = wd["mean"] / (G.groupby("wd")["ex"].std() / np.sqrt(wd["count"]))
    out["weekday_ex"] = wd.round(4)
    # top group by year and coin
    d = G[G.fc > 0]; cut = d.fc.quantile(0.8); T = G[G.fc >= cut]
    yr = T.groupby("year")["ex"].agg(["mean", "count"]); out["top_by_year"] = yr.round(4)
    out["top_by_coin"] = T.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    # book: market vs timing
    D = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            bb = data["bars"][coin][w]
            pos = bb.groupby(pd.to_datetime(bb["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].last().shift(1).values
            x = dd.copy(); x["pos"] = pos[:len(x)]; x["coin"] = coin; x["win"] = w
            D.append(x)
    D = pd.concat(D)
    D["mu"] = D.groupby("coin")["coin_return"].transform("mean")
    bk = D.groupby("day")[["book_return"]].mean()
    D["mkt"] = D["pos"] * D["mu"]
    out["book_mean"] = float(D.groupby("day")["book_return"].mean().mean())
    out["book_mkt_part"] = float(D.groupby("day")["mkt"].mean().mean())
    out["mean_pos"] = float(D["pos"].mean())
    out["book_by_win"] = D.groupby("win")["book_return"].mean().round(5).to_frame().T
    return out
