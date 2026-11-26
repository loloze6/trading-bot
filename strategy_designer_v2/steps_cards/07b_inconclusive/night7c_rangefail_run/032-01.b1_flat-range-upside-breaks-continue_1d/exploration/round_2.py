def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    for H in [3, 5, 10, 20]:
        drift = {}
        for coin, wins in bars.items():
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - H, H):
                    rets.append(c[i + H] / c[i] - 1)
            drift[coin] = np.mean(rets)
        rows = []
        for coin, wins in bars.items():
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                f = df["forecast"].fillna(0).values
                ts = pd.to_datetime(df["timestamp"])
                rise = f - np.r_[0, f[:-1]]
                hi = df["high"].shift(1).rolling(60, min_periods=20).max().values
                lo = df["low"].shift(1).rolling(60, min_periods=20).min().values
                seen = set()
                for i in np.where(rise >= 2)[0]:
                    cell = i // H
                    if cell in seen or i + H >= len(c):
                        continue
                    seen.add(cell)
                    rows.append({"coin": coin, "day": ts[i].normalize(), "year": ts[i].year,
                                 "fc": f[i], "rng": hi[i] / lo[i] - 1,
                                 "brk": c[i] / hi[i] - 1,
                                 "r": c[i + H] / c[i] - 1 - drift[coin]})
        d = pd.DataFrame(rows)
        def tday(s):
            s = s.dropna()
            dd = d.loc[s.index]
            n = len(s); m = s.mean()
            g = (s - m).groupby(dd["day"]).sum()
            return m, m / (np.sqrt((g ** 2).sum()) / n), n, g.size
        m, t, n, nd = tday(d["r"])
        medf = d["fc"].median()
        hiF = d.loc[d.fc > medf, "r"].mean() - d.loc[d.fc < medf, "r"].mean()
        medr = d["rng"].median()
        nar = d[d.rng <= medr]; wid = d[d.rng > medr]
        mn, tn, nn, _ = tday(nar["r"]); mw, tw, nw, _ = tday(wid["r"])
        out[f"H{H}"] = pd.Series({"mean": m, "t": t, "cases": n, "days": nd,
                                  "fc_hi_minus_lo": hiF,
                                  "narrow_mean": mn, "narrow_t": tn, "narrow_n": nn,
                                  "wide_mean": mw, "wide_t": tw, "wide_n": nw,
                                  "corr_rng_r": d[["rng", "r"]].corr().iloc[0, 1],
                                  "corr_fc_r": d[["fc", "r"]].corr().iloc[0, 1],
                                  "share_pos": (d.r > 0).mean()})
        if H == 5:
            out["H5_by_year"] = d.groupby("year")["r"].agg(["mean", "count"])
            out["H5_by_coin"] = d.groupby("coin")["r"].agg(["mean", "count"])
            d["rq"] = pd.qcut(d["rng"].rank(method="first"), 4, labels=["r1narrow", "r2", "r3", "r4wide"])
            out["H5_by_range_q"] = d.groupby("rq")["r"].agg(["mean", "count", "median"])
    return {"summary": pd.DataFrame({k: v for k, v in out.items() if k.startswith("H") and isinstance(v, pd.Series)}),
            "H5_by_year": out["H5_by_year"], "H5_by_coin": out["H5_by_coin"], "H5_by_range_q": out["H5_by_range_q"]}
