def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for H in (1, 3, 5, 10):
            rets = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                rets += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = (np.mean(rets), np.std(rets, ddof=1))
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd30 = r.rolling(30).std()
            ratio = ((b["high"] - b["low"]) / c) / sd30
            tr60 = c / c.shift(60) - 1
            sd365med = sd30.rolling(365, min_periods=120).median()
            agit = sd30 > sd365med
            closeup = c > b["open"]
            ret5 = c / c.shift(5) - 1
            n = len(b)
            for i in range(0, n):
                if not (tr60.iloc[i] < -0.10 and ratio.iloc[i] >= 2.0):
                    continue
                d = {"coin": coin, "w": w, "i": i, "ratio": ratio.iloc[i],
                     "closeup": bool(closeup.iloc[i]), "agit": bool(agit.iloc[i]),
                     "ret5": ret5.iloc[i], "tr60": tr60.iloc[i],
                     "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "day": pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                     "dayret": r.iloc[i]}
                for H in (1, 3, 5, 10):
                    if i + H < n:
                        m, s = drift[(coin, H)]
                        fr = c.iloc[i + H] / c.iloc[i] - 1
                        d[f"u{H}"] = -(fr - m)  # short direction
                        d[f"s{H}"] = d[f"u{H}"] / s
                    else:
                        d[f"u{H}"] = np.nan
                # grid cell for H=3
                d["cell3"] = i // 3
                rows.append(d)
    df = pd.DataFrame(rows)
    # one per grid cell of 3
    g = df.sort_values("i").groupby(["coin", "w", "cell3"]).head(1)

    def stat(x, col="u3"):
        x = x.dropna(subset=[col])
        s = x.groupby("day")[col].sum() - x[col].mean() * x.groupby("day")[col].size()
        D = len(s); n = len(x)
        se = np.sqrt((s ** 2).sum() * D / max(D - 1, 1)) / n if n else np.nan
        return pd.Series({"n": n, "days": D, "mean": x[col].mean(), "t": x[col].mean() / se if se else np.nan})

    out = {}
    out["all_by_horizon"] = pd.DataFrame({f"u{H}": stat(g, f"u{H}") for H in (1, 3, 5, 10)}).T
    out["by_coin"] = g.groupby("coin").apply(stat)
    out["by_window"] = g.groupby("w").apply(stat)
    out["by_year"] = g.groupby("year").apply(stat)
    out["by_closeup"] = g.groupby("closeup").apply(stat)
    out["by_agit"] = g.groupby("agit").apply(stat)
    g["rq"] = pd.qcut(g["ratio"], 4, labels=False)
    out["by_ratio_q"] = g.groupby("rq").apply(lambda x: pd.concat([stat(x), pd.Series({"ratio_med": x["ratio"].median()})]))
    g["dq"] = pd.qcut(g["dayret"], 4, labels=False)
    out["by_dayret_q"] = g.groupby("dq").apply(lambda x: pd.concat([stat(x), pd.Series({"dr_med": x["dayret"].median()})]))
    g["tq"] = pd.qcut(g["tr60"], 3, labels=False)
    out["by_trend60_tercile"] = g.groupby("tq").apply(lambda x: pd.concat([stat(x), pd.Series({"tr_med": x["tr60"].median()})]))
    out["corr_ratio_u3"] = float(g[["ratio", "u3"]].corr().iloc[0, 1])
    out["by_closeup_h10"] = g.groupby("closeup").apply(lambda x: stat(x, "u10"))
    return out
