import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1,2,3,5,7,10]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in bars.items():
        r3 = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c)-3, 3)
            r3 += list(c[idx+3]/c[idx]-1)
        drift[coin] = np.mean(r3); usual[coin] = np.std(r3)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df.get("debug_info.components.scaled_week_rise.last_history_value")
            raw = raw.values if raw is not None else np.full(len(df), np.nan)
            n = len(df)
            lowest = 0.0; taken = set()
            for t in range(n):
                cell = t // 3
                if f[t] - lowest >= 2 and f[t] > 0 and cell not in taken:
                    taken.add(cell)
                    rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                           "f": f[t], "raw": raw[t]}
                    for h in H:
                        rec[f"r{h}"] = c[t+h]/c[t]-1 if t+h < n else np.nan
                    rec["u3"] = rec["r3"] - drift[coin] if not np.isnan(rec["r3"]) else np.nan
                    rec["day"] = str(df["timestamp"].iloc[t])[:10]
                    rec["past7"] = c[t]/c[t-7]-1 if t >= 7 else np.nan
                    rows.append(rec)
                    lowest = f[t]
                lowest = min(lowest, f[t])
                if f[t] <= 0: lowest = 0.0
    cs = pd.DataFrame(rows)
    out = {}
    def summ(g):
        u = g["u3"].dropna()
        return pd.Series({"n": len(u), "mean_u3": u.mean(), "t": u.mean()/(u.std()/np.sqrt(len(u))) if len(u)>2 else np.nan})
    out["all"] = summ(cs)
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["by_window"] = cs.groupby("win").apply(summ)
    cs["fq"] = pd.qcut(cs["f"], 4, labels=False, duplicates="drop")
    out["by_forecast_q"] = cs.groupby("fq").apply(summ)
    cs["rq"] = pd.qcut(cs["raw"], 4, labels=False, duplicates="drop")
    out["by_raw_q"] = cs.groupby("rq").apply(summ)
    hz = {}
    for h in H:
        rr = []
        for coin, ws in bars.items():
            pass
        x = cs[f"r{h}"].dropna()
        hz[h] = {"n": len(x), "mean_total": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x)))}
    out["by_horizon_total"] = pd.DataFrame(hz).T
    out["drift_usual"] = pd.DataFrame({"drift3": drift, "usual3": usual})
    out["corr_raw_u3"] = float(cs[["raw","u3"]].corr().iloc[0,1])
    out["corr_f_u3"] = float(cs[["f","u3"]].corr().iloc[0,1])
    # in-profile baseline: all grid bars where regime == unknown
    base = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values; reg = df["regime"].values
            for t in range(0, len(c)-3, 3):
                if reg[t] == "unknown":
                    base.append({"coin": coin, "u3": c[t+3]/c[t]-1-drift[coin], "pos": df["forecast"].iloc[t] > 0})
    b = pd.DataFrame(base)
    out["inprofile_grid"] = b.groupby(["coin","pos"]).apply(summ)
    return out
