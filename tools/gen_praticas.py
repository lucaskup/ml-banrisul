"""Gera as três páginas auto-guiadas das práticas no Orange (p1-regressao.html, p2-classificacao.html,
p3-agrupamento.html). Os números das caixas "Confira" vêm de docs/guia_instrutor.md; não os altere
sem reproduzir no Orange."""
import pathlib
HERE = pathlib.Path(__file__).parent
CSS = open(HERE / 'base.css').read() + """
.wrap{position:relative;max-width:900px}
header{padding-right:56px}
.steps{color:var(--ink-2);font-size:.9rem;margin-bottom:6px}
.theme{position:absolute;top:20px;right:16px;width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--ink);cursor:pointer;padding:0}
.theme:hover{border-color:var(--you)}
.theme svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.theme .sun{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .theme .sun{display:block}:root:not([data-theme="light"]) .theme .moon{display:none}}
:root[data-theme="dark"] .theme .sun{display:block}
:root[data-theme="dark"] .theme .moon{display:none}
.task{background:var(--panel);border-left:4px solid var(--you);border-radius:0 10px 10px 0;padding:10px 14px;margin:14px 0 4px;max-width:78ch}
.task p{margin:0}.task p+p{margin-top:6px;color:var(--ink-2)}
h2.sec{font-size:1.3rem;font-weight:700;margin:30px 0 4px;padding-top:10px;border-top:1px solid var(--line)}
h2.sec .min{font-weight:400;color:var(--ink-2);font-size:.95rem;margin-left:8px}
h3{font-size:1.05rem;margin:18px 0 6px}
p{max-width:78ch}
ol.todo{list-style:none;padding:0;margin:8px 0;counter-reset:s}
ol.todo li{position:relative;padding:8px 10px 8px 46px;margin:0 0 6px;background:var(--panel);border:1px solid var(--line);border-radius:10px;max-width:78ch}
ol.todo li::before{counter-increment:s;content:counter(s);position:absolute;left:12px;top:8px;width:24px;height:24px;border-radius:50%;background:var(--you);color:#fff;font-weight:700;font-size:.85rem;display:flex;align-items:center;justify-content:center}
ol.todo li label{display:block;cursor:pointer}
ol.todo li input{accent-color:var(--you);margin:0 8px 0 0;vertical-align:-2px}
ol.todo li.done label{color:var(--ink-2);text-decoration:line-through}
.obs{border-left:4px solid var(--best);background:var(--panel);border-radius:0 10px 10px 0;padding:10px 14px;margin:10px 0;max-width:78ch}
.obs p{margin:0}.obs p+p{margin-top:6px}
.obs .lbl,details.check summary .lbl{font-weight:700;color:var(--best)}
details.check{border:1px dashed var(--line);border-radius:10px;padding:8px 14px;margin:10px 0;max-width:78ch;background:var(--panel)}
details.check summary{cursor:pointer;font-weight:500}
details.check summary .lbl{color:var(--you)}
details.check[open] summary{margin-bottom:6px}
details.help{border:1px solid var(--line);border-radius:10px;padding:8px 14px;margin:14px 0;background:var(--panel)}
details.help summary{cursor:pointer;font-weight:700}
details.help ul{padding-left:20px;margin:6px 0}
details.help li{margin:4px 0;max-width:78ch}
table{border-collapse:collapse;margin:8px 0;font-size:.93rem}
th,td{border:1px solid var(--line);padding:5px 10px;text-align:left;vertical-align:top}
th{background:var(--panel)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
b.w{font-weight:700;color:var(--you)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.92em;background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:0 4px}
kbd{font:inherit;font-size:.9em;border:1px solid var(--line);border-bottom-width:2px;border-radius:5px;padding:0 5px;background:var(--panel)}
.links a{color:var(--you)}
.nav{display:flex;justify-content:space-between;gap:12px;margin-top:32px;padding-top:12px;border-top:1px solid var(--line);font-size:.95rem}
.nav a{color:var(--you)}
.blank{display:inline-block;min-width:4em;border-bottom:1px solid var(--ink-2);vertical-align:bottom}
"""
BTN = '<button class="theme" id="theme" type="button" aria-label="Alternar modo claro e escuro" title="Modo claro / escuro"><svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>'
JS = """
(function(){const b=document.getElementById('theme');if(!b)return;
const dark=()=>{const t=document.documentElement.dataset.theme;return t?t==='dark':matchMedia('(prefers-color-scheme:dark)').matches;};
b.addEventListener('click',()=>{const next=dark()?'light':'dark';document.documentElement.dataset.theme=next;
  try{localStorage.setItem('theme',next)}catch(e){}});})();
(function(){const key='todo:'+location.pathname;let st={};try{st=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}
document.querySelectorAll('ol.todo li').forEach((li,i)=>{const cb=li.querySelector('input');if(!cb)return;const id=li.closest('section').id+':'+i;
  if(st[id]){cb.checked=true;li.classList.add('done');}
  cb.addEventListener('change',()=>{li.classList.toggle('done',cb.checked);st[id]=cb.checked;try{localStorage.setItem(key,JSON.stringify(st))}catch(e){}});});
const h=document.getElementById(location.hash.slice(1));if(h){const d=h.querySelector('details');if(d){d.open=true;}}
const r=document.getElementById('reset');if(r)r.addEventListener('click',()=>{st={};try{localStorage.removeItem(key)}catch(e){}
  document.querySelectorAll('ol.todo li').forEach(li=>{const cb=li.querySelector('input');if(cb)cb.checked=false;li.classList.remove('done');});});})();
"""

