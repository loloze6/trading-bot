import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = {h: [] for h in (1,3,5,7,10)}
        for w, b in wins.items():
            c = b["close"].values
            for h in rets:
                idx = np.arange(0, len(c)-h, h)
                rets[h] += list(c[idx+h]/c[idx]-1)
        drift[coin] = {h: np.mean(v) for h, v in rets.items()}
        drift[coin]["sd3"] = np.std(rets[3], ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; f = b["forecast"].fillna(0).values
            raw = b.get("debug_info.components.scaled_week_rise.last_history_value")
            raw = raw.values if raw is not None else np.full(len(b), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            low = 0.0
            taken = set()
            for t in range(len(b)):
                if f[t] <= 0:
                    low = 0.0; continue
                if f[t] - low >= 2:
                    cell = t // 3
                    if cell not in taken:
                        taken.add(cell)
                        r = {"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(),
                             "fc": f[t], "raw": raw[t], "regime": b["regime"].iloc[t]}
                        for h in (1,3,5,7,10):
                            r[f"u{h}"] = (c[t+h]/c[t]-1 - drift[coin][h]) if t+h < len(c) else np.nan
                        r["prior7"] = c[t]/c[t-7]-1 if t >= 7 else np.nan
                        rows.append(r)
                    low = f[t]
                else:
                    low = min(low, f[t])
    df = pd.DataFrame(rows)
    def summ(g, col="u3"):
        x = g[col].dropna()
        d = g.loc[x.index].groupby("day")[col].sum()
        n = len(x); D = len(d)
        t = x.mean()/(np.sqrt(D/(D-1))*d.std(ddof=0)*np.sqrt(D)/n) if D > 2 else np.nan
        return pd.Series({"n": n, "days": D, "mean": x.mean(), "t": t})
    out = {}
    out["all_by_h"] = pd.DataFrame({h: summ(df, f"u{h}") for h in ("u1","u3","u5","u7","u10")}).T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    df["fq"] = pd.qcut(df["fc"], 4, labels=False, duplicates="drop")
    out["by_fc_q"] = df.groupby("fq").apply(summ)
    out["fc_q_ranges"] = df.groupby("fq")["fc"].agg(["min","max"])
    df["rq"] = pd.qcut(df["raw"], 4, labels=False, duplicates="drop")
    out["by_raw_q"] = df.groupby("rq").apply(summ)
    out["by_raw_q_u7"] = df.groupby("rq").apply(lambda g: summ(g, "u7"))
    out["by_fc_q_u7"] = df.groupby("fq").apply(lambda g: summ(g, "u7"))
    out["regimes"] = df["regime"].value_counts()
    out["corr_fc_u3_u7"] = pd.Series({"fc_u3": df[["fc","u3"]].corr().iloc[0,1], "raw_u3": df[["raw","u3"]].corr().iloc[0,1],
                                      "fc_u7": df[["fc","u7"]].corr().iloc[0,1], "raw_u7": df[["raw","u7"]].corr().iloc[0,1]})
    out["sd3"] = pd.Series({k: v["sd3"] for k, v in drift.items()})
    return out
