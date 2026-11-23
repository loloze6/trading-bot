def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    cr = []
    drift = {}
    for c in bars:
        vals_ = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - 24, 24)
            vals_.append(cl[idx + 24] / cl[idx] - 1)
        drift[c] = np.concatenate(vals_).mean()
    for c in bars:
        for w, b in bars[c].items():
            s = b["close"].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            hr = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            lr = np.log(s).diff()
            n = len(s)
            df = pd.DataFrame({"coin": c, "win": w, "f": b["forecast"].fillna(0).values,
                               "cell": np.arange(n) // 24, "r24": s.shift(-24) / s - 1,
                               "r168": s / s.shift(168) - 1, "r2": s / s.shift(2) - 1,
                               "r24p": s / s.shift(24) - 1, "r720": s / s.shift(720) - 1,
                               "vr": lr.rolling(24).std() / lr.rolling(720).std(),
                               "hr": hr, "year": ts.dt.year.values, "day": ts.dt.floor("D").values})
            df = df[np.isin(hr, [0, 16])].dropna(subset=["r24", "r168"])
            cr.append(df)
    C = pd.concat(cr)
    C["x"] = C["r24"] - C["coin"].map(drift)
    C["fall2"] = C["r2"] < 0
    C["runup"] = C["r168"] > 0
    def summ(g):
        return pd.Series({"n": len(g), "mean_r24": g["r24"].mean(), "mean_x": g["x"].mean(),
                          "t_x": g["x"].mean() / (g["x"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    first = lambda d: d.groupby(["coin", "win", "cell"]).head(1)
    sig = first(C[C["f"] > 0]).copy()
    nos = first(C[(C["f"] <= 0) & C["runup"]]).copy()   # run-up, no 2h fall
    q24 = sig["r24p"].quantile(0.2)
    sig["r24p_low"] = sig["r24p"] <= q24; nos["r24p_low"] = nos["r24p"] <= q24
    out["sig_by_r24plow"] = sig.groupby("r24p_low").apply(summ)
    out["cond_nofall_by_r24plow"] = nos.groupby("r24p_low").apply(summ)
    # graded 24h fall quintiles among no-fall-2h settlement bars with runup
    nos["q"] = pd.qcut(nos["r24p"].rank(method="first"), 5, labels=False)
    out["cond_nofall_by_r24p_q"] = nos.groupby("q").apply(summ)
    q168 = sig["r168"].quantile(0.6)
    sig["r168hi"] = sig["r168"] >= q168; nos["r168hi"] = nos["r168"] >= q168
    out["sig_by_r168hi"] = sig.groupby("r168hi").apply(summ)
    out["cond_nofall_by_r168hi"] = nos.groupby("r168hi").apply(summ)
    out["sig_by_hour_year"] = sig.groupby(["hr", "year"]).apply(summ)["mean_x"].unstack(0)
    out["cond_nofall_by_hour"] = nos.groupby("hr").apply(summ)
    # crude book per subset: day mean over coins of (r24 - cost) for cases, 0 else
    ncoin = C.groupby("day")["coin"].nunique()
    def book(g):
        r = (g["r24"] - 0.0022).groupby(g["day"]).sum() / 24.0  # 24h hold spread on 1/24-ish exposure
        r = r.reindex(ncoin.index).fillna(0) / ncoin * 1.0
        r = r.sort_index()
        v = (1 + r).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(r) / 365
        ann = v.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"ann": ann, "maxdd": dd, "calmar": ann / -dd if dd < 0 else np.nan,
                          "sharpe": r.mean() / r.std() * np.sqrt(365)})
    subs = {"all": sig, "hr16": sig[sig["hr"] == 16], "r24p_low": sig[sig["r24p_low"]],
            "r168hi": sig[sig["r168hi"]], "r720pos": sig[sig["r720"] > 0],
            "r24pneg": sig[sig["r24p"] < 0]}
    out["crude_books"] = pd.DataFrame({k: book(v) for k, v in subs.items()}).T
    sig["r24pneg"] = sig["r24p"] < 0
    out["sig_by_r24pneg_year"] = sig.groupby(["r24pneg", "year"]).apply(summ)["mean_x"].unstack(0)
    return out
