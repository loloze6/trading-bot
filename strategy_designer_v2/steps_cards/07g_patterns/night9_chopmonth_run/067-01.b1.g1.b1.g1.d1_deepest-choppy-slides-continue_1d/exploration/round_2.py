import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,df in wins.items():
            c=df["close"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1=c.pct_change()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(c)),"date":ts.dt.floor("D"),
                "yr":ts.dt.year,"r60":c/c.shift(60)-1,"r30":c/c.shift(30)-1,"r1":r1,
                "sd30":r1.rolling(30).std(),"f10":c.shift(-10)/c-1,"f5":c.shift(-5)/c-1,
                "f1":c.shift(-1)/c-1,"wd":ts.dt.weekday})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in [1,5,10]:
        g=D[D.pos%h==0]
        D[f"x{h}"]=D[f"f{h}"]-D.coin.map(g.groupby("coin")[f"f{h}"].mean())
    D["z30"]=D.r30/(D.sd30*np.sqrt(30))
    out={}
    def daycl_t(s,col):
        v=s.groupby("date")[col].sum(); n=s.groupby("date").size()
        m=s[col].mean()
        dev=(s[col]-m).groupby(s.date).sum()
        se=np.sqrt((dev**2).sum())/len(s)
        return m/se, len(v)
    for h in [5,10]:
        g=D[(D.pos%h==0)&(D.r60.abs()<=0.10)].dropna(subset=["z30",f"x{h}"]).copy()
        g["sx"]=np.sign(g.z30)*g[f"x{h}"]
        g["sf"]=np.sign(g.z30)*g[f"f{h}"]
        res={}
        for nm,s in [("all",g),("up",g[g.z30>0]),("down",g[g.z30<0]),
                     ("|z|>1",g[g.z30.abs()>1]),("|z|<=1",g[g.z30.abs()<=1])]:
            t,nd=daycl_t(s,"sx")
            res[nm]={"n":len(s),"days":nd,"mean_dir_excess":s.sx.mean(),"t_day":t,
                     "mean_dir_total":s.sf.mean(),"rho_z_x":stats.spearmanr(s.z30,s[f"x{h}"])[0]}
        out[f"choppy z30 sign*x{h}"]=pd.DataFrame(res).T
        out[f"choppy plain r30 rho x{h}"]=pd.Series({"rho":stats.spearmanr(g.r30,g[f"x{h}"])[0],"p":stats.spearmanr(g.r30,g[f"x{h}"])[1]})
        out[f"choppy by window x{h}"]=g.groupby("win").apply(lambda s: pd.Series({"n":len(s),"mean_sx":s.sx.mean(),"rho":stats.spearmanr(s.z30,s[f"x{h}"])[0] if len(s)>4 else np.nan}))
        out[f"choppy by coin x{h}"]=g.groupby("coin").apply(lambda s: pd.Series({"n":len(s),"mean_sx":s.sx.mean()}))
        # wider band to check choppiness specificity
    for lo,hi,nm in [(-0.2,-0.1,"fall mild"),(0.1,0.2,"rise mild"),(-1,-0.2,"fall strong"),(0.2,9,"rise strong")]:
        g=D[(D.pos%10==0)&(D.r60>lo)&(D.r60<=hi)].dropna(subset=["z30","x10"])
        r=stats.spearmanr(g.z30,g.x10)
        out[f"r60 band {nm}"]=pd.Series({"n":len(g),"rho":r[0],"p":r[1]})
    g=D.dropna(subset=["x1"])
    out["weekday x1 by year (t)"]=g.groupby(["yr","wd"])["x1"].mean().unstack()*100
    return out
