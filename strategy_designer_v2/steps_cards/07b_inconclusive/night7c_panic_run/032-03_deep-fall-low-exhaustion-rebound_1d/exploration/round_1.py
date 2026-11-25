import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # normal drift and usual move per horizon over all windows of the coin
        d = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            d[h] = (np.mean(rs), np.std(rs, ddof=1))
        drift[coin] = d
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            ret30 = pd.Series(c).pct_change(30).values
            rng = ((df["high"] - df["low"]) / df["close"]).values
            rng30 = pd.Series(rng).rolling(30).mean().values
            rng90 = pd.Series(rng).rolling(90, min_periods=60).mean().values
            low30 = pd.Series(c).shift(1).rolling(30).min().values
            # new-low bars regardless of regime
            used = set()
            prevlow = 0.0
            for i in range(n):
                fi = f[i]
                if fi == 0:
                    prevlow = 0.0
                cell = i // 5
                is_case = (fi - prevlow >= 2) and fi > 0 and cell not in used and i + 5 < n
                if is_case:
                    used.add(cell)
                    prevlow = fi
                else:
                    prevlow = min(prevlow, fi) if fi > 0 else 0.0
                newlow = (not np.isnan(low30[i])) and c[i] < low30[i]
                if not (is_case or newlow):
                    continue
                r = {"coin": coin, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                     "case": is_case, "newlow": newlow, "inreg": df["regime"].iloc[i] == "mean_reversion",
                     "fc": fi, "ret30": ret30[i], "rr": rng30[i] / rng90[i] if rng90[i] == rng90[i] else np.nan}
                for h in H:
                    if i + h < n:
                        r[f"u{h}"] = c[i + h] / c[i] - 1 - drift[coin][h][0]
                        r[f"t{h}"] = c[i + h] / c[i] - 1
                rows.append(r)
    R = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        if len(x) < 2: return pd.Series({"n": len(x), "mean": x.mean(), "t": np.nan})
        dd = g.dropna(subset=[col]).groupby("day")[col].sum()
        G = len(dd)
        t = x.mean() / (np.sqrt((dd - dd.mean() * 0).pow(2).sum()) / len(x)) if False else x.mean() / (dd.std(ddof=1) * np.sqrt(G) / len(x))
        return pd.Series({"n": len(x), "days": G, "mean": x.mean(), "t": t})
    C = R[R.case]
    out = {}
    out["cases_by_h"] = pd.DataFrame({h: summ(C, f"u{h}") for h in H}).T
    out["cases_total_by_h"] = pd.DataFrame({h: summ(C, f"t{h}") for h in H}).T
    out["cases_by_coin"] = C.groupby("coin").apply(summ)
    out["cases_by_win"] = C.groupby("win").apply(summ)
    out["cases_by_year"] = C.groupby("year").apply(summ)
    C = C.copy()
    C["fq"] = pd.qcut(C["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    C["dq"] = pd.qcut(C["ret30"].rank(method="first"), 3, labels=["deep", "mid", "shallow"])
    out["cases_by_fc"] = C.groupby("fq").apply(summ)
    out["cases_by_fall30"] = C.groupby("dq").apply(summ)
    out["cases_by_fall30_u10"] = C.groupby("dq").apply(lambda g: summ(g, "u10"))
    out["spearman_ret30_u5"] = float(stats.spearmanr(C["ret30"], C["u5"], nan_policy="omit")[0])
    NL = R[R.newlow]
    out["newlow_inreg_vs_not_u5"] = NL.groupby("inreg").apply(summ)
    out["newlow_inreg_vs_not_u10"] = NL.groupby("inreg").apply(lambda g: summ(g, "u10"))
    return out
