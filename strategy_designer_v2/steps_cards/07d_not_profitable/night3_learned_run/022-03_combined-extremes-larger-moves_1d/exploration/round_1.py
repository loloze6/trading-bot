import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 5
    comps = ["combined","s_momentum","s_reversal","s_high","s_volatility"]
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c)-H, H)
            rr.append(c[idx+H]/c[idx]-1)
        drift[coin] = np.concatenate(rr).mean() if rr else 0
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            fwd = c.shift(-H)/c - 1
            r1 = c.pct_change()
            mom = c/c.shift(28)-1
            vol = r1.rolling(30).std()
            near = c/c.rolling(90).max()
            df = pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                               "fwd":fwd,"un":fwd-drift[coin],"mom28":mom,"rev1":-r1,"near90":near,"vol30":vol,
                               "alloc":b["postRebalance_current_allocation"],"fc":b["forecast"],
                               "pos":np.arange(len(b))})
            for k in comps:
                df[k] = b.get(f"debug_info.components.{k}.last_history_value")
            df["cpp"] = b.get("debug_info.components.combined.post_pipeline_value")
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.pos % H == 0) & A.fwd.notna()].copy()
    # signed unusual move per component, top10% and all, and by sign
    res = []
    for k in comps:
        g = G[G[k].notna()]
        thr = g[k].abs().quantile(0.9)
        t = g[g[k].abs() >= thr]
        s = np.sign(t[k]) * t["un"]
        sa = np.sign(g[k])*g["un"]
        res.append({"comp":k,"n_top":len(t),"top_mean":s.mean(),"top_t":s.mean()/s.std()*np.sqrt(len(s)),
                    "all_mean":sa.mean(),"all_t":sa.mean()/sa.std()*np.sqrt(len(sa)),
                    "share_pos":(g[k]>0).mean(),
                    "corr_k_un":g[[k,"un"]].corr().iloc[0,1]})
    out["comp_moves"] = pd.DataFrame(res)
    # raw features: rank corr with fwd by year (pooled per coin z)
    feats = ["mom28","rev1","near90","vol30"]
    fr = []
    for y, g in G.groupby("year"):
        d = {"year":y,"n":len(g)}
        for f in feats:
            gg = g[[f,"un"]].dropna()
            d[f] = stats.spearmanr(gg[f], gg["un"])[0] if len(gg)>20 else np.nan
        fr.append(d)
    out["feat_spearman_by_year"] = pd.DataFrame(fr)
    d = {}
    for f in feats:
        gg = G[[f,"un"]].dropna()
        rho,p = stats.spearmanr(gg[f], gg["un"]); d[f]=(round(rho,4),len(gg),round(p,4))
    out["feat_spearman_all"] = pd.Series({k:str(v) for k,v in d.items()})
    # quintile of vol30 (coin-relative rank) vs fwd and |fwd|
    G["volq"] = G.groupby("coin")["vol30"].rank(pct=True)
    G["volb"] = pd.cut(G["volq"],[0,.2,.4,.6,.8,1.0],labels=False)
    out["vol_quintile"] = G.groupby("volb").agg(n=("un","size"),fwd=("fwd","mean"),absfwd=("fwd",lambda x: x.abs().mean()))
    G["momq"] = pd.cut(G.groupby("coin")["mom28"].rank(pct=True),[0,.2,.4,.6,.8,1.0],labels=False)
    out["mom_quintile"] = G.groupby("momq").agg(n=("un","size"),un=("un","mean"),t=("un",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    G["nearq"] = pd.cut(G.groupby("coin")["near90"].rank(pct=True),[0,.2,.4,.6,.8,1.0],labels=False)
    out["near_quintile"] = G.groupby("nearq").agg(n=("un","size"),un=("un","mean"),t=("un",lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # book: long vs short gain, per day
    A["nxt"] = A.groupby(["coin","w"])["fwd"].transform(lambda s: s)  # placeholder
    gains=[]
    for coin, ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].values; a=b["postRebalance_current_allocation"].values
            g=a[:-1]*(c[1:]/c[:-1]-1)
            gains.append(pd.DataFrame({"a":a[:-1],"g":g}))
    Gb=pd.concat(gains)
    out["gain_by_side"]=pd.DataFrame({"long":[ (Gb.a>0).mean(), Gb.g[Gb.a>0].mean(), Gb.g[Gb.a>0].sum()],
                                      "short":[(Gb.a<0).mean(), Gb.g[Gb.a<0].mean(), Gb.g[Gb.a<0].sum()]},
                                     index=["share_bars","mean_gain","sum_gain"])
    # trades
    T = pd.concat([t for ws in data["trades"].values() for t in ws.values() if len(t)])
    out["trades"] = T.groupby("side").agg(n=("side","size"),pl=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_days=("duration_minutes",lambda x:x.mean()/1440))
    # book daily by year
    D = pd.concat([dd.assign(coin=c, w=w) for c,ws in data["days"].items() for w,dd in ws.items()])
    D["year"]=pd.to_datetime(D["day"]).dt.year
    daily = D.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).reset_index()
    daily["year"]=pd.to_datetime(daily["day"]).dt.year
    out["book_by_year"]=daily.groupby("year").agg(n=("b","size"),book=("b","mean"),hold=("h","mean"),
        bsh=("b",lambda x:x.mean()/x.std()*np.sqrt(365)))
    return out
