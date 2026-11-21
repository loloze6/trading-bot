import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1,3,5,10,20]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            fc = df["forecast"].values
            alloc = df["postRebalance_current_allocation"].fillna(0).values
            prev = df["previous_allocation"].fillna(0).values
            r90 = pd.Series(c).pct_change(90).values
            ts = df.get("debug_info.components.touch_s.last_history_value")
            fl = df.get("debug_info.components.fall90.last_history_value")
            for i in range(0, n, 5):
                rec = {"coin": coin, "win": w, "i": i, "fc": fc[i],
                       "start": (prev[i] >= 0) and (alloc[i] < 0),
                       "r90": r90[i],
                       "touch": ts.values[i] if ts is not None else np.nan,
                       "fall": fl.values[i] if fl is not None else np.nan,
                       "year": pd.Timestamp(df["timestamp"].iloc[i]).year}
                for h in H:
                    rec[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    # drift per coin per h on same grid (h=5 grid; approximate for others)
    for h in H:
        g[f"d{h}"] = g.groupby("coin")[f"r{h}"].transform("mean")
        g[f"x{h}"] = -(g[f"r{h}"] - g[f"d{h}"])
    act = g[g.fc < 0].copy()
    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out = {}
    out["by_h_active"] = pd.DataFrame({h: tt(act[f"x{h}"]) for h in H}).T
    out["by_h_start"] = pd.DataFrame({h: tt(act[act.start][f"x{h}"]) for h in H}).T
    out["by_coin"] = act.groupby("coin")["x5"].apply(tt).unstack()
    out["by_year"] = act.groupby("year")["x5"].apply(tt).unstack()
    act["fq"] = pd.qcut(-act.fc, 4, labels=False, duplicates="drop")
    out["by_fc_q"] = act.groupby("fq")["x5"].apply(tt).unstack()
    act["rq"] = pd.qcut(act.r90, 4, labels=False, duplicates="drop")
    out["by_r90_q"] = act.groupby("rq")["x5"].apply(tt).unstack()
    out["r90_q_vals"] = act.groupby("rq")["r90"].median()
    act["tq"] = pd.qcut(act.touch.rank(method="first"), 4, labels=False)
    out["by_touch_q"] = act.groupby("tq")["x5"].apply(tt).unstack()
    out["by_r90_q_h20"] = act.groupby("rq")["x20"].apply(tt).unstack()
    # inactive grid bars comparison
    ina = g[g.fc == 0]
    out["inactive_h"] = pd.DataFrame({h: tt(ina[f"x{h}"]) for h in H}).T
    # inactive with r90<0
    ina2 = ina[ina.r90 < 0]
    out["inactive_r90neg_h"] = pd.DataFrame({h: tt(ina2[f"x{h}"]) for h in H}).T
    return out
