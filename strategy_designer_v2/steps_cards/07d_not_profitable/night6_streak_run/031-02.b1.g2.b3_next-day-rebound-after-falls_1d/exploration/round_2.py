def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    wins = sorted(data["bars"][coins[0]].keys(), key=lambda w: int(w[1:]))
    br = []
    for c in coins:
        for w in wins:
            b = data["bars"][c].get(w)
            if b is None or len(b) < 5: continue
            b = b.copy()
            r = b["close"].pct_change()
            b["fwd"] = b["close"].shift(-1)/b["close"]-1
            b["sd60"] = r.rolling(60, min_periods=20).std()
            b["z"] = r/b["sd60"]
            b["vr"] = r.rolling(10).std()/b["sd60"]
            b["pos"] = b["postRebalance_current_allocation"]
            b["dpos"] = (b["pos"]-b["previous_allocation"]).abs()
            b["coin"] = c; b["wn"] = int(w[1:]); b["i"] = np.arange(len(b))
            br.append(b[["coin","wn","i","fwd","z","vr","forecast","pos","dpos"]])
    X = pd.concat(br).dropna(subset=["fwd"])
    X["ex"] = X["fwd"]-X.groupby("coin")["fwd"].transform("mean")
    cost = 0.0019/2
    def book(mask, name):
        p = X["pos"].where(mask, 0.0)
        # turnover approx from p changes within coin/window
        dp = p.groupby([X["coin"],X["wn"]]).diff().abs().fillna(p.abs())
        g = p*X["fwd"] - dp*cost
        d = pd.DataFrame({"wn":X["wn"],"i":X["i"],"g":g}).groupby(["wn","i"])["g"].mean().reset_index().sort_values(["wn","i"])
        v = (1+d["g"]).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = len(d)/365; yr = v.iloc[-1]**(1/yrs)-1
        sh = d["g"].mean()/d["g"].std()*np.sqrt(365)
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":sh,"share_in":mask.mean()})
    sig = X["forecast"]>0
    res = {}
    res["all signals"] = book(sig, "")
    res["z<-0.66"] = book(sig & (X["z"]<-0.66), "")
    res["z<-1.1"] = book(sig & (X["z"]<-1.1), "")
    res["vr>0.9"] = book(sig & (X["vr"]>0.9), "")
    res["vr>0.9 & z<-0.66"] = book(sig & (X["vr"]>0.9) & (X["z"]<-0.66), "")
    out["approx books (cost incl)"] = pd.DataFrame(res).T.round(4)
    S = X[sig].dropna(subset=["vr"]).copy()
    S["zb"] = pd.qcut(S["z"],3,labels=["deep","mid","shallow"])
    S["vb"] = pd.qcut(S["vr"],3,labels=["lowvr","midvr","highvr"])
    g = S.groupby(["zb","vb"]).agg(ex=("ex","mean"),sd=("fwd","std"),n=("ex","size"))
    g["t"] = g["ex"]/(g["sd"]/np.sqrt(g["n"]))
    out["z x vr on signal"] = g.round(5)
    # condition alone: high vr on non-signal and on all
    N = X[~sig].dropna(subset=["vr"])
    out["vr>0.9 alone (no signal) ex"] = pd.Series({"ex_nonsig_vr_hi":N.loc[N.vr>0.9,"ex"].mean(),"n":(N.vr>0.9).sum(),"ex_nonsig_vr_lo":N.loc[N.vr<=0.9,"ex"].mean()})
    # losses: worst decile of signal-bar gains by z bucket
    S["gain"] = S["pos"]*S["fwd"]
    out["gain sd and mean by z third"] = S.groupby("zb").agg(gmean=("gain","mean"),gsd=("gain","std"),pos=("pos","mean"),p5=("gain",lambda s: s.quantile(0.05)))
    return out
