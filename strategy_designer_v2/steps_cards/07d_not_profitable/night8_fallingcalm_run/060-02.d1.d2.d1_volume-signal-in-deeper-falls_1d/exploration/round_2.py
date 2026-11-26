def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    R = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]; vol = b["volume"]
            b["r1"] = cl.shift(-1)/cl-1
            b["ret20"] = cl/cl.shift(20)-1
            b["ret5p"] = cl/cl.shift(5)-1
            b["ret10p"] = cl/cl.shift(10)-1
            b["vr"] = np.log(vol.rolling(30).mean()/vol.shift(30).rolling(30).mean())
            lr = np.log(cl).diff()
            b["s10"] = lr.rolling(10).std(); b["s30"] = lr.rolling(30).std()
            b["fwd5"] = cl.shift(-5)/cl-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1"]
            b["coin"] = c; b["wn"] = int(w[1:]); b["t"] = np.arange(len(b))
            R.append(b[["timestamp","t","coin","wn","pos","gain","r1","ret20","ret5p","ret10p","vr","s10","s30","fwd5","forecast","regime"]])
    R = pd.concat(R)
    R["side"] = np.where(R["pos"]>1e-9,"long",np.where(R["pos"]<-1e-9,"short","flat"))
    # deepest fall w14: per coin gain and side, conditions
    W = R[R["wn"]==14].copy()
    W["day"] = W["timestamp"].astype(str).str[:10]
    bk = W.groupby("day")["gain"].mean()
    v = (1+bk).cumprod().values; pk = np.maximum.accumulate(v); dd = v/pk-1
    i = int(np.argmin(dd)); p = int(np.argmax(v[:i+1]))
    days = bk.index[p+1:i+1]
    E = W[W["day"].isin(days)]
    out["w14 fall by coin side"] = E.groupby(["coin","side"]).agg(n=("gain","size"), gain_sum=("gain","sum"), pos_mean=("pos","mean"),
        ret20=("ret20","mean"), ret5p=("ret5p","mean"), vr=("vr","mean"), s10s30=("s10","mean"))
    out["w14 fall coin returns"] = E.groupby("coin")["r1"].sum()
    out["w14 fall day position"] = f"days {p+1}..{i} of window, of {len(bk)}"
    # all-coin: 5-day trade grid view: gain by side x ret10p (rebound before) and vol ratio s10/s30
    H = R[R["side"]!="flat"].copy()
    H["sv"] = pd.cut(H["s10"]/H["s30"], [0,0.8,1.0,1.25,10])
    out["gain side x s10/s30"] = H.groupby(["side","sv"],observed=True)["gain"].agg(["count","mean","sum"])
    H["p10"] = pd.cut(H["ret10p"], [-1,-0.2,-0.1,0,0.1,1])
    out["gain side x past10d"] = H.groupby(["side","p10"],observed=True)["gain"].agg(["count","mean","sum"])
    # proxy book and calmar for variants
    def calmar(mask):
        G = R.copy(); G["g"] = np.where(mask, G["gain"], 0.0)
        G["day"] = G["timestamp"].astype(str).str[:10]
        bk = G.groupby(["wn","day"])["g"].mean().sort_index()
        v = (1+bk).cumprod().values; dd = (v/np.maximum.accumulate(v)-1).min()
        yr = v[-1]**(365/len(v))-1
        return pd.Series({"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"sharpe":bk.mean()/bk.std()*np.sqrt(365)})
    base = R["side"]!="flat"
    sv = R["s10"]/R["s30"]
    out["variants"] = pd.DataFrame({
        "base": calmar(base),
        "short only": calmar(R["side"]=="short"),
        "long only ret20<-40%": calmar((R["side"]=="short")|((R["side"]=="long")&(R["ret20"]<-0.4))),
        "no long after 5d rise>5%": calmar(base & ~((R["side"]=="long")&(R["ret5p"]>0.05))),
        "no pos s10/s30>1.25": calmar(base & ~(sv>1.25)),
        "no short after 10d rise": calmar(base & ~((R["side"]=="short")&(R["ret10p"]>0))),
    }).T
    # condition check on 5-day grid within regime (falling, ret20<-10%): fwd5 by vr sign and depth, signal vs not
    G = R[(R["t"]%5==0) & (R["ret20"]<-0.1)].dropna(subset=["fwd5","vr"]).copy()
    G["dd"] = pd.cut(G["ret20"], [-1,-0.4,-0.2,-0.1])
    G["vs"] = np.where(G["vr"]>0,"vol up","vol down")
    out["grid fwd5 by depth x vol sign"] = G.groupby(["dd","vs"],observed=True)["fwd5"].agg(["count","mean","std"])
    return out
