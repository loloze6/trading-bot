def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H_list = [1, 2, 3, 5]
    drift = {}
    for coin, wins in bars.items():
        for H in H_list:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rr += list(c[idx + H] / c[idx] - 1)
            drift[(coin, H)] = np.mean(rr)
        rr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            rr += list(c[idx + 5] / c[idx] - 1)
        drift[(coin, "sd5")] = np.std(rr, ddof=1)
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; lo = df["low"]
            prior_low = lo.shift(1).rolling(20).min()
            depth = (c / prior_low - 1) * 100
            day = pd.to_datetime(df["timestamp"]).dt.floor("D")
            n = len(df)
            mr = (df["regime"] == "mean_reversion").values
            for i in range(n):
                if not mr[i]:
                    continue
                d = depth.iloc[i]
                if np.isnan(d):
                    d = df.get("debug_info.components.depth.last_history_value", pd.Series([np.nan]*n)).iloc[i]
                first = (i == 0) or (not mr[i - 1])
                rec = dict(coin=coin, w=w, day=day.iloc[i], depth=d, first=first,
                           fc=df["forecast"].iloc[i], year=day.iloc[i].year)
                for H in H_list:
                    rec[f"u{H}"] = (c.iloc[i + H] / c.iloc[i] - 1 - drift[(coin, H)]) if i + H < n else np.nan
                    rec[f"tot{H}"] = (c.iloc[i + H] / c.iloc[i] - 1) if i + H < n else np.nan
                recs.append(rec)
    R = pd.DataFrame(recs)

    def summ(d, col):
        d = d[d[col].notna()]
        if len(d) < 3:
            return pd.Series(dict(n=len(d), days=d["day"].nunique(), mean=d[col].mean() if len(d) else np.nan, t=np.nan))
        x = d[col]
        g = (x - x.mean()).groupby(d["day"]).sum()
        G = len(g)
        se = np.sqrt((g ** 2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series(dict(n=len(d), days=G, mean=x.mean(), t=x.mean() / se if se > 0 else np.nan))

    out = {}
    out["MR bars, all, by H (unusual)"] = pd.DataFrame({H: summ(R, f"u{H}") for H in H_list}).T
    out["MR first bar of each break episode, by H"] = pd.DataFrame({H: summ(R[R["first"]], f"u{H}") for H in H_list}).T
    R["dq"] = pd.qcut(R["depth"].rank(method="first"), 2, labels=["shallow", "deep"])
    rows = {}
    for q in ["shallow", "deep"]:
        for H in [1, 3, 5]:
            rows[(q, H)] = summ(R[R.dq == q], f"u{H}")
    out["MR by depth half"] = pd.DataFrame(rows).T
    rows = {}
    for coin in sorted(R.coin.unique()):
        rows[coin] = pd.concat([summ(R[R.coin == coin], "u1").add_prefix("h1_"), summ(R[R.coin == coin], "u5").add_prefix("h5_")])
    out["MR by coin"] = pd.DataFrame(rows).T
    rows = {}
    for y in sorted(R.year.unique()):
        rows[y] = pd.concat([summ(R[R.year == y], "u1").add_prefix("h1_"), summ(R[R.year == y], "u5").add_prefix("h5_")])
    out["MR by year"] = pd.DataFrame(rows).T
    for H in [1, 5]:
        d = R[R[f"u{H}"].notna()]
        out[f"spearman(-depth,u{H})"] = str(stats.spearmanr(-d.depth, d[f"u{H}"]))
        out[f"spearman(fc,u{H})"] = str(stats.spearmanr(d.fc, d[f"u{H}"]))
    out["sd5 mean over coins"] = float(np.mean([drift[(c_, "sd5")] for c_ in bars]))
    out["episodes count"] = int(R["first"].sum())
    return out
