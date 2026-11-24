import pandas as pd, numpy as np

def explore(data):
    out = {}
    bars = data["bars"]
    cs = []; allret = {}
    for c in bars:
        allret[c] = pd.concat([b["close"].pct_change().dropna() for b in bars[c].values()]).mean()
        for w, b in bars[c].items():
            b = b.copy().reset_index(drop=True)
            r = b["close"].pct_change(); sd = r.rolling(20).std()
            b["r1"] = r; b["z"] = r/sd
            b["loc"] = (b["close"]-b["low"])/(b["high"]-b["low"])
            for h in [1,2,3,5]:
                b[f"n{h}"] = b["close"].shift(-h)/b["close"]-1
            b["r5"] = b["close"]/b["close"].shift(5)-1
            b["r20"] = b["close"]/b["close"].shift(20)-1
            b["volrel"] = sd/sd.rolling(60, min_periods=20).mean()
            b["rng"] = (b["high"]-b["low"])/b["close"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["case"] = b["regime"] == "mean_reversion"
            b["coin"] = c; b["wn"] = int(w[1:]); b["pos"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["year"] = b["day"].dt.year
            b["drift"] = allret[c]
            cs.append(b)
    A = pd.concat(cs, ignore_index=True)
    A["ex1"] = A["n1"] - A["drift"]
    C = A[A["case"] & A["n1"].notna()].copy()
    ncoins = A["coin"].nunique()
    cost = 0.0019
    # simulated book: each case-day, mean over coins of alloc*next - cost*alloc, others 0
    def book(mask, sizecol="alloc", label=""):
        x = C[mask].copy()
        x["g"] = x[sizecol]*x["n1"] - cost*x[sizecol]
        daily = x.groupby(["wn","day"])["g"].sum()/ncoins
        allday = A.groupby(["wn","day"]).size().index
        s = pd.Series(0.0, index=allday); s.loc[daily.index] = daily.values
        s = s.sort_index()
        v = (1+s).cumprod(); mdd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(s))-1
        return {"n": int(mask.sum()), "yearly": yr, "maxdd": mdd, "calmar": yr/abs(mdd),
                "sharpe": s.mean()/s.std()*np.sqrt(365)}
    m = pd.Series(True, index=C.index)
    res = {"all": book(m)}
    res["volrel>1"] = book(C["volrel"] > 1)
    res["volrel>0.9"] = book(C["volrel"] > 0.9)
    res["r1<-0.08"] = book(C["r1"] < -0.08)
    res["r1<-0.1"] = book(C["r1"] < -0.1)
    res["rng>0.107"] = book(C["rng"] > 0.107)
    res["r5<-0.08"] = book(C["r5"] < -0.08)
    res["r20>-0.2"] = book(C["r20"] > -0.2)
    out["sim books"] = pd.DataFrame(res).T
    # deepest fall episode of real book: cases around w14 and w20-24
    out["cases w14"] = C[C["wn"]==14][["coin","z","r1","r5","r20","volrel","alloc","n1"]].reset_index(drop=True)
    out["cases w20-24 summary"] = C[C["wn"]>=20].groupby("wn").agg(n=("n1","size"), mean=("n1","mean"), volrel=("volrel","mean"), r20=("r20","mean"))
    # longer horizons of cases, by volrel bins
    C["vb"] = pd.qcut(C["volrel"], 3).astype(str)
    out["horizons by volrel"] = C.groupby("vb")[["n1","n2","n3","n5"]].mean()
    C["rb"] = pd.qcut(C["r1"], 3).astype(str)
    out["horizons by r1"] = C.groupby("rb")[["n1","n2","n3","n5"]].mean()
    # condition alone check: bars where condition holds without the signal
    def alone(cond, name):
        g = A[A["n1"].notna() & (A["pos"] % 1 == 0)]
        a = g[cond.loc[g.index] & ~g["case"]]["ex1"]; b = g[cond.loc[g.index] & g["case"]]["ex1"]
        return {"cond_only_n": len(a), "cond_only_mean": a.mean(), "cond_only_t": a.mean()/(a.std()/np.sqrt(len(a))),
                "both_n": len(b), "both_mean": b.mean()}
    out["alone volrel>1"] = pd.Series(alone(A["volrel"] > 1, "v"))
    out["alone r1<-0.08"] = pd.Series(alone(A["r1"] < -0.08, "r"))
    out["alone rng>0.107"] = pd.Series(alone(A["rng"] > 0.107, "g"))
    out["alone r5<-0.08"] = pd.Series(alone(A["r5"] < -0.08, "r5"))
    return out
