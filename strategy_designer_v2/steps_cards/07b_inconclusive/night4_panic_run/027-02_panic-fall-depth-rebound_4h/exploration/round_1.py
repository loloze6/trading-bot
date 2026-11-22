def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H_list = [6, 18, 42, 84, 126]
    # drift / usual move per coin per horizon on non-overlapping grid
    drift = {}
    rows = []
    allpanic = []
    for coin, wins in bars.items():
        rets = {h: [] for h in H_list}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in H_list:
                idx = np.arange(0, n - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: (np.mean(rets[h]), np.std(rets[h], ddof=1)) for h in H_list}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            fc = df["forecast"].fillna(0).values
            prev = np.r_[0, fc[:-1]]
            reg = df["regime"].astype(str).values
            ch6 = pd.Series(c).pct_change(6).values * 100
            ch42 = pd.Series(c).pct_change(42).values * 100
            ch180 = pd.Series(c).pct_change(180).values * 100
            rng = (df["high"] - df["low"]) / df["close"]
            ratio = (rng.rolling(6).mean() / rng.rolling(180).mean()).values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            sig = (reg == "mean_reversion") & ((fc - prev) >= 2)
            seen = set()
            for t in np.where(sig)[0]:
                cell = t // 84
                if cell in seen:
                    continue
                seen.add(cell)
                r = {"coin": coin, "win": w, "year": year[t], "fall": -ch6[t], "fc": fc[t],
                     "pre42": ch42[t], "pre180": ch180[t], "ratio": ratio[t]}
                for h in H_list:
                    if t + h < n:
                        d, s = drift[coin][h]
                        r[f"tot{h}"] = c[t + h] / c[t] - 1
                        r[f"ex{h}"] = (c[t + h] / c[t] - 1 - d) / s
                    else:
                        r[f"tot{h}"] = np.nan; r[f"ex{h}"] = np.nan
                rows.append(r)
            # all panic-regime bars, rising or falling, first per 84 cell
            pm = reg == "mean_reversion"
            seen = set()
            for t in np.where(pm)[0]:
                cell = t // 84
                if cell in seen or t + 84 >= n:
                    continue
                seen.add(cell)
                d, s = drift[coin][84]
                allpanic.append({"coin": coin, "ch6": ch6[t], "ex84": (c[t+84]/c[t]-1-d)/s})
    cs = pd.DataFrame(rows)
    ap = pd.DataFrame(allpanic)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["cases_by_horizon"] = pd.DataFrame({h: tt(cs[f"ex{h}"]) for h in H_list}).T
    sl = {}
    for h in H_list:
        d = cs[["fall", f"ex{h}"]].dropna()
        r = stats.linregress(d["fall"], d[f"ex{h}"])
        sl[h] = {"n": len(d), "slope": r.slope, "t": r.slope / r.stderr, "rank_corr": stats.spearmanr(d["fall"], d[f"ex{h}"])[0]}
    out["slope_by_horizon"] = pd.DataFrame(sl).T
    out["by_coin_ex84"] = cs.groupby("coin")["ex84"].apply(tt).unstack()
    out["by_year_ex84"] = cs.groupby("year")["ex84"].apply(tt).unstack()
    d = cs.dropna(subset=["ex84"]).copy()
    d["fallq"] = pd.qcut(d["fall"], 4, labels=False)
    out["by_fall_quartile"] = d.groupby("fallq").agg(n=("ex84", "size"), fall=("fall", "mean"), ex84=("ex84", "mean"), ex42=("ex42", "mean"), tot84=("tot84", "mean"))
    d["preq"] = pd.qcut(d["pre180"], 3, labels=False)
    out["by_prior_30d_return_tercile"] = d.groupby("preq").agg(n=("ex84", "size"), pre=("pre180", "mean"), ex84=("ex84", "mean"), ex42=("ex42", "mean"))
    d["ratq"] = pd.qcut(d["ratio"], 3, labels=False, duplicates="drop")
    out["by_range_ratio_tercile"] = d.groupby("ratq").agg(n=("ex84", "size"), ratio=("ratio", "mean"), ex84=("ex84", "mean"))
    ap["side"] = np.where(ap["ch6"] < 0, "fell", "rose")
    out["all_panic_by_side"] = ap.groupby("side")["ex84"].apply(tt).unstack()
    r = stats.linregress(ap["ch6"].fillna(0), ap["ex84"])
    out["all_panic_slope_ex84_on_ch6"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(ap)}"
    out["median_ex84"] = float(cs["ex84"].median())
    out["share_pos_ex84"] = float((cs["ex84"] > 0).mean())
    return out
