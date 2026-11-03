"""Regenera data/*.csv a partir dos *_pt.csv, adicionando os prefixos de papel
que o Orange lê no cabeçalho (C#=contínuo, D#=discreto, c=classe/alvo, m=meta, S#=string)."""
import pandas as pd, pathlib
here=pathlib.Path(__file__).parent; out=here.parent/'data'; out.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(here/'insurance_pt.csv'); d.columns=['C#idade','D#sexo','C#imc','C#filhos','D#fumante','D#regiao','cC#custo_anual']; d.to_csv(out/'insurance.csv',index=False)
g=pd.read_csv(here/'german_credit_pt.csv'); g.columns=['cD#risco' if c=='risco' else ('D#'+c if g[c].dtype==object else 'C#'+c) for c in g.columns]; g.to_csv(out/'german_credit.csv',index=False)
c=pd.read_csv(here/'cartao_pt.csv'); c.columns=['mS#cliente']+['C#'+x for x in c.columns[1:]]; c.to_csv(out/'cartao.csv',index=False)
print('ok')
