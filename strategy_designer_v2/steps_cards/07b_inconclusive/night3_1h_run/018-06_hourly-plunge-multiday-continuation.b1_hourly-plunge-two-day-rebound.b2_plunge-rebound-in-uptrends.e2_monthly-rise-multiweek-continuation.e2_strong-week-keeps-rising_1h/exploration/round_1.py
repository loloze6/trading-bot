def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 168
    hs = [24, 72, 168, 336]
    rows = []
    usual = {}
    for coin, wins in bars.items():
        # normal drift and usual move per horizon: non-overlapping grid of all windows
        drift = {}
        for h in hs:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(list(c[idx + h] / c[idx] - 1))
            rr = np.array(rr)
            drift[h] = (rr.mean(), rr.std())
        usual[coin] = {h: drift[h][1] for h in hs}
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            low = 0.0
            seen = set()
            for i in range(n):
                if f[i] <= 0:
                    low = 0.0
                    continue
                if f[i] - low >= 2:
                    cell = i // H
                    low = f[i]
                    if cell in seen:
                        continue
                    seen.add(cell)
                    if i + H >= n:
                        continue
                    r = {"coin": coin, "win": w, "year": ts.iloc[i].year, "fc": f[i]}
                    for h in hs:
                        if i + h < n:
                            r["u%d" % h] = c[i + h] / c[i] - 1 - drift[h][0]
                            r["z%d" % h] = r["u%d" % h] / drift[h][1]
                    r["ret720"] = c[i] / c[i - 720] - 1 if i >= 720 else np.nan
                    r["ret168"] = c[i] / c[i - 168] - 1 if i >= 168 else np.nan
                    r["ret1"] = c[i] / c[i - 1] - 1 if i >= 1 else np.nan
                    rows.append(r)
                else:
                    low = min(low, f[i])
    d = pd.DataFrame(rows)

    def summ(g, col="u168"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["all"] = summ(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fcb"] = pd.cut(d["fc"], [0, 5, 10, 19.99, 20.01])
    out["by_fc"] = d.groupby("fcb").apply(summ)
    hz = []
    for h in hs:
        s = summ(d, "u%d" % h)
        s["h"] = h
        s["z"] = d["z%d" % h].mean()
        hz.append(s)
    out["by_horizon"] = pd.DataFrame(hz)
    d["trend30"] = np.where(d["ret720"].isna(), "na",
                            np.where(d["ret720"] > 0, "30d_up", "30d_down"))
    out["by_30d_trend"] = d.groupby("trend30").apply(summ)
    d["wk_q"] = pd.qcut(d["ret168"], 4, labels=["q1", "q2", "q3", "q4"])
    out["by_week_ret_quartile"] = d.groupby("wk_q").apply(summ)
    out["by_week_ret_q_mean_ret168"] = d.groupby("wk_q")["ret168"].mean()
    out["signal_bar_move_mean%"] = 100 * d["ret1"].mean()
    out["trend30_x_fc"] = d.groupby(["trend30", "fcb"]).apply(summ)
    return out
