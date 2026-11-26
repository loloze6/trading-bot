def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    R = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]; vol = b["volume"]
            b["r1"] = cl.shift(-1)/cl-1
            b["ret20"] = cl/cl.shift(20)-1
            b["ret60"] = cl/cl.shift(60)-1
            b["ret5p"] = cl/cl.shift(5)-1
            b["vr"] = np.log(vol.rolling(30).mean()/vol.shift(30).rolling(30).mean())
            b["fwd5"] = cl.shift(-5)/cl-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1"]
            b["coin"] = c; b["wn"] = int(w[1:]); b["t"] = np.arange(len(b))
            b["day"] = b["timestamp"].astype(str).str[:10]
            R.append(b[["day","t","coin","wn","pos","gain","ret20","ret60","ret5p","vr","fwd5","forecast"]])
    R = pd.concat(R)
    R["side"] = np.where(R["pos"]>1e-9,"long",np.where(R["pos"]<-1e-9,"short","flat"))
    # w14 deepest fall from the book's own days
    rows = []
    for c in days:
        d = days[c]["w14"][["day","book_return"]].copy(); d["coin"]=c; rows.append(d)
    D = pd.concat(rows); D["day"]=D["day"].astype(str).str[:10]
    bk = D.groupby("day")["book_return"].mean().fillna(0).sort_index()
    v = (1+bk).cumprod().values; dd = v/np.maximum.accumulate(v)-1
    i = int(np.argmin(dd)); p = int(np.argmax(v[:i+1]))
    fd = bk.index[p+1:i+1]
    E = R[(R["wn"]==14)&(R["day"].isin(fd))]
    out["w14 fall"] = f"depth {dd[i]:.4f}, days {p+1}..{i} of {len(bk)}"
    out["w14 fall by coin side"] = E.groupby(["coin","side"]).agg(n=("gain","size"), gain_sum=("gain","sum"),
        pos=("pos","mean"), ret20=("ret20","mean"), ret5p=("ret5p","mean"), vr=("vr","mean"))
    # condition checks on 5-day grid, falling profile (ret60<-10%)
    G = R[(R["t"]%5==0)&(R["ret60"]<-0.1)].dropna(subset=["fwd5","vr","ret20"]).copy()
    G["deep"] = np.where(G["ret20"]<-0.4,"ret20<-40%",np.where(G["ret20"]<-0.1,"-40..-10%","above -10%"))
    G["vs"] = np.where(G["vr"]>0,"vol up","vol down")
    out["fwd5 by depth x vol sign (falling)"] = G.groupby(["deep","vs"])["fwd5"].agg(["count","mean"])
    G["rb"] = np.where(G["ret5p"]>0.05,"5d rise>5%","not")
    S = G[G["ret20"]<-0.1]
    out["fwd5 by 5d rise x vol sign (ret20<-10%)"] = S.groupby(["rb","vs"])["fwd5"].agg(["count","mean"])
    # longs of the book by 5d rise, total move held 5d
    H = R[(R["side"]=="long")]
    out["long gain by 5d rise and depth"] = H.assign(rb=np.where(H["ret5p"]>0.05,"rise","not"),
        deep=np.where(H["ret20"]<-0.4,"deep","not")).groupby(["deep","rb"])["gain"].agg(["count","mean","sum"])
    return out
