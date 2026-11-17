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
            b["sd10"] = b["ret1"].rolling(10, min_periods=10).std()
            b["z"] = b["ret1"] / b["sd60"]
            b["ret20"] = cl / cl.shift(20) - 1
            b["z20"] = b["ret20"] / (b["sd60"] * np.sqrt(20))
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["r1"]
            b["coin"] = c; b["win"] = w
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    cm = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(cm)
    act = B[(B["pos"] > 0.01)].dropna(subset=["z20", "ex"]).copy()
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x)))
    act["az"] = act["z20"].abs()
    act["azq"] = pd.qcut(act["az"], 5, labels=False)
    out["by |20d vol-scaled return| quintile"] = act.groupby("azq").agg(n=("ex", "size"), az=("az", "mean"), ex=("ex", "mean"), t=("ex", tt), gain=("gain", "mean"), pos=("pos", "mean"))
    act["zq"] = pd.qcut(act["z20"], 5, labels=False)
    out["by signed 20d vol-scaled return quintile"] = act.groupby("zq").agg(n=("ex", "size"), z20=("z20", "mean"), ex=("ex", "mean"), t=("ex", tt), gain=("gain", "mean"))
    act["vr"] = act["sd10"] / act["sd60"]
    act["vrq"] = pd.qcut(act["vr"], 4, labels=False)
    out["by sd10/sd60 quartile"] = act.groupby("vrq").agg(n=("ex", "size"), vr=("vr", "mean"), ex=("ex", "mean"), t=("ex", tt), gain=("gain", "mean"), pos=("pos", "mean"))
    # gain from sizing: pos-weighted ex vs equal
    act["sdq"] = pd.qcut(act["sd60"], 4, labels=False)
    out["sd60 quartile: ex t and pos-weighted ex"] = act.groupby("sdq").apply(lambda g: pd.Series({"n": len(g), "ex": g["ex"].mean(), "t": tt(g["ex"]), "posw_ex": (g["ex"] * g["pos"]).sum() / g["pos"].sum(), "pos": g["pos"].mean()}))
    # deepest falls: portfolio daily
    dl = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = c; d["win"] = w; dl.append(d)
    D = pd.concat(dl)
    D["wn"] = D["win"].str[1:].astype(int)
    P = D.groupby(["wn", "day"]).agg(br=("book_return", "mean")).reset_index().dropna().sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + P["br"]).cumprod(); P["dd"] = (eq / eq.cummax() - 1).values
    # worst 5% book days: state of active coins that day
    thr = P["br"].quantile(0.05)
    bad = set(pd.to_datetime(P.loc[P["br"] <= thr, "day"]).dt.floor("D"))
    B["d1"] = B["day"] + pd.Timedelta(days=1)
    act2 = B[(B["pos"] > 0.01)].dropna(subset=["z20"]).copy()
    act2["bad"] = act2["d1"].isin(bad)
    out["active bars before worst 5% book days vs others"] = act2.groupby("bad").agg(n=("ex", "size"), z=("z", "mean"), z20=("z20", "mean"), sd60=("sd60", "mean"), vr=("sd10", "mean"), pos=("pos", "mean"), ex=("ex", "mean"))
    # consecutive-fall runs: is position after second big fall worse?
    act["prevz"] = np.nan
    B["prevz"] = B.groupby(["coin", "win"])["z"].shift(1)
    a3 = B[(B["pos"] > 0.01)].dropna(subset=["prevz", "ex"]).copy()
    a3["pq"] = pd.qcut(a3["prevz"], 4, labels=False)
    out["by previous day's z quartile"] = a3.groupby("pq").agg(n=("ex", "size"), prevz=("prevz", "mean"), ex=("ex", "mean"), t=("ex", tt), gain=("gain", "mean"))
    return out
