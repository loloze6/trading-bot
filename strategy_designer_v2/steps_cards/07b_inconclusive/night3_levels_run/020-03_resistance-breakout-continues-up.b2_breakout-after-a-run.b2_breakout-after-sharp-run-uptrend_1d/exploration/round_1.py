import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon on grid
        drift = {}
        for h in (1, 3, 5, 10, 20):
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            bs = df.get("debug_info.components.break_strength.post_pipeline_value")
            ru = df.get("debug_info.components.run_up.post_pipeline_value")
            r60 = pd.Series(c).pct_change(60).values
            r10 = pd.Series(c).pct_change(10).values
            lowest = 0.0
            last_cell = -1
            for t in range(len(df)):
                if f[t] <= 0:
                    lowest = 0.0
                    continue
                if f[t] - lowest >= 2:
                    cell = t // 5
                    if cell != last_cell:
                        last_cell = cell
                        rec = dict(coin=coin, window=w, year=ts[t].year, fc=f[t],
                                   bs=np.nan if bs is None else bs.iloc[t],
                                   ru=np.nan if ru is None else ru.iloc[t],
                                   r60=r60[t], r10=r10[t])
                        for h in (1, 3, 5, 10, 20):
                            rec[f"u{h}"] = (c[t + h] / c[t] - 1 - drift[h]) if t + h < len(c) else np.nan
                        rows.append(rec)
                        lowest = f[t]
                lowest = min(lowest, f[t])
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["u5"].dropna()
        return pd.Series({"n": len(x), "mean_u5": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["all"] = summ(d)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_window"] = d.groupby("window").apply(summ)
    hz = {}
    for h in (1, 3, 5, 10, 20):
        x = d[f"u{h}"].dropna()
        hz[h] = {"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))), "per_day": x.mean() / h}
    out["by_horizon"] = pd.DataFrame(hz).T
    d["fc_q"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_fc_q"] = d.groupby("fc_q").apply(summ)
    d["bs_pos"] = d["bs"] > 0
    d["ru_pos"] = d["ru"] > 0
    out["by_parts"] = d.groupby(["bs_pos", "ru_pos"]).apply(summ)
    d["r60_q"] = pd.qcut(d["r60"].rank(method="first"), 4, labels=False)
    out["by_r60_q"] = d.groupby("r60_q").apply(summ)
    d["r10_q"] = pd.qcut(d["r10"].rank(method="first"), 4, labels=False)
    out["by_r10_q"] = d.groupby("r10_q").apply(summ)
    out["by_r10_q_h10"] = d.groupby("r10_q")["u10"].agg(["count", "mean"])
    out["by_r10_q_h20"] = d.groupby("r10_q")["u20"].agg(["count", "mean"])
    return out
