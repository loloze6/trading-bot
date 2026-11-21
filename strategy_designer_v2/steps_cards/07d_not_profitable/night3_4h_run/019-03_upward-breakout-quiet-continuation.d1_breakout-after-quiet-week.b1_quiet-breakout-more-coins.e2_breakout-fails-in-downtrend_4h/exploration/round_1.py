import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars=data["bars"]; trades=data["trades"]; days=data["days"]
    out={}
    # coin mean 72-bar drift and mean bar return
    rows=[]; brow=[]; drow=[]
    for coin in bars:
        allr=[]; r1=[]
        for w,b in bars[coin].items():
            c=b["close"].values
            idx=np.arange(0,len(c)-72,72)
            allr+=list(c[idx+72]/c[idx]-1)
            r1+=list(c[1:]/c[:-1]-1)
        drift=np.mean(allr); sd=np.std(allr); m1=np.mean(r1)
        for w,b in bars[coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values; h=b["high"].values; l=b["low"].values
            n=len(c)
            pos=b["postRebalance_current_allocation"].fillna(0).values
            nxt=np.r_[c[1:]/c[:-1]-1,np.nan]
            brow.append(dict(coin=coin,w=w,gain=np.nansum(pos[:-1]*nxt[:-1]),mkt=np.sum(pos[:-1])*m1,expo=np.mean(np.abs(pos)),meanpos=np.mean(pos)))
            ret30=pd.Series(c).pct_change(180).values
            ret90=pd.Series(c).pct_change(540).values
            ret7=pd.Series(c).pct_change(42).values
            rng=(pd.Series(h).rolling(12).max()-pd.Series(l).rolling(12).min())/pd.Series(c)
            rngq=(rng/rng.rolling(180).mean()).shift(1).values
            vol=pd.Series(c).pct_change().rolling(180).std().values
            hh=pd.Series(h).rolling(12).max().shift(1).values
            fc=b["forecast"].fillna(0).values
            ent=np.where((fc<0)&(np.r_[0,fc[:-1]]==0))[0]
            for i in ent:
                if i+72>=n: continue
                fr=c[i+72]/c[i]-1
                rows.append(dict(coin=coin,w=w,fc=fc[i],tot=-fr,unus=-(fr-drift),strength=-(fr-drift)/sd,ret30=ret30[i],ret90=ret90[i],ret7=ret7[i],rngq=rngq[i],brk=c[i]/hh[i]-1 if hh[i]==hh[i] else np.nan,vol=vol[i],
                    r12=-(c[i+12]/c[i]-1),r36=-(c[i+36]/c[i]-1),r144=-(c[i+144]/c[i]-1) if i+144<n else np.nan, pos=pos[i]))
        for w,d in days[coin].items():
            drow.append(d.assign(coin=coin,w=w)[["coin","w","book_return","coin_return"]])
    E=pd.DataFrame(rows); B=pd.DataFrame(brow); D=pd.concat(drow).dropna()
    out["n_entries"]=len(E)
    out["entry_means"]=E[["tot","unus","strength","r12","r36","r144","pos"]].agg(["mean","count"]).T.assign(t=lambda x: E[x.index].mean()/E[x.index].std()*np.sqrt(E[x.index].count()) if False else [stats.ttest_1samp(E[k].dropna(),0).statistic for k in x.index])
    out["gain_vs_mkt_by_coin"]=B.groupby("coin")[["gain","mkt","expo","meanpos"]].agg({"gain":"sum","mkt":"sum","expo":"mean","meanpos":"mean"})
    out["gain_total"]=pd.Series(dict(gain=B.gain.sum(),mkt=B.mkt.sum(),timing=B.gain.sum()-B.mkt.sum()))
    D["wn"]=D.w.str[1:].astype(int)
    out["book_by_window"]=D.groupby("wn").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    def grp(col,q=4):
        x=E.dropna(subset=[col]).copy(); x["g"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("g").agg(lo=(col,"min"),hi=(col,"max"),n=("tot","size"),tot=("tot","mean"),unus=("unus","mean"),tstat=("tot",lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    for col in ["ret30","ret90","ret7","rngq","brk","vol","fc"]:
        out["by_"+col]=grp(col)
    tr=[]
    for coin in trades:
        for w,t in trades[coin].items():
            tr.append(t)
    T=pd.concat(tr)
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda s:s.mean()/60))
    return out
