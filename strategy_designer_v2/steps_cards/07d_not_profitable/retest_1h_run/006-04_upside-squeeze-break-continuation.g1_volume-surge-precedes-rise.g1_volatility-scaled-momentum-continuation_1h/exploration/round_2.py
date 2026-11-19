def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for c in coins:
        for w, d in data["days"][c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"]=c; dd["wn"]=int(w[1:])
            rows.append(dd)
    D = pd.concat(rows)
    book = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    eq = (1+book.book_return).cumprod().values
    peak = np.maximum.accumulate(eq)
    ddv = eq/peak-1
    i_trough = int(np.argmin(ddv)); i_peak = int(np.argmax(eq[:i_trough+1]))
    idx = book.index
    seg = book.iloc[i_peak+1:i_trough+1]
    out["deepest_fall"] = pd.Series({"peak_wn":idx[i_peak][0],"trough_wn":idx[i_trough][0],"days":i_trough-i_peak,
        "dd":ddv[i_trough],"book_sum":seg.book_return.sum(),"hold_sum":seg.coin_return.sum()})
    # fall by window: book drawdown within window segments
    segw = seg.reset_index().groupby("wn").agg(n=("book_return","size"),book=("book_return","sum"),hold=("coin_return","sum"))
    out["fall_by_window"]=segw.round(4)
    # per coin contribution during fall
    Dm = D.set_index(["wn","day"])
    keys = set(seg.index)
    Df = D[[ (a,b) in keys for a,b in zip(D.wn,D.day)]]
    out["fall_by_coin"]=Df.groupby("coin").agg(book=("book_return","sum"),hold=("coin_return","sum")).round(4)
    # bar features
    brs=[]
    for c in coins:
        for w,b in data["bars"][c].items():
            x = b[["close","high","low","volume","forecast","postRebalance_current_allocation"]].copy()
            x["r1"]=x.close.shift(-1)/x.close-1
            r=x.close/x.close.shift(1)-1
            x["pos"]=x.postRebalance_current_allocation
            x["gain"]=x.pos*x.r1
            x["vol24"]=r.rolling(24).std(); x["vol480"]=r.rolling(480).std()
            x["vr"]=x.vol24/x.vol480
            x["ret24"]=x.close/x.close.shift(24)-1
            x["ret240"]=x.close/x.close.shift(240)-1
            x["z240"]=x.ret240/(x.vol480*np.sqrt(240))
            x["dhi"]=x.close/x.high.rolling(240).max()-1
            x["f72"]=x.close.shift(-72)/x.close-1
            x["coin"]=c; x["wn"]=int(w[1:])
            brs.append(x)
    B=pd.concat(brs)
    H=B[B.pos>0.5].copy()
    out["n_heavy"]=len(H)
    def tab(col,q=5):
        H["q"]=pd.qcut(H[col].rank(method="first"),q,labels=False)
        g=H.groupby("q").agg(n=("gain","size"),m=(col,"mean"),pos=("pos","mean"),gain=("gain","mean"),r1=("r1","mean"))
        g["t"]=H.groupby("q").gain.apply(lambda s:s.mean()/s.std()*np.sqrt(len(s)))
        g["sum_gain"]=g.gain*g.n
        return g
    out["heavy_by_vr"]=tab("vr")
    out["heavy_by_z240"]=tab("z240")
    out["heavy_by_ret24"]=tab("ret24")
    out["heavy_by_dhi"]=tab("dhi")
    out["heavy_by_vol480"]=tab("vol480")
    # grid 72 among forecast>0 by vol480 quartile and ret24
    G=pd.concat([x.iloc[::72] for _,x in B.groupby(["coin","wn"])]).dropna(subset=["f72"])
    mu72=G.groupby("coin").f72.mean(); G["ex"]=G.f72-G.coin.map(mu72)
    GL=G[G.forecast>0].copy()
    for col in ["vol480","ret24","dhi"]:
        GL["q"]=pd.qcut(GL[col].rank(method="first"),4,labels=False)
        out["grid_by_"+col]=GL.groupby("q").agg(n=("ex","size"),m=(col,"mean"),ex=("ex","mean"),t=("ex",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    # vr x top forecast
    GL["top"]=GL.forecast>=GL.forecast.quantile(0.8)
    GL["vh"]=GL.vr>GL.vr.median()
    out["grid_top_x_vr"]=GL.groupby(["top","vh"]).agg(n=("ex","size"),ex=("ex","mean"),t=("ex",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    return out
