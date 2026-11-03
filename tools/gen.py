import json
PTS=open(__import__('pathlib').Path(__file__).parent/'pts.json').read()
CSS=open(__import__('pathlib').Path(__file__).parent/'base.css').read()
CSS+="""
.task{background:var(--panel);border-left:4px solid var(--you);border-radius:0 10px 10px 0;padding:10px 14px;margin:14px 0 4px;max-width:78ch}
.task p{margin:0}.task p+p{margin-top:6px;color:var(--ink-2)}
.steps{color:var(--ink-2);font-size:.9rem;margin-bottom:6px}
.lock .ctl input{opacity:.5}
.wrap{position:relative}
header{padding-right:56px}
.theme{position:absolute;top:20px;right:16px;width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--ink);cursor:pointer;padding:0}
.theme:hover{border-color:var(--you)}
.theme svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.theme .sun{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .theme .sun{display:block}:root:not([data-theme="light"]) .theme .moon{display:none}}
:root[data-theme="dark"] .theme .sun{display:block}
:root[data-theme="dark"] .theme .moon{display:none}
"""
STEPS=["Ajuste na mão","Um dado errado","Treino enviesado","Descendo o vale"]

def page(k, title, intro, task, flags, extra_html_left="", extra_html_right="", extra_js=""):
    F=json.dumps(flags)
    chips = """
<div class="chips" id="chips">
  <button class="chip" data-sub="M" aria-pressed="true">Só homens</button>
  <button class="chip" data-sub="F">Só mulheres</button>
  <button class="chip" data-sub="ti">Só pessoal de TI</button>
  <button class="chip" data-sub="young">Só até 40 anos</button>
  <button class="chip" data-sub="rand">70 % aleatório</button>
  <span class="seed">seu número <input id="seed" type="number" min="1" max="999" value="1"></span>
</div>""" if flags["subsets"] else ""
    typo = '<label><input type="checkbox" id="typo" checked> incluir o dado digitado errado</label>' if flags["typo"] else ""
    must = '<label id="mustlab" hidden><input type="checkbox" id="must"> retas MUST (homens / mulheres)</label>' if flags["must"] else ""
    legend_test = '<span id="legtest" hidden><span class="hollow"></span>fora do treino</span>' if flags["subsets"] else ""
    mae = flags["mae"]
    lock = """
    <div class="row" style="margin-top:12px">
      <button class="btn primary" id="lock">Travar a reta e avaliar nos demais</button>
      <button class="btn" id="unlock" hidden>Ajustar de novo</button>
    </div>""" if flags["subsets"] else ""
    reveal = """
    <div class="row" style="margin-top:12px">
      <button class="btn" id="reveal">Revelar a melhor reta</button>
      <span id="bestinfo"></span>
    </div>""" if flags["reveal"] else ""
    center = '<div class="row"><label><input type="checkbox" id="center"> centralizar x (usar x − média)</label></div>' if flags["gd"] else ""
    heat = """
    <h2 style="margin-top:18px">Superfície do erro J(a, b)</h2>
    <p class="note" style="margin:0 0 4px">Cada pixel é um par (a, b); mais escuro, menor o erro. Clique para pular até lá.</p>
    <div class="heatwrap"><canvas id="heat" width="320" height="240"></canvas><svg id="heatsvg" viewBox="0 0 320 240"></svg></div>
    <div class="ctl" style="margin-top:10px">
      <label for="eta">taxa η</label><input type="range" id="eta" min="-5" max="0.3" step="0.05" value="-3"><span id="etav"></span>
    </div>
    <div class="row">
      <button class="btn primary" id="step1">Um passo de gradiente</button>
      <button class="btn" id="step20">20 passos</button>
      <button class="btn" id="step200">200 passos</button>
      <button class="btn" id="clear">Limpar trilha</button>
      <span id="gdmsg"></span>
    </div>""" if flags["gd"] else ""
    testmet = '<div class="met test" id="tstbox" hidden><h3 id="tst-h">Fora do treino</h3><div class="big" id="tst-mse"></div><div class="sm" id="tst-sm"></div></div>' if flags["subsets"] else ""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{k}. {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script>try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body>
<div class="wrap">
<button class="theme" id="theme" type="button" aria-label="Alternar modo claro e escuro" title="Modo claro / escuro"><svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
<header>
  <div class="steps">Etapa {k} de 4</div>
  <h1>{title}</h1>
  <p>{intro}</p>
</header>
<div class="task">{task}</div>
<div class="eq" id="eq"></div>
{chips}
<div class="grid">
  <div class="panel">
    <svg id="sc" viewBox="0 0 640 420" role="img" aria-label="Dispersão altura por antebraço com a sua reta"></svg>
    <div class="row">
      <span><span class="dot" style="background:var(--m)"></span>homens</span>
      <span><span class="dot" style="background:var(--f)"></span>mulheres</span>
      {legend_test}
      <label><input type="checkbox" id="resid"> mostrar resíduos</label>
      {typo}{must}
    </div>
    <div class="note" id="mustnote" hidden>MUST (adultos &lt; 65): homens 79,2 + 3,60·ulna; mulheres 95,6 + 2,77·ulna. <a href="https://uhra.herts.ac.uk/id/eprint/2812" target="_blank" rel="noopener">Madden, Tsikoura &amp; Stott (2012)</a>.</div>
    <div class="note" id="typonote"{"" if flags["typo"] else " hidden"}>Uma altura de 168 virou 16,8, como acontece quando alguém digita em metros. O ponto está contornado em vermelho.</div>
  </div>
  <div class="panel">
    <h2>Seus parâmetros</h2>
    <div class="ctl">
      <label for="b">a</label><input type="range" id="b"><input type="number" id="bn" step="0.01">
      <label for="a">b</label><input type="range" id="a"><input type="number" id="an" step="0.5">
    </div>
    {center}
    <div class="metrics">
      <div class="met"><h3 id="trn-h">Erro</h3><div class="big" id="trn-mse"></div><div class="sm" id="trn-sm"></div></div>
      {testmet}
    </div>
    {lock}
    {reveal}
    {heat}
  </div>
</div>
</div>
<script>
const F={F};
const PTS={PTS};
const SEX={{M:'var(--m)',F:'var(--f)',N:'var(--n)'}};
const MUST=[{{s:'M',a:79.2,b:3.60}},{{s:'F',a:95.6,b:2.77}}];
const XMEAN=PTS.reduce((s,p)=>s+p.x,0)/PTS.length;
const S={{a:(F.gd?10:150),b:(F.gd?4.5:1.2),center:false,sub:F.subsets?'M':'all',seed:1,eta:1e-3,typo:{'true' if flags['typo'] else 'false'},must:false,resid:false,reveal:false,locked:false,trail:[]}};
const $=id=>document.getElementById(id);
const on=(id,ev,fn)=>{{const e=$(id);if(e)e.addEventListener(ev,fn);}};

function data(){{ if(!S.typo) return PTS; const i=PTS.findIndex(p=>p.y===168); return PTS.map((p,k)=>k===i?{{...p,y:16.8,typo:true}}:p); }}
function rng(seed){{ let t=seed*2654435761>>>0; return ()=>{{t+=0x6D2B79F5;let r=Math.imul(t^t>>>15,1|t);r^=r+Math.imul(r^r>>>7,61|r);return((r^r>>>14)>>>0)/4294967296}}; }}
function split(){{ const D=data(); let inTrain;
  switch(S.sub){{case 'M':inTrain=p=>p.s==='M';break;case 'F':inTrain=p=>p.s==='F';break;case 'ti':inTrain=p=>p.t===1;break;case 'young':inTrain=p=>p.i<=40;break;
    case 'rand':{{const r=rng(S.seed);const idx=D.map((_,k)=>k).sort(()=>r()-.5).slice(0,Math.round(.7*D.length));const set=new Set(idx);inTrain=(p,k)=>set.has(k);break;}}
    default:inTrain=()=>true;}}
  const tr=[],te=[]; D.forEach((p,k)=>(inTrain(p,k)?tr:te).push(p)); return {{tr,te,all:D}}; }}
const xv=p=>S.center?p.x-XMEAN:p.x;
const pred=(a,b,p)=>a+b*xv(p);
function metrics(set,a=S.a,b=S.b){{ if(!set.length) return null; let se=0,ae=0; for(const p of set){{const e=pred(a,b,p)-p.y;se+=e*e;ae+=Math.abs(e);}} return {{n:set.length,mse:se/set.length,rmse:Math.sqrt(se/set.length),mae:ae/set.length}}; }}
function ols(set){{ const n=set.length; let sx=0,sy=0; for(const p of set){{sx+=xv(p);sy+=p.y;}} const mx=sx/n,my=sy/n; let sxy=0,sxx=0; for(const p of set){{sxy+=(xv(p)-mx)*(p.y-my);sxx+=(xv(p)-mx)**2;}} const b=sxy/sxx; return {{a:my-b*mx,b}}; }}
function grad(set,a,b){{ let ga=0,gb=0; for(const p of set){{const e=pred(a,b,p)-p.y;ga+=e;gb+=e*xv(p);}} return [2*ga/set.length,2*gb/set.length]; }}
function ranges(){{ return S.center?{{a:[120,230],b:[-2,8]}}:{{a:[-100,300],b:[0,10]}}; }}
const fmt=(v,d=1)=>v.toLocaleString('pt-BR',{{minimumFractionDigits:d,maximumFractionDigits:d}});
function syncSliders(){{ const R=ranges(); $('a').min=R.a[0];$('a').max=R.a[1];$('a').step=.5;$('b').min=R.b[0];$('b').max=R.b[1];$('b').step=.01;
  $('a').value=S.a;$('an').value=fmt(S.a,1).replace(',','.');$('b').value=S.b;$('bn').value=fmt(S.b,2).replace(',','.');
  ['a','an','b','bn'].forEach(i=>$(i).disabled=S.locked); document.body.classList.toggle('lock',S.locked); }}

function drawScatter(){{ const {{tr,te,all}}=split(); const showTest=!F.subsets||S.locked; const W=640,H=420,m={{l:52,r:16,t:16,b:44}};
  const xs=all.map(p=>p.x),ys=all.map(p=>p.y); const x0=Math.floor(Math.min(...xs)-1),x1=Math.ceil(Math.max(...xs)+1);
  let y0=Math.floor(Math.min(...ys)/10)*10-5,y1=Math.ceil(Math.max(...ys)/10)*10+5; if(S.typo){{y0=0;}}
  const sx=x=>m.l+(x-x0)/(x1-x0)*(W-m.l-m.r), sy=y=>H-m.b-(y-y0)/(y1-y0)*(H-m.t-m.b);
  const line=(a,b,col,dash,raw)=>{{const f=x=>a+b*(raw?x:(S.center?x-XMEAN:x)); return '<line x1="'+sx(x0)+'" y1="'+sy(f(x0))+'" x2="'+sx(x1)+'" y2="'+sy(f(x1))+'" stroke="'+col+'" stroke-width="2.5" '+(dash?'stroke-dasharray="7 5"':'')+' />';}};
  let g='<defs><clipPath id="cp"><rect x="'+m.l+'" y="'+m.t+'" width="'+(W-m.l-m.r)+'" height="'+(H-m.t-m.b)+'"/></clipPath></defs><g class="axis">';
  const xt=[];for(let x=x0;x<=x1;x+=2)xt.push(x); const yt=[];const ystep=S.typo?20:10;for(let y=y0;y<=y1;y+=ystep)yt.push(y);
  xt.forEach(x=>{{g+='<line class="gridl" x1="'+sx(x)+'" x2="'+sx(x)+'" y1="'+m.t+'" y2="'+(H-m.b)+'"/><text x="'+sx(x)+'" y="'+(H-m.b+16)+'" text-anchor="middle">'+x+'</text>';}});
  yt.forEach(y=>{{g+='<line class="gridl" x1="'+m.l+'" x2="'+(W-m.r)+'" y1="'+sy(y)+'" y2="'+sy(y)+'"/><text x="'+(m.l-8)+'" y="'+(sy(y)+4)+'" text-anchor="end">'+y+'</text>';}});
  g+='<text x="'+(W/2)+'" y="'+(H-6)+'" text-anchor="middle" style="font-size:13px;fill:var(--ink)">antebraço (cm)</text>';
  g+='<text transform="translate(14,'+(H/2)+') rotate(-90)" text-anchor="middle" style="font-size:13px;fill:var(--ink)">altura (cm)</text></g><g clip-path="url(#cp)">';
  const rs=S.resid?(showTest?tr.concat(te):tr):[];
  rs.forEach(p=>{{g+='<line x1="'+sx(p.x)+'" x2="'+sx(p.x)+'" y1="'+sy(p.y)+'" y2="'+sy(pred(S.a,S.b,p))+'" stroke="var(--err)" stroke-width="1.2" opacity=".55"/>';}});
  if(S.must) MUST.forEach(e=>{{g+=line(e.a,e.b,SEX[e.s],true,true);}});
  if(S.reveal){{const o=ols(tr); g+=line(o.a,o.b,'var(--best)',false,false);}}
  g+=line(S.a,S.b,'var(--you)',false,false);
  if(showTest) te.forEach(p=>{{g+='<circle cx="'+sx(p.x)+'" cy="'+sy(p.y)+'" r="5" fill="none" stroke="'+SEX[p.s]+'" stroke-width="1.6" opacity=".7"/>';}});
  tr.forEach(p=>{{g+='<circle cx="'+sx(p.x)+'" cy="'+sy(p.y)+'" r="5.5" fill="'+SEX[p.s]+'" '+(p.typo?'stroke="var(--err)" stroke-width="2.5"':'stroke="var(--panel)" stroke-width="1.2"')+'><title>antebraço '+fmt(p.x)+' cm, altura '+fmt(p.y)+' cm</title></circle>';}});
  g+='</g>'; $('sc').innerHTML=g; }}

function drawMetrics(){{ const {{tr,te}}=split(); const mt=metrics(tr),me=metrics(te);
  $('trn-h').textContent=(F.subsets?'Treino':'Erro')+' (n = '+tr.length+')'; $('trn-mse').textContent='MSE '+fmt(mt.mse,1);
  $('trn-sm').textContent='RMSE '+fmt(mt.rmse,2)+' cm'+(F.mae?' · MAE '+fmt(mt.mae,2)+' cm':'');
  if(F.subsets){{ $('tstbox').hidden=!S.locked; $('legtest').hidden=!S.locked; if(me){{$('tst-h').textContent='Fora do treino (n = '+te.length+')';$('tst-mse').textContent='MSE '+fmt(me.mse,1);$('tst-sm').textContent='RMSE '+fmt(me.rmse,2)+' cm'+(F.mae?' · MAE '+fmt(me.mae,2)+' cm':'');}} }}
  const xl=S.center?'(x − '+fmt(XMEAN,1)+')':'x';
  $('eq').innerHTML='ŷ = <b>'+fmt(S.b,2)+'</b> · '+xl+' + <b>'+fmt(S.a,1)+'</b>';
  if(F.reveal){{ if(S.reveal){{const o=ols(tr),mo=metrics(tr,o.a,o.b);$('bestinfo').innerHTML='<span class="best">a = '+fmt(o.b,2)+', b = '+fmt(o.a,1)+'</span>, MSE '+fmt(mo.mse,1)+(F.mae?', MAE '+fmt(mo.mae,2):'')+(F.subsets&&me?' · fora do treino MSE '+fmt(metrics(te,o.a,o.b).mse,1)+', MAE '+fmt(metrics(te,o.a,o.b).mae,2):'');}} else $('bestinfo').textContent=''; }} }}

let heatCache=null;
function hex(s){{s=s.trim().replace('#','');return [0,2,4].map(i=>parseInt(s.substr(i,2),16));}}
function drawHeat(force){{ if(!F.gd) return; const {{tr}}=split(); const R=ranges(); const cv=$('heat'),W=cv.width,H=cv.height,ctx=cv.getContext('2d');
  const key=S.sub+S.seed+S.center+S.typo+matchMedia('(prefers-color-scheme:dark)').matches+(document.documentElement.dataset.theme||'');
  if(force||heatCache!==key){{ heatCache=key; const img=ctx.createImageData(W,H); const vals=new Float32Array(W*H); let lo=Infinity,hi=-Infinity;
    for(let j=0;j<H;j++)for(let i=0;i<W;i++){{const a=R.a[0]+(i/(W-1))*(R.a[1]-R.a[0]);const b=R.b[1]-(j/(H-1))*(R.b[1]-R.b[0]);const v=Math.log(metrics(tr,a,b).mse);vals[j*W+i]=v;if(v<lo)lo=v;if(v>hi)hi=v;}}
    const cs=getComputedStyle(document.documentElement); const c0=hex(cs.getPropertyValue('--heat0')),c1=hex(cs.getPropertyValue('--heat1'));
    for(let k=0;k<W*H;k++){{const t=1-(vals[k]-lo)/(hi-lo);const q=Math.pow(t,2.2);img.data[4*k]=c0[0]+(c1[0]-c0[0])*q;img.data[4*k+1]=c0[1]+(c1[1]-c0[1])*q;img.data[4*k+2]=c0[2]+(c1[2]-c0[2])*q;img.data[4*k+3]=255;}}
    ctx.putImageData(img,0,0); }}
  const px=a=>(a-R.a[0])/(R.a[1]-R.a[0])*W, py=b=>(R.b[1]-b)/(R.b[1]-R.b[0])*H;
  const every=Math.max(1,Math.ceil(S.trail.length/400)), last=S.trail.length-1;
  let g='<g>'; S.trail.forEach((t,k)=>{{ if(k>0){{const u=S.trail[k-1];g+='<line x1="'+px(u[0])+'" y1="'+py(u[1])+'" x2="'+px(t[0])+'" y2="'+py(t[1])+'" stroke="var(--you)" stroke-width="1.5" opacity=".8"/>';}} if(k%every===0||k===last) g+='<circle cx="'+px(t[0])+'" cy="'+py(t[1])+'" r="2.5" fill="var(--you)"/>'; }}); g+='</g>';
  if(S.reveal){{const o=ols(tr);g+='<circle cx="'+px(o.a)+'" cy="'+py(o.b)+'" r="6" fill="none" stroke="var(--best)" stroke-width="2.5"/>';}}
  g+='<circle cx="'+px(S.a)+'" cy="'+py(S.b)+'" r="6" fill="var(--you)" stroke="#fff" stroke-width="2"/>';
  g+='<text x="6" y="14" style="font-size:11px;fill:var(--ink-2)">a = '+fmt(R.b[1],0)+'</text><text x="6" y="'+(H-6)+'" style="font-size:11px;fill:var(--ink-2)">a = '+fmt(R.b[0],0)+'</text>';
  g+='<text x="'+(W-6)+'" y="'+(H-6)+'" text-anchor="end" style="font-size:11px;fill:var(--ink-2)">b = '+fmt(R.a[1],0)+'</text><text x="'+(W/2)+'" y="'+(H-6)+'" text-anchor="middle" style="font-size:11px;fill:var(--ink-2)">b →</text>';
  $('heatsvg').innerHTML=g; }}
function render(force){{ syncSliders(); drawScatter(); drawMetrics(); drawHeat(force); }}

function gdSteps(n){{ const {{tr}}=split(); const R=ranges(); if(!S.trail.length)S.trail.push([S.a,S.b]); let div=false;
  for(let k=0;k<n;k++){{const [ga,gb]=grad(tr,S.a,S.b); S.a-=S.eta*ga; S.b-=S.eta*gb; S.trail.push([S.a,S.b]); if(!isFinite(S.a)||Math.abs(S.a)>1e6||Math.abs(S.b)>1e5){{div=true;break;}} }}
  if(div){{S.a=Math.min(Math.max(S.a,R.a[0]),R.a[1]);S.b=Math.min(Math.max(S.b,R.b[0]),R.b[1]);$('gdmsg').innerHTML='<span class="warn">divergiu: η grande demais para esta escala de x</span>';}}
  else{{const [ga,gb]=grad(tr,S.a,S.b);$('gdmsg').textContent='gradiente (∂a = '+fmt(gb,2)+', ∂b = '+fmt(ga,2)+')';}}
  if(S.trail.length>5000)S.trail=S.trail.slice(-5000); render(); }}

on('chips','click',e=>{{const c=e.target.closest('.chip');if(!c)return;S.sub=c.dataset.sub;document.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed',x===c));S.trail=[];S.reveal=false;S.locked=false;unlockUI();render();}});
on('seed','input',e=>{{S.seed=+e.target.value||1;if(S.sub==='rand'){{S.locked=false;unlockUI();render();}}}});
on('a','input',e=>{{S.a=+e.target.value;S.trail=[];render();}});
on('b','input',e=>{{S.b=+e.target.value;S.trail=[];render();}});
on('an','change',e=>{{S.a=+e.target.value;S.trail=[];render();}});
on('bn','change',e=>{{S.b=+e.target.value;S.trail=[];render();}});
on('center','change',e=>{{ S.a=e.target.checked?S.a+S.b*XMEAN:S.a-S.b*XMEAN; S.center=e.target.checked; S.trail=[]; $('gdmsg').textContent=''; render(true); }});
on('resid','change',e=>{{S.resid=e.target.checked;drawScatter();}});
on('must','change',e=>{{S.must=e.target.checked;$('mustnote').hidden=!S.must;drawScatter();}});
on('typo','change',e=>{{S.typo=e.target.checked;$('typonote').hidden=!S.typo;S.reveal=false;if($('reveal'))$('reveal').textContent='Revelar a melhor reta';render(true);}});
on('reveal','click',()=>{{S.reveal=!S.reveal;$('reveal').textContent=S.reveal?'Esconder a melhor reta':'Revelar a melhor reta';render();}});
function unlockUI(){{ if(!F.subsets) return; $('lock').hidden=S.locked; $('unlock').hidden=!S.locked; if(F.must){{$('mustlab').hidden=!S.locked; if(!S.locked){{S.must=false;$('must').checked=false;$('mustnote').hidden=true;}}}} }}
on('lock','click',()=>{{S.locked=true;unlockUI();render();}});
on('unlock','click',()=>{{S.locked=false;S.reveal=false;unlockUI();render();}});
on('eta','input',e=>{{S.eta=Math.pow(10,+e.target.value);$('etav').textContent='η = '+S.eta.toExponential(1).replace('e','·10^');}});
on('step1','click',()=>gdSteps(1));
on('step20','click',()=>gdSteps(20));
on('step200','click',()=>gdSteps(200));
on('clear','click',()=>{{S.trail=[];$('gdmsg').textContent='';drawHeat();}});
on('heat','click',e=>{{const r=e.target.getBoundingClientRect();const R=ranges();const fx=(e.clientX-r.left)/r.width,fy=(e.clientY-r.top)/r.height;S.a=R.a[0]+fx*(R.a[1]-R.a[0]);S.b=R.b[1]-fy*(R.b[1]-R.b[0]);S.trail=[];render();}});
matchMedia('(prefers-color-scheme:dark)').addEventListener('change',()=>render(true));
if($('etav'))$('etav').textContent='η = 1.0·10^-3';
render(true);
</script>
<script>
(function(){{const b=document.getElementById('theme');if(!b)return;
const dark=()=>{{const t=document.documentElement.dataset.theme;return t?t==='dark':matchMedia('(prefers-color-scheme:dark)').matches;}};
b.addEventListener('click',()=>{{const next=dark()?'light':'dark';document.documentElement.dataset.theme=next;
  try{{localStorage.setItem('theme',next)}}catch(e){{}}
  if(typeof render==='function')render(true);}});}})();
</script>
</body>
</html>"""

base=dict(subsets=False,typo=False,must=False,mae=True,reveal=False,gd=False)
pages=[
 ("1-ajuste.html", STEPS[0],
  "Cada ponto é uma pessoa da turma: comprimento do antebraço no eixo horizontal, altura no vertical. A reta verde é o seu modelo, ŷ = a·x + b.",
  "<p>Mova <b>a</b> e <b>b</b> até a reta passar bem pelo meio dos pontos. Acompanhe o MSE: tente ficar abaixo de 45.</p><p>Depois ligue os resíduos e veja o que o MSE está somando. Quando achar que não dá para melhorar, revele a melhor reta e compare com a sua.</p>",
  dict(base,reveal=True)),
 ("2-dado-errado.html", STEPS[1],
  "A mesma turma, agora com MAE ao lado do MSE. Uma das respostas foi digitada em metros.",
  "<p>Ajuste a reta com o dado errado incluído e anote MSE e MAE. Depois desmarque o dado errado, ajuste de novo e anote.</p><p>Qual métrica mudou mais? Qual das duas retas você usaria para prever a altura de uma pessoa nova? Revele a melhor reta nos dois casos e veja para onde ela foi puxada.</p>",
  dict(base,typo=True,mae=True,reveal=True)),
 ("3-enviesado.html", STEPS[2],
  "Agora você treina só com parte da turma. Quem ficou de fora não aparece até você travar a reta.",
  "<p>Escolha um grupo, ajuste a reta para ele e trave. O erro nas pessoas de fora aparece junto com os pontos vazados.</p><p>Repita com outro grupo. Em qual caso o erro de fora ficou mais longe do erro de treino, e por quê? No 70 % aleatório, use o seu número da lista como semente e compare os coeficientes com os colegas.</p>",
  dict(base,subsets=True,must=True,reveal=True)),
 ("4-gradiente.html", STEPS[3],
  "O mapa à direita mostra o erro para cada par (a, b): a inclinação a na vertical, o intercepto b na horizontal. Um algoritmo só sente a inclinação do ponto onde está e dá um passo ladeira abaixo; ele nunca vê o mapa inteiro.",
  "<p>Dê alguns passos de gradiente e observe a trilha no mapa. Aumente η até divergir; diminua até parar de andar.</p><p>Depois marque <b>centralizar x</b>, olhe a forma do vale e repita. Por que ficou tão mais fácil?</p>",
  dict(base,gd=True,reveal=True)),
]
for fn,t,intro,task,fl in pages:
    open(str(__import__('pathlib').Path(__file__).parent.parent/fn),'w').write(page(fn[0],t,intro,task,fl))
print("ok")
