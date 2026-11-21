import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [6, 12, 18, 36]
    rows = []
    for coin, wins in bars.items():
        # normal drift and usual move per horizon on grid of all windows
        drift, sd = {}, {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            rs = np.array(rs); drift[h] = rs.mean(); sd[h] = rs.std()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            f = df["forecast"].fillna(0).values; reg = df["regime"].values
            q = df.get("debug_info.components.quiet.post_pipeline_value")
            q = q.values if q is not None else np.full(len(c), np.nan)
            prior_hi = pd.Series(hi).shift(1).rolling(12).max().values
            rng = (hi - lo) / c
            r7 = pd.Series(rng).rolling(42).mean().values
            r60 = pd.Series(rng).rolling(360).mean().values
            past60 = pd.Series(c).pct_change(360).values
            past10 = pd.Series(c).pct_change(60).values
            low = None; seen = set()
            for t in range(len(c)):
                if f[t] <= 0:
                    low = 0.0; continue
                if low is None: low = 0.0
                if reg[t] == "trending" and f[t] - low >= 2:
                    low = f[t]
                    cell = t // 18
                    if cell in seen or t + 18 >= len(c): continue
                    seen.add(cell)
                    rec = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[t]).year,
                               q=q[t], ratio=r60[t] / r7[t] if r7[t] else np.nan,
                               brk=c[t] / prior_hi[t] - 1, p60=past60[t], p10=past10[t])
                    for h in H:
                        if t + h < len(c):
                            rec[f"u{h}"] = c[t + h] / c[t] - 1 - drift[h]
                            rec[f"s{h}"] = rec[f"u{h}"] / sd[h]
                    rows.append(rec)
                else:
                    low = min(low, f[t])
    d = pd.DataFrame(rows)
    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["strength_by_horizon"] = pd.DataFrame({h: summ(d, f"s{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("w").apply(summ)
    d["qq"] = pd.qcut(d["q"], 5, labels=False, duplicates="drop")
    out["by_quiet_quintile"] = d.groupby("qq").apply(summ)
    d["rq"] = pd.qcut(d["ratio"], 5, labels=False, duplicates="drop")
    out["by_ratio_quintile"] = d.groupby("rq").apply(summ)
    d["bq"] = pd.qcut(d["brk"], 5, labels=False, duplicates="drop")
    out["by_breakout_size_quintile"] = d.groupby("bq").apply(summ)
    out["by_p60_sign"] = d.groupby(np.sign(d["p60"])).apply(summ)
    out["by_p10_sign"] = d.groupby(np.sign(d["p10"])).apply(summ)
    out["by_p60_sign_u36"] = d.groupby(np.sign(d["p60"])).apply(lambda g: summ(g, "u36"))
    out["sd_unusual_u18"] = d["u18"].std()
    return out
