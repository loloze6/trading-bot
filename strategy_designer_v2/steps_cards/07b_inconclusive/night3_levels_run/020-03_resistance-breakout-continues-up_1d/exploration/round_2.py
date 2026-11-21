import pandas as pd, numpy as np

def explore(data):
    rows = []
    H = [3, 5, 10]
    for coin, wins in data["bars"].items():
        drift = {}
        for h in H:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            c = b["close"].values
            raw = b["debug_info.components.res_break.last_history_value"].values
            p20 = pd.Series(c).pct_change(20).values
            p10 = pd.Series(c).pct_change(10).values
            vol = pd.Series(c).pct_change().rolling(20).std().values
            lowest = 0.0; seen = set()
            for t in range(len(b)):
                if f[t] <= 0:
                    lowest = 0.0; continue
                lowest = min(lowest, f[t])
                if f[t] - lowest >= 2:
                    cell = t // 5
                    if cell in seen:
                        lowest = f[t]; continue
                    seen.add(cell)
                    r = {"coin": coin, "win": int(w[1:]), "raw": raw[t], "p20": p20[t], "p10": p10[t],
                         "p20v": p20[t] / (vol[t] * np.sqrt(20)) if vol[t] and vol[t] > 0 else np.nan,
                         "year": pd.Timestamp(b["timestamp"].iloc[t]).year}
                    for h in H:
                        r[f"x{h}"] = (c[t + h] / c[t] - 1 - drift[h]) if t + h < len(c) else np.nan
                    rows.append(r)
                    lowest = f[t]
    d = pd.DataFrame(rows)
    def summ(g, col="x5"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    d = d.dropna(subset=["p20"])
    d["p20h"] = (d["p20"] > d["p20"].median()).astype(int)
    out["p20half_by_coin"] = d.groupby(["coin", "p20h"]).apply(summ).unstack()
    out["p20half_by_year"] = d.groupby(["year", "p20h"]).apply(summ).unstack()
    d["q"] = pd.qcut(d["p20"].rank(method="first"), 4, labels=False)
    out["p20q_h3"] = d.groupby("q").apply(lambda g: summ(g, "x3"))
    out["p20q_h10"] = d.groupby("q").apply(lambda g: summ(g, "x10"))
    d["qv"] = pd.qcut(d["p20v"].rank(method="first"), 4, labels=False)
    out["p20v_q"] = d.groupby("qv").apply(summ)
    d["q10"] = pd.qcut(d["p10"].rank(method="first"), 4, labels=False)
    out["p10_q"] = d.groupby("q10").apply(summ)
    top = d[d["p20h"] == 1].copy()
    top["rh"] = (top["raw"] > top["raw"].median()).astype(int)
    out["top_p20_raw_half"] = top.groupby("rh").apply(summ)
    out["corr_p20_x5"] = float(d[["p20", "x5"]].dropna().corr(method="spearman").iloc[0, 1])
    out["windows_top_half_pos_share"] = float((d[d.p20h == 1].groupby("win")["x5"].mean() > 0).mean())
    out["windows_bot_half_pos_share"] = float((d[d.p20h == 0].groupby("win")["x5"].mean() > 0).mean())
    return out
