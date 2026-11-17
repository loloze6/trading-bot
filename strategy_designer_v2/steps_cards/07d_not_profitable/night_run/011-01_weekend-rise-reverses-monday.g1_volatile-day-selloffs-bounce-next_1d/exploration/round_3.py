import numpy as np, pandas as pd

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
            b["sd10"] = b["ret1"].rolling(10, min_periods=10).std()
            b["z"] = b["ret1"] / b["sd60"]
            b["vr"] = b["sd10"] / b["sd60"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["r1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["coin"] = c; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(cm)
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    act = B[B["pos"] > 0.01].dropna(subset=["vr", "ex", "z"]).copy()
    act["vrh"] = (act["vr"] > 1).astype(int)
    act["bigfall"] = (act["z"] < -1.3).astype(int)
    out["bigfall x vr>1"] = act.groupby(["bigfall", "vrh"]).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tt), gain=("gain", "mean"), sumgain=("gain", "sum"), pos=("pos", "mean"), fee=("fee", "mean"))
    act["vrq"] = pd.qcut(act["vr"], 4, labels=False)
    out["vr quartile: sum gain, sum fee, loss share"] = act.groupby("vrq").agg(n=("ex", "size"), sumgain=("gain", "sum"), sumfee=("fee", "sum"), lossbars=("gain", lambda x: (x < 0).mean()), worst=("gain", lambda x: x.quantile(0.02)))
    # by sd60 quartile within vr>1 vs <=1: graded?
    act["sdq"] = pd.qcut(act["sd60"], 3, labels=False)
    out["sd60 tercile x vr>1"] = act.groupby(["sdq", "vrh"]).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", tt), pos=("pos", "mean"))
    # worst book days
    dl = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w; dl.append(d)
    D = pd.concat(dl)
    P = D.groupby(["win", "day"]).agg(br=("book_return", "mean")).reset_index().dropna()
    thr = P["br"].quantile(0.05)
    bad = set(pd.to_datetime(P.loc[P["br"] <= thr, "day"]).dt.floor("D"))
    act["bad"] = (act["day"] + pd.Timedelta(days=1)).isin(bad)
    out["worst 5% book days: vr>1 share and loss"] = act.groupby("bad").agg(n=("ex", "size"), vr_hi_share=("vrh", "mean"), vr=("vr", "mean"), sumgain=("gain", "sum"))
    out["loss on worst days by vr>1"] = act[act["bad"]].groupby("vrh").agg(n=("gain", "size"), sumgain=("gain", "sum"), pos=("pos", "mean"))
    return out
