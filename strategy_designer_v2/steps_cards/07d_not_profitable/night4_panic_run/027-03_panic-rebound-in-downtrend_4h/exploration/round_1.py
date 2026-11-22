import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    trades = []
    days_in = []
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            rng = (b["high"] - b["low"]) / c
            rr = rng.rolling(6).mean() / rng.rolling(180).mean()  # short/long, >=3 is panic
            prior = c.shift(6) / c.shift(186) - 1
            r6 = c / c.shift(6) - 1
            fallz = r6 / r6.abs().rolling(180).mean()
            fwd = c.shift(-84) / c - 1
            idx = np.arange(0, len(b), 84)
            g = pd.DataFrame({"rr": rr.iloc[idx].values, "prior": prior.iloc[idx].values,
                              "fallz": fallz.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                              "alloc": b["postRebalance_current_allocation"].iloc[idx].values,
                              "fc": b["forecast"].iloc[idx].values})
            g["coin"] = coin; g["win"] = w
            grid.append(g)
            t = data["trades"][coin][w]
            if len(t):
                tt = t.copy(); tt["coin"] = coin; trades.append(tt)
            d = data["days"][coin][w]
            bb = b.copy(); bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            inpos = bb.groupby("day")["postRebalance_current_allocation"].apply(lambda s: (s.abs() > 0).any())
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd["inpos"] = dd["day"].map(inpos).fillna(False)
            days_in.append(dd)
        G = pd.concat(grid)
        G = G.dropna(subset=["fwd"])
        drift = G["fwd"].mean()
        G["unus"] = G["fwd"] - drift
        rows.append(G)
    G = pd.concat(rows)
    G = G.dropna(subset=["rr", "fallz", "prior"])
    def summ(df, key):
        out = df.groupby(key, observed=True)["unus"].agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["total_mean"] = df.groupby(key, observed=True)["fwd"].mean()
        return out.round(4)
    G["rr_b"] = pd.cut(G["rr"], [0, 1, 1.5, 2, 3, 100])
    G["fall_b"] = pd.cut(G["fallz"], [-100, -3, -2, -1, 0, 1, 2, 100])
    G["prior_neg"] = G["prior"] < 0
    falls = G[G["fallz"] < 0]
    res = {}
    res["by range ratio (all)"] = summ(G, "rr_b")
    res["by fall z (all)"] = summ(G, "fall_b")
    res["falls, by range ratio x prior_neg"] = summ(falls, ["rr_b", "prior_neg"])
    res["rr>=1.5 falls, by fall z"] = summ(G[(G["rr"] >= 1.5)], "fall_b")
    T = pd.concat(trades)
    res["trades"] = pd.DataFrame({"n": [len(T)], "mean_net": [T["net_profit_loss_percent"].mean()],
                                  "median_net": [T["net_profit_loss_percent"].median()],
                                  "win_share": [(T["net_profit_loss_percent"] > 0).mean()],
                                  "mean_dur_days": [T["duration_minutes"].mean() / 1440]})
    res["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"])
    D = pd.concat(days_in)
    res["days in position share"] = float(D["inpos"].mean())
    res["book ret in/out pos"] = D.groupby("inpos")[["book_return", "coin_return"]].mean()
    return res
