import numpy as np, pandas as pd, warnings; warnings.filterwarnings('ignore')
from Orange.data import Table, Domain
from Orange.evaluation import CrossValidation
def with_target(t,name,metas=()):
    attrs=[a for a in t.domain.variables if a.name!=name and a.name not in metas]
    ms=[a for a in t.domain.variables if a.name in metas]+list(t.domain.metas)
    return t.transform(Domain(attrs,t.domain[name],ms))
def reg_scores(res):
    y=np.asarray(res.actual).ravel(); out=[]
    for p in res.predicted:
        p=np.asarray(p).ravel(); e=p-y
        out.append(dict(rmse=np.sqrt((e**2).mean()), mae=np.abs(e).mean(), r2=1-(e**2).sum()/((y-y.mean())**2).sum()))
    return out
def cv(d,learners,k=10,seed=42): return CrossValidation(k=k,random_state=seed,stratified=True)(d,learners)
