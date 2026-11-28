import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    H = (1, 3, 5, 7, 10)
    for coin, wins in data["bars"].items():
        rets = {h: [] for h in H}
        for w, b in wins.items():
            c = b["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                rets[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        drift[coin]["sd3"] = np.std(rets[3], ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; f = b["forecast"].fillna(0).values
            col = "debug_info.components.scaled_week_rise.last_history_value"
            raw = b[col].values if col in b.columns else np.full(len(b), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            low = 0.0
            taken = set()
            for t in range(len(b)):
                if f[t] <= 0:
                    low = 0.0; continue
                if f[t] - low >= 2:
                    cell = t // 3
                    if cell not in taken:
                        taken.add(cell)
                        r = {"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(),
                             "fc": f[t], "raw": raw[t]}
                        for h in H:
                            r[f"u{h}"] = (c[t+h]/c[t]-1 - drift[coin][h]) if t+h < len(c) else np.nan
                            r[f"tot{h}"] = (c[t+h]/c[t]-1) if t+h < len(c) else np.nan
                        r["prior7"] = c[t]/c[t-7]-1 if t >= 7 else np.nan
                        r["prior1"] = c[t]/c[t-1]-1 if t >= 1 else np.nan
                        rows.append(r)
                    low = f[t]
                else:
                    low = min(low, f[t])
    df = pd.DataFrame(rows)

    def summ(g, col="u3"):
        x = g[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series({"n": n, "days": np.nan, "mean": x.mean() if n else np.nan, "t": np.nan})
        d = g.loc[x.index].groupby("day")[col].apply(lambda s: (s - x.mean()).sum())
        D = len(d)
        se = np.sqrt(D / (D - 1)) * np.sqrt((d ** 2).sum()) / n if D > 1 else np.nan
        return pd.Series({"n": n, "days": D, "mean": x.mean(), "t": x.mean() / se if se else np.nan})

    out = {}
    out["all_by_h"] = pd.DataFrame({k: summ(df, k) for k in ["u1", "u3", "u5", "u7", "u10", "tot3"]}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    out["by_win"] = df.groupby("win").apply(summ)
    df["fq"] = pd.qcut(df["fc"].rank(method="first"), 4, labels=False)
    out["by_fc_q"] = df.groupby("fq").apply(summ)
    out["fc_q_ranges"] = df.groupby("fq")["fc"].agg(["min", "max", "count"])
    out["by_fc_q_u7"] = df.groupby("fq").apply(lambda g: summ(g, "u7"))
    df["rq"] = pd.qcut(df["raw"].rank(method="first"), 4, labels=False)
    out["by_raw_q"] = df.groupby("rq").apply(summ)
    out["by_raw_q_u7"] = df.groupby("rq").apply(lambda g: summ(g, "u7"))
    df["p1pos"] = df["prior1"] > 0
    out["by_prior1_sign"] = df.groupby("p1pos").apply(summ)
    sl = {}
    for x in ["fc", "raw", "prior7"]:
        for y in ["u3", "u7"]:
            s = df[[x, y]].dropna()
            if len(s) > 5:
                res = stats.linregress(s[x], s[y])
                sl[f"{y}_on_{x}"] = {"slope": res.slope, "t": res.slope / res.stderr, "n": len(s)}
    out["slopes"] = pd.DataFrame(sl).T
    out["sd3"] = pd.Series({k: v["sd3"] for k, v in drift.items()})
    out["n_cases"] = len(df)
    return out
