def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        g48 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            g48 += list(c[idx + 48] / c[idx] - 1)
        drift[coin] = np.mean(g48); usual[coin] = np.std(g48)
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            n = len(c)
            for kind, wd in (("weekend", 6), ("midweek", 1)):  # Sun 23:00 -> Mon 00:00 ; Tue 23:00 -> Wed 00:00
                pos = np.where((ts.dt.weekday.values == wd) & (ts.dt.hour.values == 23))[0]
                for p in pos:
                    if p - 48 < 0:
                        continue
                    past = c[p] / c[p - 48] - 1
                    r = {"coin": coin, "w": w, "year": ts.iloc[p].year, "kind": kind,
                         "past": past, "past_z": past / usual[coin]}
                    for h in (24, 48, 72, 120):
                        r[f"f{h}"] = c[p + h] / c[p] - 1 if p + h < n else np.nan
                    r["u48"] = r["f48"] - drift[coin] if not np.isnan(r["f48"]) else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    d["side"] = np.where(d["past"] > 0, "rise", "fall")
    # signed reversal: positive = reversal
    d["rev48"] = -np.sign(d["past"]) * d["u48"]
    def summ(g, col="rev48"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by_kind_side"] = d.groupby(["kind", "side"]).apply(summ)
    d["q"] = d.groupby("kind")["past_z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["by_kind_quintile_u48_raw"] = d.groupby(["kind", "q"]).apply(lambda g: pd.Series({
        "n": g["u48"].notna().sum(), "past_z": g["past_z"].mean(), "mean_u48": g["u48"].mean(),
        "t": g["u48"].mean() / (g["u48"].std() / np.sqrt(g["u48"].notna().sum()))}))
    wr = d[(d.kind == "weekend") & (d.side == "rise")]
    out["weekend_rise_by_coin"] = wr.groupby("coin").apply(summ)
    out["weekend_rise_by_year"] = wr.groupby("year").apply(summ)
    hz = {}
    for kind in ("weekend", "midweek"):
        for h in (24, 48, 72, 120):
            for side in ("rise", "fall"):
                g = d[(d.kind == kind) & (d.side == side)]
                dr = {k: v * h / 48 for k, v in drift.items()}
                x = (-np.sign(g["past"]) * (g[f"f{h}"] - g["coin"].map(dr))).dropna()
                hz[f"{kind}_{side}_h{h}"] = [len(x), x.mean(), x.mean() / (x.std() / np.sqrt(len(x)))]
    out["horizons_rev"] = pd.DataFrame(hz, index=["n", "mean", "t"]).T
    sl = {}
    for kind in ("weekend", "midweek"):
        g = d[d.kind == kind].dropna(subset=["u48"])
        res = stats.linregress(g["past_z"], g["u48"])
        sl[kind] = [len(g), res.slope, res.slope / res.stderr]
    out["slope_u48_on_pastz"] = pd.DataFrame(sl, index=["n", "slope", "t"]).T
    return out
