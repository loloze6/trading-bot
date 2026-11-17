def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    A = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.reset_index(drop=True).copy()
            d["r1"] = d["close"].shift(-1)/d["close"] - 1
            d["pos"] = d["postRebalance_current_allocation"]
            d["ma100"] = d["close"].rolling(100, min_periods=60).mean()
            d["up"] = d["close"] > d["ma100"]
            d["gain"] = d["pos"]*d["r1"]
            d["gain_long"] = d["pos"].clip(lower=0)*d["r1"]
            d["gain_short"] = d["pos"].clip(upper=0)*d["r1"]
            d["gain_longup"] = np.where(d["up"], d["pos"].clip(lower=0), 0)*d["r1"]
            d["coin"] = c; d["wn"] = int(w[1:]); d["i"] = np.arange(len(d))
            A.append(d[["coin","wn","i","r1","pos","gain","gain_long","gain_short","gain_longup","up"]])
    B = pd.concat(A).dropna(subset=["r1"])
    P = B.groupby(["wn","i"])[["gain","gain_long","gain_short","gain_longup","r1"]].mean().reset_index().sort_values(["wn","i"])
    def stats_(x):
        eq = (1+x).cumprod(); dd = (eq/eq.cummax()-1).min()
        yr = eq.iloc[-1]**(365/len(x))-1
        return pd.Series({"mean": x.mean(), "sharpe": x.mean()/x.std()*np.sqrt(365), "maxdd": dd, "yearly": yr, "calmar": yr/abs(dd)})
    out["variants"] = pd.DataFrame({k: stats_(P[k]) for k in ["gain","gain_long","gain_short","gain_longup","r1"]}).T
    eq = (1+P["gain"]).cumprod(); dd = eq/eq.cummax()-1
    P["dd"] = dd.values
    trough = P["dd"].idxmin(); peak = eq.loc[:trough].idxmax()
    seg = P.loc[peak:trough]
    out["deepest_fall"] = pd.Series({"days": len(seg), "sum_gain": seg["gain"].sum(), "sum_long": seg["gain_long"].sum(),
                                    "sum_short": seg["gain_short"].sum(), "sum_coin": seg["r1"].sum(),
                                    "win_start": seg["wn"].iloc[0], "win_end": seg["wn"].iloc[-1]})
    out["short_gain_by_window"] = P.groupby("wn")[["gain_long","gain_short","r1"]].sum().T
    return out
