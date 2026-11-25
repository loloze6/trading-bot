import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            f = df["forecast"].fillna(0).values
            c = df["close"].values
            raw = df.get("debug_info.components.break_up.last_history_value")
            raw = raw.values if raw is not None else np.full(len(f), np.nan)
            post = df.get("debug_info.components.break_up.post_pipeline_value")
            post = post.values if post is not None else np.full(len(f), np.nan)
            low = 0.0
            cand = np.zeros(len(f), bool)
            for i in range(len(f)):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cand[i] = True; low = f[i]
                else:
                    low = min(low, f[i])
            cell = np.arange(len(f)) // 5
            seen = set()
            for i in np.where(cand)[0]:
                if cell[i] in seen: continue
                seen.add(cell[i])
                # length of the run of positive forecast before this bar
                k = i
                while k - 1 >= 0 and f[k - 1] > 0: k -= 1
                r = {"coin": coin, "win": w, "day": str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                     "fc": f[i], "raw": raw[i], "post": post[i], "run": i - k,
                     "alloc": df["postRebalance_current_allocation"].iloc[i]}
                for h in H:
                    r[f"u{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < len(c) else np.nan
                rows.append(r)
    cs = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g.dropna(subset=[col]); n = len(x)
        if n < 2: return pd.Series({"n": n})
        m = x[col].mean()
        dev = x.groupby("day")[col].apply(lambda s: (s - m).sum()); D = len(dev)
        se = np.sqrt(D / (D - 1) * (dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": D, "mean": m, "t": m / se, "hit": (x[col] > 0).mean()})
    def slope(x, y):
        d = cs[[x, y]].dropna()
        if len(d) < 5: return pd.Series({"n": len(d)})
        r = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope / r.stderr, "rho_spearman": stats.spearmanr(d[x], d[y])[0]})
    out = {}
    out["fc_distribution"] = pd.Series({"share_fc_eq_20": (cs["fc"] >= 19.99).mean(),
                                         "fc_median": cs["fc"].median(), "raw_missing": cs["raw"].isna().mean(),
                                         "raw_median": cs["raw"].median(), "run_mean": cs["run"].mean()})
    out["slopes"] = pd.DataFrame({f"{x}->{y}": slope(x, y) for x in ["fc", "raw", "alloc"] for y in ["u3", "u5", "u10"]}).T
    cs["raw_q"] = pd.qcut(cs["raw"].rank(method="first"), 4, labels=["r1", "r2", "r3", "r4"])
    out["by_raw_quartile_u5"] = cs.groupby("raw_q").apply(summ)
    out["raw_q_means"] = cs.groupby("raw_q")[["raw", "fc"]].mean()
    cs["capped"] = cs["fc"] >= 19.99
    out["by_capped_u5"] = cs.groupby("capped").apply(summ)
    out["by_run_u5"] = cs.groupby(np.minimum(cs["run"], 3)).apply(summ)
    cs["lograw"] = np.log1p(cs["raw"].clip(lower=0))
    out["slope_lograw"] = pd.DataFrame({y: slope("lograw", y) for y in ["u3", "u5", "u10"]}).T
    out["no_btc_u5"] = summ(cs[cs.coin != "BTCUSD"])
    return out