HELP = """
<details class="help" open>
<summary>Como mexer no Orange</summary>
<ul>
<li><b>Widgets</b> são as caixas na tela. Duplo clique abre a janela do widget; fechar a janela não apaga o widget.</li>
<li><b>Ligar dois widgets:</b> arraste a partir da borda direita de um (a saída) até a borda esquerda do outro (a entrada). Quando houver mais de um canal possível, o Orange abre uma janela para você escolher qual saída vai em qual entrada.</li>
<li><b>Desfazer uma ligação:</b> clique na linha e aperte <kbd>Delete</kbd>. Ligar uma nova fonte a uma entrada que só aceita uma ligação substitui a anterior.</li>
<li><b>Adicionar um widget:</b> na barra da esquerda, abra a categoria (Data, Visualize, Model, Evaluate, Unsupervised) e clique no widget, ou arraste-o para a tela.</li>
<li><b>Os resultados atualizam sozinhos</b> quando uma ligação muda. Alguns widgets têm o botão <b>Apply</b> ou a caixa <b>Send Automatically</b>; se um número não mudou, confira se o botão foi clicado.</li>
<li><b>Linhas tracejadas</b> entre widgets significam que nada passou ainda por aquela ligação (o widget de origem ainda não produziu saída).</li>
<li><b>Papéis das colunas:</b> no widget <b class="w">File</b>, a tabela mostra cada coluna como <i>feature</i>, <i>target</i> ou <i>meta</i>. Os arquivos destas práticas já chegam com o papel certo; não é preciso alterar.</li>
</ul>
</details>"""

ORANGE_VER = '3.40.0'
ORANGE_ZIP = f'https://download.biolab.si/download/files/Orange3-{ORANGE_VER}.zip'
INSTALL = f"""
<section id="orange"><details class="help">
<summary>Ainda não tem o Orange? Versão portátil, sem instalar</summary>
<p>A versão portátil do Orange roda no Windows a partir de uma pasta comum, sem instalador e sem senha de administrador. São 500 MB para baixar e 1,4 GB depois de descompactado, em cerca de 24 mil arquivos. No macOS use o instalador <code>.dmg</code> da <a class="links" href="https://orangedatamining.com/download/">página de download</a>.</p>
<ol class="todo">
<li><label><input type="checkbox">Baixe o arquivo <a class="links" href="{ORANGE_ZIP}">Orange3-{ORANGE_VER}.zip</a>. É o mesmo arquivo da opção <b>Portable Orange</b>, aba Windows, em orangedatamining.com/download.</label></li>
<li><label><input type="checkbox">Mova o zip para uma pasta local em que você possa gravar, como <code>Documentos</code> ou a Área de Trabalho. Evite pastas de rede e pastas sincronizadas com o OneDrive: a sincronização de milhares de arquivos pequenos deixa tudo lento.</label></li>
<li><label><input type="checkbox">Clique com o botão direito no zip, escolha <b>Extrair Tudo…</b> e depois <b>Extrair</b>. A descompactação leva alguns minutos. 7-Zip ou WinRAR também servem.</label></li>
<li><label><input type="checkbox">Abra a pasta extraída (<code>Orange3-{ORANGE_VER}</code>). Dentro há a pasta <code>Orange</code> e o atalho <b>Orange</b>. Dê duplo clique no atalho. Uma janela preta de terminal pisca e some; isso é esperado.</label></li>
<li><label><input type="checkbox">Espere: a primeira abertura leva de um a dois minutos, porque o Windows lê todos os arquivos pela primeira vez. As seguintes são mais rápidas. Se aparecer um aviso do SmartScreen, clique em <b>Mais informações</b> e em <b>Executar assim mesmo</b>.</label></li>
<li><label><input type="checkbox">Confira: a tela do Orange abre com a barra de widgets à esquerda (Data, Visualize, Model…). Em <b>Help → About</b> aparece a versão {ORANGE_VER}.</label></li>
</ol>
<p>Se o atalho não abrir nada (algumas máquinas corporativas bloqueiam o <code>cmd.exe</code> que ele usa), entre na pasta <code>Orange</code>, clique na barra de endereço do Explorador de Arquivos, digite <code>pythonw.exe -m Orange.canvas</code> e aperte <kbd>Enter</kbd>.</p>
<p>A versão portátil não associa a extensão <code>.ows</code>: duplo clique no arquivo do workflow não abre o Orange. Use <b>File → Open</b> dentro do Orange ou arraste o arquivo para a tela.</p>
</details></section>"""

def todo(items):
    return '<ol class="todo">' + ''.join(f'<li><label><input type="checkbox">{t}</label></li>' for t in items) + '</ol>'
