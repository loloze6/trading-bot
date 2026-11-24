import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 30
    drift = {}; usual = {}
    for c, ws in bars.items():
        rs = []
        for w, b in ws.items():
            cl = b["close"].values
            for i in range(0, len(cl) - H, H):
                rs.append(cl[i + H] / cl[i] - 1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs, ddof=1)
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            s90 = b["debug_info.components.fall90.last_history_value"].values if "debug_info.components.fall90.last_history_value" in b else np.full(len(b), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            ref = 0.0; used = set()
            for t in range(len(b)):
                if f[t] <= 0:
                    ref = 0.0; continue
                if f[t] - ref >= 2:
                    ref = f[t]
                    cell = t // H
                    if cell in used or t + H >= len(b):
                        continue
                    used.add(cell)
                    r = {"coin": c, "year": ts[t].year, "day": ts[t].normalize(), "fc": f[t], "s90": s90[t],
                         "r30": cl[t] / cl[t - 30] - 1 if t >= 30 else np.nan,
                         "r10": cl[t] / cl[t - 10] - 1 if t >= 10 else np.nan,
                         "r90": cl[t] / cl[t - 90] - 1 if t >= 90 else np.nan}
                    for h in (10, 20, 30):
                        r[f"x{h}"] = cl[t + h] / cl[t] - 1 - drift[c] * h / 30
                    r["z30"] = r["x30"] / usual[c]
                    rows.append(r)
    d = pd.DataFrame(rows)
    d["x30w"] = d["x30"].clip(d["x30"].quantile(0.05), d["x30"].quantile(0.95))
    def tday(g, col):
        dd = g.groupby("day")[col].sum(); n = len(dd)
        return dd.mean() / (dd.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
    def summ(g):
        return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": g["x30"].mean(),
                          "median": g["x30"].median(), "hit": (g["x30"] > 0).mean(),
                          "t_day": tday(g, "x30"), "wins_mean": g["x30w"].mean(), "t_wins": tday(g, "x30w"),
                          "x10": g["x10"].mean(), "x20": g["x20"].mean(), "z30": g["z30"].mean()})
    out = {}
    out["all_winsorised"] = summ(d)
    out["r30_known_share"] = d["r30"].notna().mean()
    e = d.dropna(subset=["r30"]).copy()
    e["r30_q"] = pd.qcut(e["r30"].rank(method="first"), 3, labels=["deep", "mid", "small"])
    out["by_r30"] = e.groupby("r30_q").apply(summ)
    sp = stats.spearmanr(e["r30"], e["x30"]); out["spearman_r30_x30_p"] = pd.Series({"rho": sp.correlation, "p": sp.pvalue, "n": len(e)})
    sp = stats.spearmanr(e["r30"], e["z30"]); out["spearman_r30_z30_p"] = pd.Series({"rho": sp.correlation, "p": sp.pvalue})
    e2 = d.dropna(subset=["r10"]).copy()
    sp = stats.spearmanr(e2["r10"], e2["x30"]); out["spearman_r10_x30_p"] = pd.Series({"rho": sp.correlation, "p": sp.pvalue, "n": len(e2)})
    e3 = d.dropna(subset=["r90", "r30"]).copy()
    if len(e3) > 10:
        e3["share30"] = e3["r30"] / e3["r90"]
        sp = stats.spearmanr(e3["share30"], e3["x30"]); out["spearman_share30_x30"] = pd.Series({"rho": sp.correlation, "p": sp.pvalue, "n": len(e3)})
    out["r30_by_year"] = e.groupby(["year", "r30_q"])["x30"].agg(["count", "mean"]).unstack()
    top = d.nlargest(5, "x30")[["coin", "year", "r30", "s90", "x30"]].reset_index(drop=True)
    top["year"] = top["year"].astype(int)
    out["top5"] = top
    out["s90_deepest_wins"] = summ(d[d["s90"] <= d["s90"].quantile(1/3)])
    return out
