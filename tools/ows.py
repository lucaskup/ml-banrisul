import json, html
REG=json.load(open(__import__("pathlib").Path(__file__).parent/"reg.json"))
BASE='https://lucaskup.github.io/ml-banrisul/data/'
def scheme(title,desc,nodes,links,notes,props):
    """nodes: list of (key,name,x,y,title?) ; links: (src_key,src_channel,dst_key,dst_channel) ; notes: (x,y,w,h,text)"""
    idx={k:i for i,(k,*_) in enumerate(nodes)}
    xs=['<?xml version=\'1.0\' encoding=\'utf-8\'?>',f'<scheme version="2.0" title="{html.escape(title)}" description="{html.escape(desc)}">','<nodes>']
    for k,name,x,y,*rest in nodes:
        q=REG[name][0]; t=rest[0] if rest else name
        xs.append(f'<node id="{idx[k]}" name="{html.escape(name)}" qualified_name="{q}" project_name="Orange3" version="" title="{html.escape(t)}" position="({x}, {y})" />')
    xs.append('</nodes><links>')
    for i,(s,sc,d,dc) in enumerate(links):
        sname=nodes[idx[s]][1]; dname=nodes[idx[d]][1]
        sid=dict(REG[sname][3])[sc]; did=dict(REG[dname][2])[dc]
        xs.append(f'<link id="{i}" source_node_id="{idx[s]}" sink_node_id="{idx[d]}" source_channel="{sc}" sink_channel="{dc}" enabled="true" source_channel_id="{sid}" sink_channel_id="{did}" />')
    xs.append('</links><annotations>')
    for i,(x,y,w,h,text) in enumerate(notes):
        xs.append(f'<text id="{i}" type="text/plain" rect="({x}, {y}, {w}, {h})" font-family="Helvetica" font-size="13">{html.escape(text)}</text>')
    xs.append('</annotations><thumbnail /><node_properties>')
    for k,p in props.items():
        xs.append(f'<properties node_id="{idx[k]}" format="literal">{html.escape(repr(p))}</properties>')
    xs.append('</node_properties></scheme>')
    return '\n'.join(xs)
def fileprops(fname): return {'source':1,'recent_urls':[BASE+fname],'url':BASE+fname,'sheet_names':{},'controlAreaVisible':True,'__version__':1}

def p1(full):
    nodes=[('file','File',100,250,'insurance.csv'),('tab','Data Table',350,100),('fs','Feature Statistics',350,250),('sp','Scatter Plot',350,400),('dist','Distributions',350,550),
           ('lin','Linear Regression',650,150),('knn','kNN',650,300),('pre','Preprocess',650,450,'Preprocess (normalizar)'),('ts','Test and Score',900,220),('pred','Predictions',900,400)]
    links=[('file','Data','tab','Data'),('file','Data','fs','Data'),('file','Data','sp','Data'),('file','Data','dist','Data')]
    if full: links+=[('file','Data','ts','Data'),('lin','Learner','ts','Learner'),('knn','Learner','ts','Learner'),('file','Data','lin','Data'),('lin','Model','pred','Predictors'),('file','Data','pred','Data'),('pre','Preprocessor','knn','Preprocessor')]
    notes=[(80,40,480,40,'Prática 1 – Regressão: quanto custa o seguro desta pessoa?\nTarget: custo_anual (US$/ano). Dados: 1.338 segurados.'),
           (620,40,420,90,'Passo A: ligue File → Test and Score (Data), e os dois modelos → Test and Score (Learner).\nPasso B: ligue File → Linear Regression → Predictions, e File → Predictions (Data).\nPasso C (quebra): Preprocess → kNN (Preprocessor), com Normalize Features marcado.'),
           (80,640,500,40,'Alvo: ficar com RMSE abaixo de 6.500 em validação cruzada (10 folds).')]
    props={'file':fileprops('insurance.csv'),'ts':{'n_folds':2,'resampling':0,'controlAreaVisible':True,'__version__':3},'knn':{'n_neighbors':5,'metric_index':0,'weight_index':0,'controlAreaVisible':True,'__version__':1}}
    # n_folds index: Orange NFolds=[2,3,5,10,20] -> index 3 = 10
    props['ts']['n_folds']=3
    return scheme('P1 – Regressão (seguro)','Custo anual de seguro saúde: regressão linear e kNN',nodes,links,notes,props)

