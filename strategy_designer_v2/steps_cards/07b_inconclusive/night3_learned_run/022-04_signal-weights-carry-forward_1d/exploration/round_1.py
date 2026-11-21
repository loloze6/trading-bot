def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 5
    comps = ["mom", "rev", "high", "vol"]
    rows = []
    for coin, wins in data["bars"].items():
        cells = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            for i in range(0, n - H, H):
                r = c[i + H] / c[i] - 1
                d = {"coin": coin, "window": w, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "ret": r, "f": b["forecast"].iloc[i]}
                for k in comps:
                    col = "debug_info.components.%s.post_pipeline_value" % k
                    d[k] = b[col].iloc[i] if col in b else np.nan
                    rc = "debug_info.components.%s.last_history_value" % k
                    d[k + "_raw"] = b[rc].iloc[i] if rc in b else np.nan
                cells.append(d)
        df = pd.DataFrame(cells)
        df["ex"] = df["ret"] - df["ret"].mean()
        df["usual"] = df["ret"].std()
        rows.append(df)
    df = pd.concat(rows, ignore_index=True)
    df = df[df["f"].notna()]
    nz = df[df["f"] != 0].copy()
    nz["m"] = nz["f"] / 10 * nz["ex"]

    def tstat(x):
        x = pd.Series(x).dropna()
        return pd.Series({"mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "n": len(x)})

    out = {}
    out["main_check"] = tstat(nz["m"])
    out["by_coin"] = nz.groupby("coin")["m"].apply(tstat).unstack()
    out["by_year"] = nz.groupby("year")["m"].apply(tstat).unstack()
    out["by_window"] = nz.groupby("window")["m"].apply(tstat).unstack()
    # per component: component value x excess return
    comp_res = {}
    for k in comps:
        x = nz[k] * nz["ex"]
        comp_res[k] = tstat(x)
        comp_res[k + "_corr"] = pd.Series({"mean": nz[[k, "ex"]].corr().iloc[0, 1], "t": np.nan, "n": nz[k].notna().sum()})
    out["components"] = pd.DataFrame(comp_res).T
    # sign of raw w_k*z (sign of weight unknown); by abs forecast quintile
    nz["q"] = pd.qcut(nz["f"].abs(), 5, labels=False, duplicates="drop")
    out["by_absf_quintile"] = nz.groupby("q")["m"].apply(tstat).unstack()
    nz["side"] = np.where(nz["f"] > 0, "long", "short")
    g = nz.groupby("side")
    out["by_side"] = pd.DataFrame({"m": g["m"].apply(lambda s: s.mean()), "t": g["m"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s)))),
                                   "ex_dir": g.apply(lambda s: (np.sign(s["f"]) * s["ex"]).mean()), "n": g.size()})
    # component per year correlation
    cy = {}
    for k in comps:
        cy[k] = nz.groupby("year").apply(lambda s: s[[k, "ex"]].corr().iloc[0, 1])
    out["comp_corr_by_year"] = pd.DataFrame(cy)
    # market regime: 28d trailing? use sign of ex vs by up/down of the coin's own past 30 days not available easily; use component raw sign
    return out
