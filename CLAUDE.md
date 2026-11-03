# Curso de ML para o Banrisul – material prático

Dono: Lucas Kupssinskü (PUCRS). Site público: https://lucaskup.github.io/ml-banrisul/
Repositório: https://github.com/lucaskup/ml-banrisul (GitHub Pages servindo a branch `main`, raiz).

A raiz do repositório é o conteúdo do GitHub Pages. `tools/` guarda os geradores e `docs/` o guia
do instrutor. Os workflows `.ows` apontam para `https://lucaskup.github.io/ml-banrisul/data/<arquivo>.csv`,
então não renomear arquivos nem mover pastas.

## Mapa do repositório

```
index.html                      índice: regressão (antebraço), k-means (Iris) e três práticas Orange
1-ajuste.html … 4-gradiente.html         práticas de regressão linear com dados da turma (geradas por tools/gen.py)
c1-passo-a-passo.html … c3-limitacoes.html   práticas de k-means (editadas à mão, sem gerador)
data/insurance.csv              1.338 segurados; cabeçalho com prefixos de papel do Orange (cC# = alvo)
data/german_credit.csv          1.000 solicitantes de crédito; alvo risco (bom/mau)
data/cartao.csv                 8.950 clientes de cartão; cliente como meta (mS#)
p1-regressao.html, p2-classificacao.html, p3-agrupamento.html   roteiros auto-guiados das práticas Orange (gerados por tools/gen_praticas.py)
orange/p{1,2,3}_*_inicio.ows    workflows de partida (exploração ligada, modelagem por ligar)
orange/p{1,2,3}_*_completo.ows  gabarito com tudo ligado
qr/*.svg                        QR codes para os slides (índice e uma por página interativa)
tools/
  gen.py + base.css + pts.json  regenera as quatro páginas do antebraço (pts.json = respostas anonimizadas)
  prep_data.py + *_pt.csv       regenera data/*.csv a partir dos CSV em português
  ows.py + reg.json             regenera os seis .ows (reg.json = nomes de widgets/canais do Orange 3.40)
  gen_praticas.py               regenera os três roteiros das práticas Orange (números das caixas "Confira" = guia)
  qr.py                         regenera qr/*.svg (pip install segno)
  orng.py                       helpers usados para calcular os números do guia (API do Orange)
docs/guia_instrutor.md          guia de condução das três práticas, com números esperados
```

Todos os geradores rodam a partir de qualquer diretório (`python tools/gen.py`) e escrevem na raiz.
`prep_data.py` precisa de pandas; `ows.py` e `gen.py` só da biblioteca padrão.

## Regras

- Não alterar os números de `docs/guia_instrutor.md` sem reproduzir no Orange; eles vieram de
  validação cruzada 10-fold com `random_state=42` (regressão/classificação) e k-Means com
  `random_state=0`, dados normalizados 0–1 para o kNN via Preprocess. Em 3 nov 2026 foram
  reproduzidos com Orange 3.40.0 e scikit-learn 1.9.1: regressão e k-Means batem; a regressão
  logística varia cerca de 1 ponto de acurácia conforme a versão do scikit-learn.
- Os dados do antebraço (`tools/pts.json`) são de pessoas reais, já anonimizados (só sexo, idade,
  antebraço, altura e indicador TI). Não adicionar colunas.
- Se a URL base mudar, editar `BASE` em `tools/ows.py` e em `tools/qr.py` e regenerar; o Orange
  guarda a URL no `.ows`.
- As páginas `1-…4-*.html` são saída de `tools/gen.py` e `p1-…p3-*.html` de `tools/gen_praticas.py`:
  editar o gerador, não o HTML, para a mudança não se perder na próxima regeneração.
- Depois de um push, `gh api repos/lucaskup/ml-banrisul/pages --jq '.status'` deve devolver `built`.
- Texto para o usuário em português; código e nomes de arquivo como estão.

## Prosa

Valem as regras de prosa do curso de deep learning (`~/Projects/courses/deep-learning-course/AGENTS.md`,
seção "Prose style for course content"): sem `-`/`---` como parêntese; afirmação antes da negação;
sem adjetivo que só sinaliza importância ou grau ("lição central", "pergunta boa"); sem rótulo de
resumo ("A lição", "Resumindo"); sujeito primeiro, sem frase invertida; e cada página é autocontida,
sem apontar para outra parte do material por posição ("na etapa 3", "na próxima prática", "como vimos").
Nomear o conceito em vez da posição ("depois da normalização", "quando o k-Means entrar").
