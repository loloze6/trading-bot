def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    grid=[]; rows=[]
    for coin,ws in data["bars"].items():
        g7=[]
        for w,b in ws.items():
            c=b["close"].values
            for i in range(0,len(c)-7,7): g7.append(c[i+7]/c[i]-1)
        m7=np.mean(g7)
        m1=np.nanmean(np.concatenate([b["close"].pct_change().values for b in ws.values()]))
        for w,b in ws.items():
            c=b["close"].values; n=len(c)
            z=b["debug_info.components.fall_short.last_history_value"].values
            ret14=pd.Series(c).pct_change(14).values
            ret60=pd.Series(c).pct_change(60).values
            ret30=pd.Series(c).pct_change(30).values
            vol=pd.Series(c).pct_change().rolling(30).std().values
            pos=b["postRebalance_current_allocation"].values
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            rows.append(pd.DataFrame({"coin":coin,"w":w,"yr":yr,"pos":pos,"r1":r1,"gain":pos*r1,"mkt":pos*m1,"fc":b["forecast"].values}))
            for i in range(0,n-7,7):
                grid.append((coin,w,yr[i],z[i],ret14[i],ret30[i],ret60[i],vol[i],b["forecast"].values[i],c[i+7]/c[i]-1-m7,abs(pos[i])))
    G=pd.DataFrame(grid,columns=["coin","w","yr","z","r14","r30","r60","vol","fc","ex","apos"])
    d=pd.concat(rows)
    out={}
    F=G[G.r14<0].copy()
    F["q"]=pd.qcut(F["r14"]/F["vol"],6)
    out["fall_grade_r14_over_vol"]=F.groupby("q")["ex"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    F["fq"]=pd.cut(F["fc"],[-6,-4,-2,-0.01,0.01,6])
    out["fall_by_fc"]=F.groupby("fq")["ex"].agg(["count","mean"])
    U=G[G.r14>0].copy()
    U["q"]=pd.qcut(U["r14"]/U["vol"],5)
    out["rise_grade"]=U.groupby("q")["ex"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    F["t60"]=np.sign(F["r60"])
    out["fall_by_60d_sign"]=F.groupby("t60")["ex"].agg(["count","mean",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["fall_by_year"]=F.groupby("yr")["ex"].agg(["count","mean"])
    out["fall_by_coin"]=F.groupby("coin")["ex"].agg(["count","mean"])
    out["abs_pos_when_active"]=d[d.fc!=0]["pos"].abs().describe()
    d["s"]=np.sign(d.pos.round(3))
    out["book_by_year"]=d.groupby("yr").agg(gain_bp=("gain",lambda x:x.mean()*1e4),r1_bp=("r1",lambda x:x.mean()*1e4),short_share=("s",lambda x:(x<0).mean()),flat=("s",lambda x:(x==0).mean()))
    sl=stats.linregress(F["r14"]/F["vol"],F["ex"])
    out["slope_fall_ex_on_r14vol"]=pd.Series({"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(F)})
    return out
