import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = [24, 72, 168, 336, 720]
    rows = {h: [] for h in H}
    for coin, ws in bars.items():
        for h in H:
            allg = []
            tmp = []
            for w, df in ws.items():
                c = df["close"].values; n = len(c)
                idx = np.arange(0, n - h, h)
                if len(idx) == 0: continue
                fr = c[idx + h] / c[idx] - 1
                allg.append(fr)
                year = pd.to_datetime(df["timestamp"].values[idx]).year
                tmp.append(pd.DataFrame({"coin": coin, "w": w, "year": year, "fr": fr,
                                         "f": df["forecast"].values[idx],
                                         "reg": df["regime"].values[idx]}))
            if not tmp: continue
            m = np.concatenate(allg).mean()
            t = pd.concat(tmp); t["ex"] = t["fr"] - m
            rows[h].append(t)
    out = {}
    hz = []
    for h in H:
        d = pd.concat(rows[h]); d = d[d["reg"] == "trending"].dropna(subset=["f", "ex"])
        r = stats.linregress(d["f"], d["ex"])
        pos = d[d["f"] > 0]["ex"]; zero = d[d["f"] <= 0]["ex"]
        hz.append({"h": h, "n": len(d), "slope": r.slope, "t": r.slope / r.stderr,
                   "ex_pos_mean": pos.mean(), "ex_zero_mean": zero.mean(),
                   "t_pos_minus_zero": stats.ttest_ind(pos, zero, equal_var=False).statistic})
        if h == 336:
            pc = []
            for k, g in d.groupby("coin"):
                rr = stats.linregress(g["f"], g["ex"]) if g["f"].std() > 0 else None
                pc.append({"coin": k, "n": len(g), "slope": rr.slope if rr else np.nan,
                           "t": rr.slope / rr.stderr if rr else np.nan})
            out["336 by coin"] = pd.DataFrame(pc)
            py = []
            for k, g in d.groupby("year"):
                if len(g) > 5 and g["f"].std() > 0:
                    rr = stats.linregress(g["f"], g["ex"])
                    py.append({"year": k, "n": len(g), "slope": rr.slope, "t": rr.slope / rr.stderr})
            out["336 by year"] = pd.DataFrame(py)
            d["q"] = pd.cut(d["f"], [-0.01, 0.0, 5, 10, 20.1])
            out["336 by forecast bin"] = d.groupby("q")["ex"].agg(["count", "mean", "median"])
    out["slope by horizon"] = pd.DataFrame(hz)
    # book: gross vs fees, timing
    gross = []; fee = []; tim = []; mkt = []
    for coin, ws in bars.items():
        dd = pd.concat([days[coin][w] for w in ws])
        mcr = dd["coin_return"].mean()
        for w, df in ws.items():
            c = df["close"].values
            a = df["postRebalance_current_allocation"].fillna(0).values
            g = np.nansum(a[:-1] * (c[1:] / c[:-1] - 1))
            fr = ((df["total_portfolio_value"] - df["postRebalance_total_value"]) / df["total_portfolio_value"]).fillna(0).sum()
            gross.append(g); fee.append(fr)
    out["sum hourly gross gain per coin-window mean"] = float(np.mean(gross))
    out["sum fee share per coin-window mean"] = float(np.mean(fee))
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values()])
    out["trades"] = pd.DataFrame({"n": [len(tr)], "mean_pl": [tr["profit_loss_percent"].mean()],
                                  "mean_net": [tr["net_profit_loss_percent"].mean()],
                                  "med_dur_h": [tr["duration_minutes"].median() / 60]})
    return out
