def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [1, 3, 5, 7, 10]
    out = {}
    drift = {}
    for c, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                cl = b["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = (np.mean(rs), np.std(rs))
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            cl = b["close"].values
            inprof = (b["regime"] == "unknown").values
            n = len(b)
            minpos = 0.0
            last_case_cell = -1
            for i in range(n):
                if f[i] <= 0:
                    minpos = 0.0
                    continue
                cell = i // 3
                is_case = (f[i] - minpos >= 2) and cell != last_case_cell
                if is_case:
                    last_case_cell = cell
                    minpos = f[i]
                else:
                    minpos = min(minpos, f[i]) if minpos > 0 else f[i]
                if is_case:
                    d = {"coin": c, "win": w, "i": i, "f": f[i], "day": str(b["timestamp"].iloc[i])[:10],
                         "year": pd.Timestamp(b["timestamp"].iloc[i]).year}
                    for h in H:
                        if i + h < n:
                            d["u%d" % h] = cl[i + h] / cl[i] - 1 - drift[(c, h)][0]
                    rows.append(d)
    df = pd.DataFrame(rows)
    def tday(s, days):
        x = pd.DataFrame({"v": s.values, "d": days.values}).dropna()
        if len(x) < 3: return np.nan
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(x)
        return m / se
    def summ(g):
        r = {"n": len(g)}
        for h in H:
            col = "u%d" % h
            r["mean_" + col] = g[col].mean()
            r["t_" + col] = tday(g[col], g["day"])
        return pd.Series(r)
    out["all"] = summ(df)
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_fquart"] = df.groupby("fq").apply(summ)
    out["by_win"] = df.groupby("win").apply(lambda g: pd.Series({"n": len(g), "m3": g["u3"].mean(), "m7": g["u7"].mean()}))
    # non-case profile bars: forecast 0 inside profile (coin down over 7 days), grid 3
    nr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            ip = (b["regime"] == "unknown").values
            for i in range(0, len(cl) - 3, 3):
                if ip[i]:
                    nr.append({"pos": f[i] > 0, "u3": cl[i + 3] / cl[i] - 1 - drift[(c, 3)][0],
                               "u7": (cl[i + 7] / cl[i] - 1 - drift[(c, 7)][0]) if i + 7 < len(cl) else np.nan})
    nr = pd.DataFrame(nr)
    out["profile_grid_by_fpos"] = nr.groupby("pos").agg(n=("u3", "size"), m3=("u3", "mean"), m7=("u7", "mean"))
    out["usual_moves"] = pd.Series({f"{k[0]}_{k[1]}": v[1] for k, v in drift.items() if k[1] == 3})
    return out
