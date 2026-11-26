def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 30
    drift = {}; usual = {}
    for c in bars:
        r = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - H, H):
                r.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(r); usual[c] = np.std(r, ddof=1)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            cl = df["close"].values
            ts = pd.to_datetime(df["timestamp"])
            low = 0.0; taken = set(); n = len(df)
            for i in range(n):
                low = min(low, f[i])
                if f[i] - low >= 2:
                    cell = i // H; low = f[i]
                    if cell in taken: continue
                    taken.add(cell)
                    if i + H >= n: continue
                    rec = {"coin": c, "day": ts[i].normalize(), "fc": f[i],
                           "u30": cl[i + H] / cl[i] - 1 - drift[c]}
                    rec["s30"] = rec["u30"] / usual[c]
                    for k in (10, 20, 30):
                        rec[f"p{k}"] = cl[i] / cl[i - k] - 1 if i >= k else np.nan
                    # off-low: close vs 30-day low
                    lo = cl[max(0, i - 30):i + 1].min()
                    rec["offlow"] = cl[i] / lo - 1
                    rec["offlow_bars"] = i - max(0, i - 30) - int(np.argmin(cl[max(0, i - 30):i + 1]))
                    rows.append(rec)
    d = pd.DataFrame(rows)

    def tday(x, col="u30"):
        x = x.dropna(subset=[col])
        m = x[col].mean()
        g = (x[col] - m).groupby(x["day"]).sum(); G = len(g)
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(x) if G > 1 else np.nan
        return pd.Series({"n": len(x), "mean": m, "median": x[col].median(), "t": m / se, "days": G,
                          "share_pos": (x[col] > 0).mean()})

    out = {}
    out["all"] = tday(d).to_frame().T
    out["excl_XRP"] = tday(d[d.coin != "XRPUSD"]).to_frame().T
    top = d["u30"].sort_values(ascending=False)
    out["top5_sum_share_of_total"] = float(top.head(5).sum() / d["u30"].sum())
    for k in ("p10", "p20", "p30", "offlow", "offlow_bars"):
        x = d[[k, "u30", "s30"]].dropna()
        out[f"spearman_{k}"] = float(stats.spearmanr(x[k], x["s30"])[0])
    x = d.dropna(subset=["offlow"]).copy()
    x["q"] = pd.qcut(x["offlow"].rank(method="first"), 3, labels=["at_low", "mid", "off_low"])
    out["by_offlow"] = x.groupby("q").apply(lambda y: pd.concat([tday(y), pd.Series({"offlow": y["offlow"].mean(), "s30m": y["s30"].mean()})]))
    x = d.dropna(subset=["p30"]).copy()
    x["q"] = pd.qcut(x["p30"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_p30_quart"] = x.groupby("q").apply(lambda y: pd.concat([tday(y), pd.Series({"p30": y["p30"].mean(), "s30m": y["s30"].mean()})]))
    out["by_p30_quart_exXRP"] = x[x.coin != "XRPUSD"].groupby("q").apply(lambda y: tday(y))
    x["up"] = x["p30"] > 0
    out["p30_pos_vs_neg"] = x.groupby("up").apply(lambda y: tday(y))
    return out
