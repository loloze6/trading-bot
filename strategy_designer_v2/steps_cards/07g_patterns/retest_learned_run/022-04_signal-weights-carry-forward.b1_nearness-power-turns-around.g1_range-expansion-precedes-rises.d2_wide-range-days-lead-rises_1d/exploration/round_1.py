def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            idx = np.arange(0, len(b) - H, H)
            allr += list(c[idx + H] / c[idx] - 1)
        drift[coin] = (np.mean(allr), np.std(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            rng = (b["high"] - b["low"]) / b["close"]
            b["rr"] = (b["high"] - b["low"]) / (b["high"] - b["low"]).rolling(30, min_periods=10).mean()
            b["clv"] = ((b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)) * 2 - 1
            b["r1"] = b["close"].pct_change()
            b["r5"] = b["close"].pct_change(5)
            b["r20"] = b["close"].pct_change(20)
            b["vol20"] = b["r1"].rolling(20).std()
            b["volrel"] = b["vol20"] / b["r1"].rolling(60, min_periods=30).std()
            b["hi30"] = b["close"] / b["high"].rolling(30, min_periods=10).max() - 1
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            c = b["close"].values
            for i in range(0, len(b) - H, H):
                fr = c[i + H] / c[i] - 1
                d = b.iloc[i]
                rows.append(dict(coin=coin, win=w, fr=fr, ex=fr - drift[coin][0],
                                 exs=(fr - drift[coin][0]) / drift[coin][1],
                                 rr=d["rr"], clv=d["clv"], r1=d["r1"], r5=d["r5"], r20=d["r20"],
                                 volrel=d["volrel"], hi30=d["hi30"], wd=d["wd"], fc=d["forecast"]))
    df = pd.DataFrame(rows)
    out = {}
    def tq(col, q=5, sub=None):
        x = df if sub is None else sub
        x = x.dropna(subset=[col, "ex"])
        g = pd.qcut(x[col].rank(method="first"), q, labels=False)
        t = x.groupby(g)["ex"].agg(["mean", "count", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))])
        t.columns = ["mean_ex", "n", "t"]
        sl = stats.linregress(x[col], x["exs"])
        return t, sl.slope / sl.stderr
    for col in ["rr", "clv", "r1", "r5", "r20", "volrel", "hi30"]:
        t, st = tq(col)
        out[f"quint_{col}"] = t
        out[f"slope_t_std_{col}"] = round(st, 2)
    wide = df[df["rr"] > 1]
    t, st = tq("clv", 3, wide)
    out["wide_days_by_clv"] = t; out["wide_clv_slope_t"] = round(st, 2)
    wide2 = wide.dropna(subset=["r1"])
    t, st = tq("r1", 3, wide2)
    out["wide_days_by_r1"] = t; out["wide_r1_slope_t"] = round(st, 2)
    out["by_weekday"] = df.groupby("wd")["ex"].agg(["mean", "count"])
    out["by_coin_rr_slope"] = df.dropna(subset=["rr"]).groupby("coin").apply(
        lambda x: pd.Series({"slope_t": (lambda s: s.slope / s.stderr)(stats.linregress(x["rr"], x["exs"])), "n": len(x)}))
    # book
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; bd.append(d)
    bd = pd.concat(bd)
    bd["yr"] = pd.to_datetime(bd["day"]).dt.year
    out["book_by_year"] = bd.groupby("yr")[["book_return", "coin_return"]].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t)
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["mean", "count", "median"])
    out["n_cases"] = len(df)
    return out
