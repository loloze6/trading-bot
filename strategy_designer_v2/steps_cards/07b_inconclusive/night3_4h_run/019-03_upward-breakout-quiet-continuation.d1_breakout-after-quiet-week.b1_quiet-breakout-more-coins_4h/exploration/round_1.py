def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        rets = {h: [] for h in (6, 18, 36)}
        for w, b in wins.items():
            c = b["close"].values
            for h in rets:
                idx = np.arange(0, len(c) - h, h)
                rets[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        usual[coin] = np.std(rets[18])
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; f = b["forecast"].fillna(0).values
            hi = b["high"].values; lo = b["low"].values
            rng = pd.Series((hi - lo) / c)
            q = rng.rolling(42).mean() / rng.rolling(360, min_periods=180).mean()
            ret30 = pd.Series(c).pct_change(180).values
            n = len(c)
            for g in range(0, n - H, H):
                for t in range(g, min(g + H, n - H)):
                    prev = f[t - 1] if t > 0 else 0
                    if f[t] >= 2 and prev < 2:
                        r = {"coin": coin, "win": w, "year": pd.Timestamp(b["timestamp"].iloc[t]).year,
                             "fc": f[t], "q": q.iloc[t], "ret30": ret30[t],
                             "u18": c[t + 18] / c[t] - 1 - drift[coin][18]}
                        for h in (6, 36):
                            r["u%d" % h] = (c[t + h] / c[t] - 1 - drift[coin][h]) if t + h < n else np.nan
                        r["nxt"] = c[t + 1] / c[t] - 1
                        rows.append(r); break
    d = pd.DataFrame(rows)
    def agg(g):
        x = g["u18"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "u6": g["u6"].mean(), "u36": g["u36"].mean()})
    out = {"all": agg(d).to_frame().T}
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_quint"] = d.groupby("fq").apply(agg)
    d["qq"] = pd.qcut(d["q"], 5, labels=False)
    out["by_quiet_quint(low=quiet)"] = d.groupby("qq").apply(agg)
    d["tq"] = pd.qcut(d["ret30"], 5, labels=False)
    out["by_30d_ret_quint"] = d.groupby("tq").apply(agg)
    out["fc_q_cross"] = d.groupby(["qq", "tq"])["u18"].mean().unstack()
    return out
