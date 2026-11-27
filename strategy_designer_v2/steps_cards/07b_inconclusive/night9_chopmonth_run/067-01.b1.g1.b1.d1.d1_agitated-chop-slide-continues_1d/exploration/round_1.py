def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    H = [5, 10, 20]
    # drift per coin per horizon
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = (np.mean(rs) if rs else np.nan, np.std(rs, ddof=1) if len(rs) > 1 else np.nan)
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            r30 = pd.Series(cl).pct_change(30).values
            n = len(df)
            for start in range(0, n, 10):
                idx = [i for i in range(start, min(start + 10, n)) if fc[i] <= -2]
                if not idx:
                    continue
                i = idx[0]
                rec = {"coin": c, "window": w, "year": ts[i].year, "day": ts[i].normalize(),
                       "fc": fc[i], "r30": r30[i]}
                for h in H:
                    if i + h < n:
                        tot = -(cl[i + h] / cl[i] - 1)
                        rec[f"tot{h}"] = tot
                        rec[f"un{h}"] = tot + drift[(c, h)][0]
                    else:
                        rec[f"tot{h}"] = np.nan; rec[f"un{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def ct(s, days):
        x = pd.DataFrame({"v": s, "d": days}).dropna()
        if len(x) < 3:
            return np.nan, len(x), 0
        m = x["v"].mean()
        g = (x["v"] - m).groupby(x["d"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x)
        return m / se, len(x), G

    def summ(sub):
        res = {}
        for h in H:
            t, n, G = ct(sub[f"un{h}"].values, sub["day"].values)
            res[f"un{h}"] = sub[f"un{h}"].mean()
            res[f"tot{h}"] = sub[f"tot{h}"].mean()
            res[f"t{h}"] = t
        res["n"] = len(sub)
        res["days"] = sub["day"].nunique()
        return pd.Series(res)

    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ).round(4)
    out["by_window"] = d.groupby("window").apply(summ).round(4)
    out["by_year"] = d.groupby("year").apply(summ).round(4)
    d["fcq"] = pd.qcut(d["fc"].abs(), 4, labels=False, duplicates="drop")
    out["by_fc_quartile"] = d.groupby("fcq").apply(summ).round(4)
    d["r30q"] = pd.qcut(d["r30"], 4, labels=False, duplicates="drop")
    out["by_r30_quartile"] = d.groupby("r30q").apply(summ).round(4)
    out["r30_by_q_mean"] = d.groupby("r30q")["r30"].agg(["mean", "min", "max"]).round(3)
    out["spearman_fc_un10"] = float(d[["fc", "un10"]].dropna().corr("spearman").iloc[0, 1])
    out["drift10"] = pd.DataFrame({c: {"mean": drift[(c, 10)][0], "sd": drift[(c, 10)][1]} for c in bars}).T.round(4)
    return out
