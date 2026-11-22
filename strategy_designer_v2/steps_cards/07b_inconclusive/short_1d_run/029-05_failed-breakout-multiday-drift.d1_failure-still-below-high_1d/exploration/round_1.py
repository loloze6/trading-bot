import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H_list = [2, 4, 8, 16]
    # drift and usual move per coin per horizon
    drift = {}; usual = {}
    for c in bars:
        for h in H_list:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(cl)
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            r20 = pd.Series(cl).pct_change(20).values
            for start in range(0, n, 8):
                end = min(start + 8, n)
                sel = [i for i in range(start, end) if f[i] <= -2]
                if not sel: continue
                i = sel[0]
                rec = {"coin": c, "win": w, "year": year[i], "absf": -f[i], "r20": r20[i]}
                for h in H_list:
                    if i + h < n:
                        tot = -(cl[i + h] / cl[i] - 1)
                        rec[f"u{h}"] = tot + drift[(c, h)]
                        rec[f"t{h}"] = tot
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u8"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["overall_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H_list}).T
    out["total_by_horizon"] = pd.DataFrame({h: summ(d, f"t{h}") for h in H_list}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["absf"], 3, labels=["low", "mid", "high"])
    out["by_forecast_tercile"] = d.groupby("fq").apply(summ)
    d["trend"] = np.where(d["r20"] > 0, "r20_up", "r20_down")
    out["by_prior20d"] = d.groupby("trend").apply(summ)
    out["by_coin_h16"] = d.groupby("coin").apply(lambda g: summ(g, "u16"))
    out["usual8"] = pd.Series({c: usual[(c, 8)] for c in bars})
    return out
