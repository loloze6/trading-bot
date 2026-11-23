def explore(data):
    import numpy as np, pandas as pd
    out={}
    rows=[];bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            a=b["postRebalance_current_allocation"]; pa=b["previous_allocation"]; f=b["forecast"]
            ch=(a-pa).abs()
            rows.append(pd.DataFrame({"coin":coin,"w":w,"ch_pos":(ch>1e-9).astype(float),
                "sign_agree":(np.sign(a)==np.sign(f)).astype(float),"long":(a>0).astype(float),
                "absa":a.abs(),"r":b["close"].pct_change().shift(-1)*a}))
            c=b["close"].values
            bk.append(pd.Series({"coin":coin,"w":w,"corr_a_f":np.corrcoef(a.fillna(0),f.fillna(0))[0,1],
                "share_long":(a>0).mean(),"coin_ret":c[-1]/c[0]-1,
                "book_ret":b["postRebalance_total_value"].iloc[-1]/b["postRebalance_total_value"].iloc[0]-1}))
    R=pd.concat(rows); B=pd.DataFrame(bk)
    out["bar_stats"]=pd.Series({"share_bars_pos_changes":R.ch_pos.mean(),"share_sign_alloc_eq_forecast":R.sign_agree.mean(),
        "share_long":R.long.mean(),"mean_abs_alloc":R.absa.mean()})
    B["coin_ret"]=B.coin_ret.astype(float);B["book_ret"]=B.book_ret.astype(float);B["share_long"]=B.share_long.astype(float);B["corr_a_f"]=B.corr_a_f.astype(float)
    out["corr_alloc_forecast_by_coin"]=B.groupby("coin")[["corr_a_f","share_long"]].mean()
    out["book_vs_coin_by_window"]=B.groupby("w")[["coin_ret","book_ret","share_long","corr_a_f"]].mean()
    out["corr_bookret_coinret_x_sign"]=float(np.corrcoef(B.book_ret,B.coin_ret*(2*B.share_long-1))[0,1])
    # idealised 24h fade on grid, by |f| band and vr, net of cost 0.19%
    G=[]
    for coin,ws in data["bars"].items():
        al=[]
        for w,b in ws.items():
            c=b["close"].values; idx=np.arange(0,len(c)-24,24); al.append(c[idx+24]/c[idx]-1)
        dr=np.concatenate(al).mean()
        for w,b in ws.items():
            b=b.reset_index(drop=True); c=b["close"]
            r1=c.pct_change(); s24=r1.rolling(24).std(); vr=s24/s24.rolling(720,min_periods=240).mean()
            ts=pd.to_datetime(b["timestamp"])
            idx=np.arange(0,len(c)-24,24); fr=c.values[idx+24]/c.values[idx]-1
            G.append(pd.DataFrame({"f":b["forecast"].values[idx],"vr":vr.values[idx],"fr":fr,"dr":dr,
                "year":ts.dt.year.values[idx],"hour":ts.dt.hour.values[idx]}))
    G=pd.concat(G).dropna(subset=["vr"]); G=G[G.f!=0]
    G["vrq"]=pd.qcut(G.vr,3,labels=["vlo","vmid","vhi"])
    G["fq"]=pd.qcut(G.f.abs(),5,labels=False)
    G["tot"]=np.sign(G.f)*G.fr; G["exc"]=np.sign(G.f)*(G.fr-G.dr)
    def agg(g): return pd.Series({"n":len(g),"tot%":g.tot.mean()*100,"net%":(g.tot.mean()-0.0019)*100,"t":g.exc.mean()/(g.exc.std()/np.sqrt(len(g)))})
    out["grid_fq_x_vr"]=G.groupby(["fq","vrq"]).apply(agg)
    # condition alone: coin's raw 24h move (long, minus drift) in vhi vs others, and |move|
    G["rawexc"]=G.fr-G.dr
    out["vr_alone_raw"]=G.groupby("vrq").agg(n=("fr","size"),mean_raw_exc=("rawexc",lambda x:x.mean()*100),mean_absmove=("fr",lambda x:x.abs().mean()*100))
    top=G[(G.fq==4)&(G.vrq=="vhi")]
    out["top_vhi_by_year"]=top.groupby("year").apply(agg)
    out["top_vhi_side"]=top.groupby(np.where(top.f>0,"long","short")).apply(agg)
    out["grid_hour_values"]=G.groupby("hour").size()
    return out