def obs(*ps):
    return '<div class="obs"><p><span class="lbl">Observe.</span> ' + ps[0] + '</p>' + ''.join(f'<p>{p}</p>' for p in ps[1:]) + '</div>'
def check(summary, body):
    return f'<details class="check"><summary><span class="lbl">Confira:</span> {summary}</summary>{body}</details>'
def sec(id_, title, minutes, body):
    return f'<section id="{id_}"><h2 class="sec">{title}<span class="min">{minutes}</span></h2>{body}</section>'
def tbl(head, rows, num_from=1):
    h = ''.join(f'<th{" class=n" if i >= num_from else ""}>{c}</th>' for i, c in enumerate(head))
    r = ''.join('<tr>' + ''.join(f'<td{" class=n" if i >= num_from else ""}>{c}</td>' for i, c in enumerate(row)) + '</tr>' for row in rows)
    return f'<table><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'
def before(n, base, csv, extra=''):
    return f"""
<h2 class="sec" style="border-top:0;margin-top:20px">Antes de começar<span class="min">5 min</span></h2>{INSTALL}
<p class="links">Baixe o <a href="orange/{base}_inicio.ows" download>workflow de início</a> e abra no Orange (<b>File → Open</b>, ou arraste o arquivo para a tela). Os dados são carregados pela internet; se a rede bloquear, baixe o <a href="data/{csv}">CSV</a>, abra o widget <b class="w">File</b>, escolha a aba de arquivo local e aponte para ele.</p>
<p>A parte da esquerda do workflow já está ligada (carga e exploração). Os widgets da direita estão soltos: ligar e configurar cada um deles é o trabalho desta prática. Se travar em algum ponto, o <a class="links" href="orange/{base}_completo.ows" download>workflow completo</a> tem tudo ligado.</p>{extra}
{HELP}"""

