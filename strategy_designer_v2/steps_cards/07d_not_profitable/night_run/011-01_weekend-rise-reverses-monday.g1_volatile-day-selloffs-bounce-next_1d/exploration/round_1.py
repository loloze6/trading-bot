import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy().reset_index(drop=True)
            cl = b["close"]
            b["r1"] = cl.shift(-1) / cl - 1
            b["ret1"] = cl / cl.shift(1) - 1
            b["sd60"] = b["ret1"].rolling(60, min_periods=60).std()
            b["z"] = b["ret1"] / b["sd60"]
            b["ret20"] = cl / cl.shift(20) - 1
            b["ret60"] = cl / cl.shift(60) - 1
            b["ret5"] = cl / cl.shift(5) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["r1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["coin"] = c; b["win"] = w
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(cm)
    act = B[B["pos"] > 0.01].copy()
    out["active share, mean pos, mean gain/bar on active, mean fee/bar all"] = pd.Series({
        "active_share": len(act) / len(B), "mean_pos": act["pos"].mean(),
        "gain_active": act["gain"].mean(), "gain_per_bar_all": B["gain"].mean(),
        "fee_per_bar_all": B["fee"].mean(), "n_active": len(act)})
    # gain by forecast bin
    act["fbin"] = pd.cut(act["forecast"], [0, 1, 3, 6, 10, 20.01])
    out["by forecast bin"] = act.groupby("fbin").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "mean"), pos=("pos", "mean"), fee=("fee", "mean"))
    # trend states
    act["t60"] = np.sign(act["ret60"])
    act["t20q"] = pd.qcut(act["ret20"], 4, labels=False)
    out["by 60d trend sign"] = act.groupby("t60").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "mean"), sumgain=("gain", "sum"))
    out["by 20d return quartile"] = act.groupby("t20q").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "mean"), sumgain=("gain", "sum"), r20=("ret20", "mean"))
    act["vq"] = pd.qcut(act["sd60"], 4, labels=False)
    out["by sd60 quartile"] = act.groupby("vq").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "mean"), sumgain=("gain", "sum"), pos=("pos", "mean"))
    out["by weekday"] = act.groupby("wd").agg(n=("ex", "size"), ex=("ex", "mean"), gain=("gain", "mean"))
    act["zq"] = pd.qcut(act["z"], 4, labels=False)
    out["by z quartile"] = act.groupby("zq").agg(n=("ex", "size"), z=("z", "mean"), ex=("ex", "mean"), gain=("gain", "mean"), pos=("pos", "mean"))
    # holding duration: run lengths of pos>0
    # book daily
    dl = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w; dl.append(d)
    D = pd.concat(dl)
    D["wn"] = D["win"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().dropna()
    P = P.sort_values(["wn", "day"])
    eq = (1 + P["br"]).cumprod()
    dd = eq / eq.cummax() - 1
    P["dd"] = dd.values
    out["book stats"] = pd.Series({"mean": P["br"].mean(), "sharpe": P["br"].mean() / P["br"].std() * np.sqrt(365), "maxdd": dd.min(), "n_days": len(P), "hold_mean": P["cr"].mean()})
    out["book by window"] = P.groupby("wn").agg(br=("br", "sum"), cr=("cr", "sum"), mindd=("dd", "min"))
    # worst book days: coin state
    P["year"] = pd.to_datetime(P["day"]).dt.year
    out["book by year"] = P.groupby("year").agg(br=("br", "mean"), cr=("cr", "mean"), n=("br", "size"))
    return out
