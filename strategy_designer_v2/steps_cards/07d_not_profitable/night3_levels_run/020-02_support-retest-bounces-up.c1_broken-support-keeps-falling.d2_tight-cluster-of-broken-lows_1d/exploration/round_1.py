def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    grid = []
    for coin, wins in data["bars"].items():
        # coin mean 5-bar return over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            allr += list(c[idx + 5] / c[idx] - 1)
        mu5 = np.mean(allr)
        dr = []
        for w, b in wins.items():
            c = b["close"].values
            dr += list(c[1:] / c[:-1] - 1)
        mud = np.mean(dr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            pos = b["postRebalance_current_allocation"].fillna(0)
            g = pos * (c.shift(-1) / c - 1)
            rows.append(pd.DataFrame({"coin": coin, "win": w, "pos": pos, "gain": g,
                                      "mkt": pos * mud, "year": pd.to_datetime(b["timestamp"]).dt.year,
                                      "fc": b["forecast"]}))
            cv = c.values
            idx = np.arange(0, len(cv) - 5, 5)
            # trailing 60-day return & 20-day return at grid
            r60 = (c / c.shift(60) - 1).values
            r20 = (c / c.shift(20) - 1).values
            ma = (c / c.rolling(50).mean() - 1).values
            grid.append(pd.DataFrame({"coin": coin, "win": w, "fc": b["forecast"].values[idx],
                                      "f5": cv[idx + 5] / cv[idx] - 1, "ex": cv[idx + 5] / cv[idx] - 1 - mu5,
                                      "r60": r60[idx], "r20": r20[idx], "ma50": ma[idx],
                                      "year": pd.to_datetime(b["timestamp"]).dt.year.values[idx]}))
    R = pd.concat(rows); G = pd.concat(grid)
    out["exposure"] = pd.Series({"mean_pos": R.pos.mean(), "share_short": (R.pos < -0.01).mean(),
                                 "mean_gain_bar": R.gain.mean(), "market_part": R.mkt.mean(),
                                 "timing_part": R.gain.mean() - R.mkt.mean()})
    out["by_year"] = R.groupby("year").agg(pos=("pos", "mean"), gain=("gain", "mean"), mkt=("mkt", "mean"))
    out["by_coin"] = R.groupby("coin").agg(pos=("pos", "mean"), gain=("gain", "mean"), mkt=("mkt", "mean"))
    nz = G[G.fc < 0].copy()
    nz["q"] = pd.qcut(-nz.fc, 3, labels=["small", "mid", "large"])
    out["fc_terciles"] = nz.groupby("q").agg(n=("ex", "size"), ex=("ex", "mean"), raw=("f5", "mean"))
    out["zero_fc"] = pd.Series({"n": (G.fc == 0).sum(), "ex": G[G.fc == 0].ex.mean(), "raw": G[G.fc == 0].f5.mean()})
    # by trend state among short cases
    for k in ["r60", "ma50"]:
        s = nz.dropna(subset=[k]).copy()
        s["t"] = pd.qcut(s[k], 4, labels=["q1low", "q2", "q3", "q4high"])
        out["short_by_" + k] = s.groupby("t").agg(n=("ex", "size"), raw=("f5", "mean"), ex=("ex", "mean"),
                                                   k=(k, "mean"))
        a = G.dropna(subset=[k]).copy()
        a["t"] = pd.qcut(a[k], 4, labels=["q1low", "q2", "q3", "q4high"])
        out["all_by_" + k] = a.groupby("t").agg(n=("ex", "size"), raw=("f5", "mean"), ex=("ex", "mean"))
    # interaction: in downtrend (r60<0), slope of ex on short size
    for nm, s in [("down", G[G.r60 < 0]), ("up", G[G.r60 >= 0])]:
        s = s.dropna(subset=["ex"])
        x = -s.fc / 10
        sl = stats.linregress(x, s.ex)
        out["slope_" + nm] = pd.Series({"n": len(s), "slope": sl.slope, "t": sl.slope / sl.stderr,
                                        "raw_mean_short": s[s.fc < 0].f5.mean(), "n_short": (s.fc < 0).sum()})
    return out