def page(fn, n, title, intro, task, body, prev, nxt):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Orange {n}. {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script>try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<div class="wrap">
{BTN}
<header>
  <div class="steps">Orange · prática {n} de 3 · 60 min, em duplas</div>
  <h1>{title}</h1>
  <p>{intro}</p>
</header>
<div class="task">{task}</div>
{body}
<p class="note">Marcações das etapas ficam salvas neste navegador. <button class="btn" id="reset" type="button" style="font-size:.85rem;padding:3px 8px">Limpar marcações</button></p>
<nav class="nav"><span>{prev}</span><span>{nxt}</span></nav>
</div>
<script>{JS}</script>
</body>
</html>"""

# ---------------------------------------------------------------- P1
p1 = before(1, 'p1_regressao', 'insurance.csv') + sec('explorar', '1. Explorar os dados', '5–15 min',
 """<p>Os quatro widgets de exploração já recebem os dados do <b class="w">File</b>. Abra cada um e responda às perguntas.</p>""" +
 todo([
  'Abra o <b class="w">Data Table</b>. Quantas linhas e quantas colunas há? Qual coluna está marcada como alvo (<i>target</i>)?',
  'Abra o <b class="w">Feature Statistics</b>. Anote o mínimo e o máximo de <code>idade</code>, <code>imc</code> e <code>custo_anual</code>. Compare a média e a mediana do custo.',
  'Abra o <b class="w">Distributions</b> e escolha <code>custo_anual</code>. Em <b>Split by</b>, escolha <code>fumante</code>.',
  'Abra o <b class="w">Scatter Plot</b>. Coloque <code>idade</code> no eixo x, <code>custo_anual</code> no eixo y e <code>fumante</code> em <b>Color</b>.',
  'Troque o eixo x para <code>imc</code>. Olhe só os pontos de fumantes: o que acontece acima de IMC 30?',
  'Antes de treinar qualquer modelo, aposte: qual coluna mais pesa no custo? Anote a aposta da dupla.',
 ]) +
 obs('O custo tem média bem acima da mediana: poucas pessoas com custo muito alto puxam a média. No gráfico de idade há três faixas quase paralelas; a de cima é só de fumantes.',
     'Repare nas escalas: idade vai de 18 a 64, IMC de 16 a 53, filhos de 0 a 5, e fumante é sim ou não. O kNN mede distância com essas escalas do jeito que estão.') +
 check('o que você deve ter visto', '<p>1.338 linhas e 7 colunas; o alvo é <code>custo_anual</code>. Idade 18–64, IMC 16–53, custo de 1.122 a 63.770 dólares (média 13.270, mediana 9.382). Entre fumantes, acima de IMC 30 o custo mais ou menos dobra.</p>')
) + sec('construir', '2. Construir e avaliar dois modelos', '15–40 min',
 """<p>Agora os dois modelos entram na validação cruzada. O <b class="w">Test and Score</b> treina cada modelo 10 vezes, cada vez deixando 10 % dos dados de fora para medir o erro.</p>""" +
 todo([
  'Ligue <b class="w">File</b> → <b class="w">Test and Score</b>. Na janela que abrir, confirme a ligação <b>Data → Data</b>.',
  'Ligue <b class="w">Linear Regression</b> → <b class="w">Test and Score</b> (canal <b>Learner</b>). Faça o mesmo com <b class="w">kNN</b>.',
  'Abra o <b class="w">Test and Score</b>. Confira que está em <b>Cross validation</b> com <b>Number of folds: 10</b>. Anote RMSE, MAE e R² de cada modelo.',
  'Abra o <b class="w">kNN</b> e confira que <b>Number of neighbors</b> é 5. Ainda não mude nada.',
  'Ligue <b class="w">File</b> → <b class="w">Linear Regression</b> (Data). Depois ligue <b class="w">Linear Regression</b> → <b class="w">Predictions</b> e escolha <b>Model → Predictors</b>. Por fim, <b class="w">File</b> → <b class="w">Predictions</b> (Data).',
  'Adicione um <b class="w">Data Table</b> novo (categoria Data) e ligue <b class="w">Linear Regression</b> → esse <b class="w">Data Table</b>, escolhendo a saída <b>Coefficients</b>. Anote o intercepto e os coeficientes de <code>idade</code>, <code>imc</code>, <code>filhos</code> e <code>fumante</code>.',
  'Com os coeficientes, calcule à mão o custo previsto para uma pessoa de 45 anos, homem, IMC 30, 2 filhos, fumante, região sudeste. Some: intercepto + idade × 45 + IMC × 30 + filhos × 2 + o coeficiente de <code>sexo = homem</code> + o de <code>regiao = sudeste</code> + o de <code>fumante = sim</code>. Cada coluna categórica tem um coeficiente por nível; entra só o nível da pessoa. Depois calcule a mesma pessoa não fumante, trocando o último termo pelo coeficiente de <code>fumante = não</code>.',
 ]) +
 obs('RMSE e MAE estão em dólares por ano; R² é a fração da variação do custo que o modelo explica. O kNN com k = 5 fica bem atrás da regressão linear. Guarde esse número para comparar com o kNN normalizado.',
     'O Orange divide o efeito de uma coluna binária entre os dois níveis: fumante = sim ganha um coeficiente positivo e fumante = não o mesmo valor negativo. A diferença entre fumar e não fumar é a soma dos dois.') +
 check('números esperados (10 folds; pequenas variações são normais)',
   tbl(['Modelo', 'RMSE (US$)', 'MAE (US$)', 'R²'], [['Regressão linear', '6.084', '4.205', '0,747'], ['kNN, k = 5, sem normalizar', '10.266', '6.735', '0,281']]) +
   '<p>Coeficientes: intercepto −667; idade +257 por ano; IMC +339 por ponto; filhos +476 por filho; fumante sim +11.924 e não −11.924 (diferença de 23.850); sexo e região abaixo de 600 em módulo. A pessoa do exercício custa cerca de US$ 33.400 fumante e US$ 9.600 não fumante.</p>')
) + sec('quebrar', '3. Quebrar o modelo: a escala das colunas', '40–50 min',
 """<p>O kNN decide pela distância entre pessoas. Sem tratamento, 10 anos de idade valem 10 unidades de distância e fumar vale 1. O widget <b class="w">Preprocess</b> já vem configurado com <b>Normalize Features</b> no intervalo [0, 1]: todas as colunas passam a pesar igual.</p>""" +
 todo([
  'Abra o <b class="w">Preprocess</b> só para ver o que ele faz. Não altere.',
  'Ligue <b class="w">Preprocess</b> → <b class="w">kNN</b>. Na janela, escolha <b>Preprocessor → Preprocessor</b>.',
  'Volte ao <b class="w">Test and Score</b> e anote de novo RMSE, MAE e R² do kNN.',
  'Abra o <b class="w">kNN</b>, mude <b>Number of neighbors</b> para 15 e veja o que acontece com o erro. Depois volte para 5.',
  'Se sobrar tempo: adicione um <b class="w">Select Columns</b> (categoria Data). Ligue <b class="w">File</b> → <b class="w">Select Columns</b> e <b class="w">Select Columns</b> → <b class="w">Test and Score</b> (Data); a ligação nova substitui a que vinha direto do File. No Select Columns, mova <code>fumante</code> para <b>Ignored</b> e veja o R² da regressão linear. Depois faça o contrário, deixando só <code>fumante</code> como feature.',
 ]) +
 obs('Só a normalização muda o kNN de pior para melhor que a regressão linear. Nenhum dado novo entrou; mudou a régua com que o modelo mede distância.',
     'A regressão linear nem percebe a normalização: multiplicar uma coluna por uma constante só muda o coeficiente dela.') +
 check('números esperados',
   tbl(['Modelo', 'RMSE (US$)', 'MAE (US$)', 'R²'], [['kNN, k = 5, normalizado 0–1', '5.777', '3.541', '0,772'], ['kNN, k = 15, normalizado', '6.204', '3.830', '0,737'], ['Linear sem a coluna fumante', '11.375', '—', '0,117'], ['Linear só com a coluna fumante', '7.482', '—', '0,618']]))
) + sec('fechar', '4. Anotar e discutir', '50–60 min',
 """<p>Cada dupla diz em voz alta o RMSE do melhor modelo. Depois, discutam:</p>
<ul>
<li>Uma única coluna binária (fumante) explica 62 % da variação do custo. O que isso diz sobre coletar mais linhas versus coletar a coluna certa?</li>
<li>Um RMSE de 6.000 dólares é bom? Compare com a mediana do custo (9.400) e com o desvio padrão (12.100).</li>
<li>O kNN erra menos, mas não produz coeficiente. Para um comitê de precificação, ou para um regulador, qual dos dois modelos você defenderia?</li>
<li>A reta superestima jovens não fumantes e subestima fumantes obesos. Onde uma seguradora perderia dinheiro com esse erro sistemático?</li>
</ul>""")
P1 = page('p1-regressao.html', 1, 'Regressão: quanto custa o seguro desta pessoa?',
 'Uma corretora precisa cotar o prêmio de saúde de uma pessoa nova. O arquivo tem 1.338 segurados com idade, sexo, IMC, filhos, fumante, região e o custo anual em dólares. Você vai medir quanto cada característica pesa e comparar dois modelos: regressão linear e k vizinhos mais próximos (kNN).',
 '<p>Ao final, a dupla entrega: o RMSE do melhor modelo em validação cruzada, os coeficientes da regressão linear e o custo previsto para a pessoa do exercício, fumante e não fumante.</p><p>Alvo: ficar com RMSE abaixo de 6.500.</p>',
 p1, '<a href="index.html">← Índice</a>', '<a href="p2-classificacao.html">Prática 2: classificação →</a>')

# ---------------------------------------------------------------- P2
p2 = before(2, 'p2_classificacao', 'german_credit.csv') + sec('explorar', '1. Explorar os dados', '5–15 min',
 """<p>O alvo é <code>risco</code>: bom ou mau pagador. Junto com o arquivo vem uma matriz de custo: <b>aprovar um mau pagador custa 5; negar um bom pagador custa 1</b>. Toda a prática gira em torno desse custo.</p>""" +
 todo([
  'Abra o <b class="w">Distributions</b> e escolha <code>risco</code>. Quantos bons e quantos maus? Se um modelo aprovasse todo mundo, qual seria a acurácia dele? Escreva esse número num canto da folha.',
  'Abra o <b class="w">Rank</b>. Quais quatro colunas aparecem no topo?',
  'No <b class="w">Distributions</b>, escolha <code>conta_corrente</code> e, em <b>Split by</b>, <code>risco</code>. Qual grupo tem a menor fração de maus pagadores?',
  'Abra o <b class="w">Data Table</b> e procure a coluna <code>estado_civil_sexo</code>. Ela deveria entrar num modelo de crédito? Anote a opinião da dupla para a etapa 4.',
 ]) +
 obs('Quem não tem conta corrente no banco é o grupo mais seguro deste conjunto. Isso contraria a intuição e rende uma pergunta: quem são essas pessoas?',
     'O número que você escreveu no canto (a acurácia de aprovar todo mundo) é a referência: qualquer modelo com acurácia menor que isso está perdendo para não fazer nada.') +
 check('o que você deve ter visto', '<p>700 bons e 300 maus; aprovar todo mundo acerta 70 %. No Rank, <code>conta_corrente</code>, <code>prazo_meses</code>, <code>historico_credito</code> e <code>poupanca</code> lideram.</p>')
) + sec('construir', '2. Construir, avaliar e calcular o custo', '15–40 min',
 """<p>Dois classificadores entram na validação cruzada: regressão logística e kNN. A matriz de confusão mostra os dois tipos de erro, e é dela que sai o custo.</p>""" +
 todo([
  'Ligue <b class="w">File</b> → <b class="w">Test and Score</b> (Data). Ligue <b class="w">Logistic Regression</b> e <b class="w">kNN</b> → <b class="w">Test and Score</b> (Learner).',
  'Abra o <b class="w">Test and Score</b>: <b>Cross validation</b>, 10 folds. Anote a acurácia (CA) e a AUC de cada modelo. A AUC é a chance de o modelo dar probabilidade de mau maior a um mau pagador do que a um bom, os dois sorteados ao acaso: 0,5 é sorteio, 1 é perfeito. Compare a CA com o número do canto da folha.',
  'Ligue <b class="w">Test and Score</b> → <b class="w">Confusion Matrix</b> (Evaluation Results).',
  'Abra o <b class="w">Confusion Matrix</b>. Em <b>Show</b>, escolha <b>Number of instances</b>. Selecione um modelo por vez na lista da esquerda. As linhas são a classe real e as colunas, a classe prevista.',
  'Para cada modelo, anote: maus previstos como bons (linha <code>mau</code>, coluna <code>bom</code>) e bons previstos como maus (linha <code>bom</code>, coluna <code>mau</code>).',
  'Calcule o custo de cada modelo: <b>5 × (maus aprovados) + 1 × (bons negados)</b>. Calcule também o custo de aprovar todo mundo.',
 ]) +
 obs('O kNN sem normalização perde para "aprovar todo mundo" em acurácia. A regressão logística ganha em acurácia, em AUC e em custo.',
     'Os dois erros não valem o mesmo. Um modelo com acurácia maior pode custar mais, se os erros dele forem do tipo caro.') +
 check('números esperados (10 folds; variações de 1 a 2 pontos são normais)',
   tbl(['Modelo', 'Acurácia', 'AUC', 'Maus aprovados', 'Bons negados', 'Custo'], [
    ['Aprovar todo mundo', '0,700', '0,500', '300', '0', '1.500'],
    ['Regressão logística', '0,749', '0,785', '158', '93', '883'],
    ['kNN, k = 5, sem normalizar', '0,647', '0,563', '230', '123', '1.273']]))
) + sec('quebrar', '3. Quebrar o modelo: quem são os erros, e onde fica o corte', '40–50 min',
 """<p>Um classificador dá uma probabilidade, e alguém escolhe o corte que a transforma em "bom" ou "mau". O padrão é 0,5. Com erros de custo diferente, o padrão raramente é a melhor escolha.</p>""" +
 todo([
  'No <b class="w">Confusion Matrix</b>, com a regressão logística selecionada, clique na célula "mau real, previsto bom". Adicione um <b class="w">Data Table</b> e ligue <b class="w">Confusion Matrix</b> → <b class="w">Data Table</b> (Selected Data). Esses são os clientes que o modelo aprovaria e que deram prejuízo. Olhe <code>conta_corrente</code> e <code>prazo_meses</code> nesses clientes: o que eles têm em comum com os bons pagadores?',
  'Ligue <b class="w">File</b> → <b class="w">Logistic Regression</b> (Data). Depois <b class="w">Logistic Regression</b> → <b class="w">Predictions</b> (Model → Predictors) e <b class="w">File</b> → <b class="w">Predictions</b> (Data).',
  'Abra o <b class="w">Predictions</b>. No topo, em <b>Show probabilities for</b>, escolha <code>mau</code>: a coluna do modelo passa a mostrar só a probabilidade de mau. Clique no cabeçalho dessa coluna para ordenar; se vier do menor para o maior, clique de novo. Desça até a probabilidade cruzar 0,30: o número da linha, na margem esquerda, é quantos clientes seriam negados com esse corte.',
  'Repita para 0,20. Mais negados, menos maus aprovados: o custo cai ou sobe? Até onde vale a pena baixar o corte?',
  'Ligue <b class="w">Preprocess</b> → <b class="w">kNN</b> (Preprocessor). O Preprocess já normaliza as colunas para [0, 1]. Veja no <b class="w">Test and Score</b> o que muda na acurácia do kNN.',
 ]) +
 obs('O <b class="w">Predictions</b> aqui usa o modelo treinado em todos os 1.000 clientes e avalia nos mesmos clientes, então os números saem um pouco melhores que na validação cruzada. A direção é a mesma: baixar o corte derruba a acurácia e reduz o custo, até certo ponto.',
     'Na validação cruzada, o custo mínimo fica perto do corte 0,2, onde o banco nega mais da metade dos pedidos.') +
 check('números esperados',
   '<p>Validação cruzada (10 folds), regressão logística, negar quando P(mau) ≥ corte:</p>' +
   tbl(['Corte', 'Acurácia', 'Negados', 'Maus aprovados', 'Bons negados', 'Custo'], [
    ['0,50', '0,749', '235', '158', '93', '883'], ['0,40', '0,730', '326', '122', '148', '758'], ['0,30', '0,709', '429', '81', '210', '615'], ['0,20', '0,663', '551', '43', '294', '509'], ['0,15', '0,606', '628', '33', '361', '526']]) +
   '<p>Maus aprovados: cerca de 30 % não têm conta corrente (entre todos os maus são 15 %; entre os bons, 50 %) e o prazo mediano é 18 meses, igual ao dos bons. O modelo os aprova porque, nas colunas que mais pesam, eles se parecem com bons pagadores.</p><p>No <b class="w">Predictions</b> (treino e teste nos mesmos dados): corte 0,30 nega cerca de 434 e custa cerca de 518; corte 0,20 nega cerca de 565 e custa cerca de 493.</p><p>kNN com Preprocess: acurácia sobe de 0,647 para cerca de 0,729; com k = 15, 0,744.</p>')
) + sec('fechar', '4. Anotar e discutir', '50–60 min',
 """<p>Cada dupla diz em voz alta o custo do melhor modelo que encontrou (modelo e corte). Depois, discutam:</p>
<ul>
<li>Se a acurácia não serve, que número você pediria no relatório de um modelo de crédito?</li>
<li>Os valores 5 e 1 da matriz de custo vieram de onde? Quem no banco saberia os valores reais? O que mudaria se negar um bom cliente custasse 2?</li>
<li><code>estado_civil_sexo</code> está entre as colunas de maior peso. Tirá-la (um <b class="w">Select Columns</b> ligado ao <b class="w">File</b> e, dele, ao <b class="w">Test and Score</b>, com a coluna em <b>Ignored</b>) muda a acurácia em menos de um ponto. Mantê-la expõe o banco a uma decisão de crédito que depende de sexo e estado civil. O que o Banrisul faria?</li>
<li>O conjunto tem 30 anos e é de outro país. O que precisaria ser verdade para o modelo valer para clientes de hoje?</li>
</ul>""")
P2 = page('p2-classificacao.html', 2, 'Classificação: aprovar ou negar o crédito?',
 'A mesa de crédito quer um modelo que diga quem negar. O arquivo tem 1.000 solicitantes de um banco alemão nos anos 1990, com 20 atributos (conta corrente, prazo, valor, histórico, poupança, emprego, idade, moradia) e o resultado: 700 pagaram, 300 não. Você vai comparar regressão logística e kNN, e descobrir por que acurácia engana quando os erros custam diferente.',
 '<p>Ao final, a dupla entrega: a matriz de confusão de cada modelo, o custo de cada um (5 por mau aprovado, 1 por bom negado) e o corte de probabilidade que a dupla escolheria.</p><p>Referência: aprovar todo mundo acerta 70 % e custa 1.500. Qualquer modelo tem que bater isso.</p>',
 p2, '<a href="p1-regressao.html">← Prática 1: regressão</a>', '<a href="p3-agrupamento.html">Prática 3: agrupamento →</a>')

# ---------------------------------------------------------------- P3
p3 = before(3, 'p3_agrupamento', 'cartao.csv') + sec('explorar', '1. Explorar os dados', '5–15 min',
 """<p>Não há coluna alvo: ninguém disse quais são os grupos. A coluna <code>cliente</code> é só identificador e já chega marcada como meta, fora do cálculo.</p>""" +
 todo([
  'Abra o <b class="w">Feature Statistics</b>. Compare a escala de <code>saldo</code>, <code>compras</code> e <code>limite</code> com a das frequências (<code>freq_compras</code>, <code>freq_saque</code>). Veja a coluna de valores faltantes.',
  'Abra o <b class="w">Data Table</b> e passe os olhos em dez clientes. Dá para descrever algum perfil só de olhar?',
  'Ligue <b class="w">File</b> → <b class="w">Scatter Plot</b> por enquanto (a ligação muda quando o k-Means entrar). Coloque <code>compras</code> em x e <code>saque</code> em y.',
  'Pergunta da dupla: uma distância euclidiana entre dois clientes, calculada com todas as colunas do jeito que estão, seria dominada por quais colunas?',
 ]) +
 obs('Saldo vai de 0 a 19 mil; frequências vão de 0 a 1. Sem tratamento, as colunas em dinheiro decidem tudo e as frequências não contam.',
     'No gráfico compras × saque, a maioria dos pontos está colada em um dos eixos: quase ninguém compra muito e saca muito ao mesmo tempo. Há 313 valores faltantes em <code>pagamento_minimo</code> e 1 em <code>limite</code>; o k-Means do Orange preenche com a média, sem avisar.') +
 check('o que você deve ter visto', '<p>8.950 clientes e 17 colunas numéricas. Saldo 0–19.043, compras 0–49.040, limite 50–30.000, frequências 0–1.</p>')
) + sec('construir', '2. Agrupar e dar nome aos grupos', '15–40 min',
 """<p>O k-Means precisa saber quantos grupos procurar. O widget testa vários valores de k e mostra a silhueta de cada um: quanto maior, mais separados os grupos.</p>""" +
 todo([
  'Ligue <b class="w">File</b> → <b class="w">k-Means</b>. Abra o widget: em <b>Number of Clusters</b>, confira <b>From 2 to 10</b>; <b>Normalize columns</b> marcado; <b>Re-runs</b> 10. Espere a tabela de silhuetas aparecer (até um minuto).',
  'Anote a silhueta de cada k. Qual k tem a maior? Clique na linha desse k para selecioná-lo.',
  'Ligue <b class="w">k-Means</b> → <b class="w">Silhouette Plot</b>. Cada barra é um cliente; barras negativas são clientes que ficariam melhor em outro grupo.',
  'Ligue <b class="w">k-Means</b> → <b class="w">Scatter Plot</b> (isso substitui a ligação que vinha do File). Em <b>Color</b>, escolha <code>Cluster</code>. Veja compras × saque, depois saldo × limite e freq_compras × freq_saque.',
  'Ligue <b class="w">k-Means</b> → <b class="w">Box Plot</b>. Em <b>Subgroups</b>, escolha <code>Cluster</code>. Troque a <b>Variable</b> uma por vez: <code>saldo</code>, <code>compras</code>, <code>saque</code>, <code>freq_compras</code>, <code>pct_pagamento_total</code>.',
  'Preencha uma linha por grupo: nome, tamanho, o que o caracteriza, uma ação comercial. Use o <b class="w">Box Plot</b> para a característica e o <b class="w">Silhouette Plot</b> para o tamanho.',
 ]) +
 '<table><thead><tr><th>Grupo</th><th>Nome</th><th>Tamanho</th><th>O que o caracteriza</th><th>Ação comercial</th></tr></thead><tbody>' +
 ''.join(f'<tr><td>{c}</td><td><span class="blank"></span></td><td><span class="blank"></span></td><td><span class="blank" style="min-width:12em"></span></td><td><span class="blank" style="min-width:12em"></span></td></tr>' for c in 'ABC') +
 '</tbody></table>' +
 obs('A silhueta máxima é baixa em termos absolutos (em torno de 0,25): os grupos existem, mas se sobrepõem. Eles servem para segmentar campanhas, desde que ninguém os trate como caixas estanques.',
     'A numeração dos grupos (C1, C2, C3) muda de máquina para máquina. Compare pelos perfis, não pelos números.') +
 check('números esperados (normalizado, k = 3)',
   '<p>Silhueta por k: 2 → 0,21; <b>3 → 0,25</b>; 4 → 0,20; 5 → 0,19; de 6 a 10 entre 0,20 e 0,22.</p>' +
   tbl(['Grupo', 'n', 'Saldo médio', 'Compras', 'Saque', 'Freq. compras', 'Freq. saque', 'Limite', 'Pag. integral', 'Nome sugerido'], [
    ['A', '6.108', '804', '500', '335', '0,46', '0,07', '3.266', '15 %', 'Pouco uso'],
    ['B', '1.261', '2.190', '4.214', '453', '0,95', '0,06', '7.682', '30 %', 'Compradores'],
    ['C', '1.581', '4.003', '387', '3.887', '0,23', '0,45', '6.697', '3 %', 'Sacadores']]) +
   '<p>Com k = 4, os compradores se dividem em frequentes (3.367) e grandes compradores (409, compras médias de 7.700). Também é um resultado defensável para campanha.</p>')
) + sec('quebrar', '3. Quebrar o modelo: a escala de novo, e uma coluna a menos', '40–50 min',
 """<p>O algoritmo só vê as colunas que recebe, na escala em que chegam. Mudar uma das duas coisas produz grupos diferentes.</p>""" +
 todo([
  'No <b class="w">k-Means</b>, mude para <b>Fixed: 3</b> e desmarque <b>Normalize columns</b>. Olhe de novo o <b class="w">Box Plot</b> de <code>saldo</code> e <code>compras</code> e o tamanho dos grupos no <b class="w">Silhouette Plot</b>.',
  'Marque <b>Normalize columns</b> de volta.',
  'Se sobrar tempo: adicione um <b class="w">Select Columns</b> (categoria Data). Ligue <b class="w">File</b> → <b class="w">Select Columns</b> e <b class="w">Select Columns</b> → <b class="w">k-Means</b> (Data); a ligação nova substitui a que vinha direto do File. Mova <code>saque</code> e <code>freq_saque</code> para <b>Ignored</b> e rode de novo com k = 3. Que grupo desapareceu?',
  'Ligue <b class="w">k-Means</b> → <b class="w">PCA</b> e <b class="w">PCA</b> → <b class="w">Scatter Plot (PCA)</b>, escolhendo <b>Transformed Data → Data</b>. No gráfico, PC1 em x, PC2 em y e <code>Cluster</code> em <b>Color</b>.',
 ]) +
 obs('Sem normalizar, os grupos viram pequeno, médio e grande em dinheiro, e o terceiro grupo tem 134 pessoas. O comportamento (compra ou saca) some, porque as colunas de frequência deixam de pesar.',
     'Sem as colunas de saque, o grupo dos sacadores não existe: o algoritmo só encontra o que está nas colunas que recebe.') +
 check('números esperados (sem normalizar, k = 3)',
   '<p>Grupos de 6.514 (saldo 855, compras 603), 2.302 (saldo 3.384, compras 1.586, saque 2.091) e 134 (saldo 4.797, compras 10.471, pagamentos 17.991).</p><p>No PCA com duas componentes, coloridas por grupo, há separação parcial com muita sobreposição.</p>')
) + sec('fechar', '4. Anotar e discutir', '50–60 min',
 """<p>Cada dupla lê o nome que deu a um dos grupos. Os nomes convergem entre as duplas? Depois, discutam:</p>
<ul>
<li>Os sacadores pagam só o mínimo em 97 % dos meses. Isso é um grupo de receita de juros ou um grupo de risco? Quem decide?</li>
<li>Se o produto pediu quatro campanhas e a silhueta prefere três grupos, o que você entrega?</li>
<li>Sem rótulo não existe gabarito. Então o que torna um agrupamento bom?</li>
<li>Em que momento um cliente muda de grupo, e como o banco saberia?</li>
</ul>""")
P3 = page('p3-agrupamento.html', 3, 'Agrupamento: quem são os clientes de cartão?',
 'O produto de cartões quer três ou quatro campanhas, uma por perfil de cliente, e ninguém sabe quais são os perfis. O arquivo tem 8.950 clientes ao longo de seis meses e 17 medidas de uso: saldo, compras, saques, frequências, limite, pagamentos. Você vai deixar o k-Means propor os grupos e decidir se eles fazem sentido para o negócio.',
 '<p>Ao final, a dupla entrega uma tabela com um nome, o tamanho, o que o caracteriza e uma ação comercial para cada grupo.</p><p>Sem coluna alvo, o grupo é bom quando a área de negócio consegue nomeá-lo e agir sobre ele.</p>',
 p3, '<a href="p2-classificacao.html">← Prática 2: classificação</a>', '<a href="index.html">Índice →</a>')

for fn, html in [('p1-regressao.html', P1), ('p2-classificacao.html', P2), ('p3-agrupamento.html', P3)]:
    (HERE.parent / fn).write_text(html)
print('ok')