def p2(full):
    nodes=[('file','File',100,250,'german_credit.csv'),('tab','Data Table',350,100),('dist','Distributions',350,250),('rank','Rank',350,400),
           ('log','Logistic Regression',650,150),('knn','kNN',650,300),('pre','Preprocess',650,450,'Preprocess (normalizar)'),('ts','Test and Score',900,220),('cm','Confusion Matrix',1150,220),('pred','Predictions',900,420)]
    links=[('file','Data','tab','Data'),('file','Data','dist','Data'),('file','Data','rank','Data')]
    if full: links+=[('file','Data','ts','Data'),('log','Learner','ts','Learner'),('knn','Learner','ts','Learner'),('ts','Evaluation Results','cm','Evaluation Results'),('pre','Preprocessor','knn','Preprocessor'),('file','Data','log','Data'),('log','Model','pred','Predictors'),('file','Data','pred','Data')]
    notes=[(80,40,520,40,'Prática 2 – Classificação: aprovar ou negar o crédito?\nTarget: risco (bom/mau). 1.000 solicitantes, 30 % maus pagadores.'),
           (620,40,460,90,'Passo A: File → Test and Score (Data); Logistic Regression e kNN → Test and Score (Learner).\nPasso B: Test and Score → Confusion Matrix.\nPasso C: Preprocess (Normalize Features) → kNN. Passo D: File → Logistic Regression → Predictions.'),
           (80,520,520,60,'Custo: cada mau aprovado custa 5; cada bom negado custa 1.\nCusto do modelo = 5 × (maus aprovados) + 1 × (bons negados). Qual modelo custa menos?')]
    props={'file':fileprops('german_credit.csv'),'ts':{'n_folds':3,'resampling':0,'controlAreaVisible':True,'__version__':3},'knn':{'n_neighbors':5,'metric_index':0,'weight_index':0,'controlAreaVisible':True,'__version__':1}}
    return scheme('P2 – Classificação (crédito)','Risco de crédito: regressão logística e kNN',nodes,links,notes,props)

def p3(full):
    nodes=[('file','File',100,250,'cartao.csv'),('tab','Data Table',350,100),('fs','Feature Statistics',350,250),('km','k-Means',650,250),('sil','Silhouette Plot',900,120),('sp','Scatter Plot',900,250),('box','Box Plot',900,380),('pca','PCA',650,450),('sp2','Scatter Plot',900,520,'Scatter Plot (PCA)')]
    links=[('file','Data','tab','Data'),('file','Data','fs','Data')]
    if full: links+=[('file','Data','km','Data'),('km','Data','sil','Data'),('km','Data','sp','Data'),('km','Data','box','Data'),('km','Data','pca','Data'),('pca','Transformed Data','sp2','Data')]
    notes=[(80,40,520,40,'Prática 3 – Agrupamento: quem são os clientes de cartão?\n8.950 clientes, 17 variáveis de uso (sem rótulo).'),
           (620,40,460,90,'Passo A: File → k-Means (Data); em k-Means, marque "From 2 to 10" e veja a silhueta por k.\nPasso B: k-Means → Silhouette Plot, Scatter Plot e Box Plot (agrupe por Cluster).\nPasso C (quebra): desmarque "Normalize columns" no k-Means e refaça.'),
           (80,620,520,40,'Entregável: um nome e uma ação comercial para cada grupo.')]
    props={'file':fileprops('cartao.csv'),'km':{'k':3,'k_from':2,'k_to':10,'optimize_k':True,'normalize':True,'max_iterations':300,'n_init':10,'smart_init':0,'controlAreaVisible':True,'__version__':2}}
    return scheme('P3 – Agrupamento (cartão)','Segmentação de clientes de cartão com k-Means',nodes,links,notes,props)

for name,fn in [('p1_regressao',p1),('p2_classificacao',p2),('p3_agrupamento',p3)]:
    out=__import__("pathlib").Path(__file__).parent.parent/"orange"; out.mkdir(parents=True,exist_ok=True)
    open(out/f'{name}_inicio.ows','w').write(fn(False))
    open(out/f'{name}_completo.ows','w').write(fn(True))
print('ok')
