# Práticas com Orange – guia do instrutor

Nov 3, 2026 · @Lucas Kupssinskü

## Visão geral

Três práticas de 60 minutos no Orange, em duplas, uma por tarefa de aprendizado: regressão linear (custo de seguro), regressão logística e KNN (risco de crédito) e k-means (segmentação de clientes de cartão). Cada prática segue o mesmo relógio, o que reduz a carga de explicar o formato três vezes.

| Bloco | Minutos | O que acontece |
| --- | --- | --- |
| Abertura | 0–5 | Você apresenta a pergunta de negócio e abre o dataset projetado |
| Exploração guiada | 5–15 | Duplas abrem o workflow pronto, olham tabela, distribuições e um gráfico que você indica |
| Construção | 15–40 | Duplas completam o workflow (modelo, avaliação) e anotam o número pedido |
| Quebra o modelo | 40–50 | Uma alteração proposital que muda o resultado; a dupla explica por quê |
| Fechamento | 50–60 | Cada dupla reporta um número; você compara no quadro e conduz a discussão |

Duplas porque uma pessoa opera o Orange enquanto a outra lê e interpreta; troque os papéis aos 30 minutos. Com 50 pessoas são 25 duplas; o fechamento funciona com cada dupla dizendo um único número em voz alta enquanto você anota no quadro, o que leva cerca de 3 minutos e já mostra a variância entre duplas.

Materiais, todos no repositório do curso ([lucaskup.github.io/ml-banrisul](https://lucaskup.github.io/ml-banrisul/)):

- `data/insurance.csv`, `data/german_credit.csv`, `data/cartao.csv`: os três datasets, já com nomes de colunas em português.
- `orange/p1_regressao_inicio.ows`, `orange/p2_classificacao_inicio.ows`, `orange/p3_agrupamento_inicio.ows`: workflows de partida, com os widgets de carga e exploração já conectados e os de modelagem por conectar. Os `*_completo.ows` são o gabarito com tudo ligado.
- Orange 3.38 ou mais novo instalado em cada máquina (instalador em orangedatamining.com; peça à TI do Banrisul com uma semana de antecedência, porque o instalador tem \~500 MB e o primeiro boot demora).

O widget File do Orange aceita URL, então os workflows apontam direto para os CSV no GitHub Pages. Se a rede do banco bloquear github.io, distribua a pasta `data/` por pendrive e troque a URL pelo arquivo local no widget File (um clique).

## Prática 1 – Regressão: quanto custa o seguro desta pessoa?

A lição central: a regressão linear explica 75 % da variação do custo com sete variáveis e um coeficiente legível por variável; o kNN sem normalização explica 28 % porque a escala de idade e IMC esconde a variável que mais importa (fumante), e com normalização passa a 77 %.

**Dataset.** `insurance.csv`: 1.338 segurados de um plano de saúde nos EUA; idade, sexo, IMC, filhos, fumante, região e o alvo `custo_anual` em dólares (média 13.270, mediana 9.382, máximo 63.770). O arquivo já marca `custo_anual` como alvo no cabeçalho, então o widget File abre com o papel certo. Pergunta de negócio: a corretora precisa cotar um prêmio para uma pessoa nova; quais características pesam, e quanto?

**Roteiro.**

1. 0–5: projete o Data Table e pergunte à turma qual coluna eles acham que mais pesa. Anote as apostas no quadro.
2. 5–15: duplas abrem `p1_regressao_inicio.ows`. Feature Statistics mostra as escalas (idade 18–64, IMC 16–53, custo até 63 mil). No Scatter Plot, custo × idade colorido por fumante: três faixas visíveis, a de cima só de fumantes. Peça que mudem o eixo x para IMC: nos fumantes, acima de IMC 30 o custo dobra.
3. 15–40: ligam File → Test and Score (Data) e Linear Regression e kNN → Test and Score (Learner), validação cruzada em 10 folds. Números esperados abaixo. Depois ligam File → Linear Regression → Predictions com uma pessoa inventada no Data Table (ou editada num CSV de uma linha): 45 anos, homem, IMC 30, 2 filhos, fumante, sudeste dá cerca de US$ 33.400; a mesma pessoa não fumante, US$ 9.600.
4. 40–50 (quebra): ligam Preprocess → kNN (Preprocessor). O widget Preprocess dos workflows já vem com Normalize Features em [0, 1]; basta ligar. O kNN sai de R² 0,28 para 0,77 e passa a regressão linear. Pergunte: o que a normalização mudou? A resposta está na distância: sem normalizar, 10 anos de idade valem 10 unidades e fumar vale 1.
5. 50–60: cada dupla reporta o RMSE do melhor modelo. Discussão: o modelo com menor erro (kNN) não dá coeficiente; a linear dá “fumante: +11.924 por lado”, ou seja, 23.850 de diferença. Para um comitê de precificação ou para um regulador, qual dos dois você defende?

**Números esperados** (10 folds, semente pode variar ± 2 %):

| Modelo | RMSE (US$) | MAE (US$) | R² |
| --- | --- | --- | --- |
| Regressão linear | 6.084 | 4.205 | 0,747 |
| kNN, k = 5, sem normalizar | 10.266 | 6.735 | 0,281 |
| kNN, k = 5, normalizado 0–1 | 5.777 | 3.541 | 0,772 |
| kNN, k = 15, normalizado | 6.204 | 3.830 | 0,737 |
| Linear sem a coluna fumante | 11.375 | — | 0,117 |
| Linear só com a coluna fumante | 7.482 | — | 0,618 |

Coeficientes da regressão linear (widget Linear Regression, saída Coefficients): intercepto −667; idade +257 por ano; IMC +339 por ponto; filhos +476 por filho; fumante sim +11.924 e não −11.924 (o Orange divide o efeito entre os dois níveis); sexo e região abaixo de 600 em módulo, próximos de ruído.

**Perguntas para o fechamento.**

- Uma única variável binária explica 62 % da variação. O que isso diz sobre coletar mais dados versus coletar a variável certa?
- O RMSE de 6.000 dólares é bom? Compare com a mediana de 9.400 e com o desvio padrão de 12.100.
- A reta superestima jovens não fumantes e subestima fumantes obesos. Onde o banco perderia dinheiro com esse erro sistemático?

## Prática 2 – Classificação: aprovar ou negar o crédito?

A lição central: acurácia engana quando as classes são desbalanceadas e os erros custam diferente. Aprovar todo mundo acerta 70 %; a regressão logística acerta 75 % e corta o custo pela metade; baixar o limiar de 0,5 para 0,2 derruba a acurácia para 66 % e corta o custo em mais um terço.

**Dataset.** `german_credit.csv` (Statlog German Credit, UCI): 1.000 solicitantes de um banco alemão nos anos 1990, 20 atributos (conta corrente, prazo, valor, histórico, poupança, emprego, estado civil e sexo, idade, moradia, ocupação, etc.) e o alvo `risco` com 700 bons e 300 maus. Nomes de coluna em português, valores em inglês como no original. A matriz de custo acompanha o dataset: aprovar um mau pagador custa 5, negar um bom custa 1. Pergunta de negócio: a mesa de crédito quer um modelo que diga quem negar; o que é “um modelo bom” aqui?

**Roteiro.**

1. 0–5: mostre o Distributions de `risco`. Pergunte: um modelo que aprova todo mundo acerta quanto? (70 %.) Escreva 70 % no quadro e deixe lá a aula inteira.
2. 5–15: duplas abrem `p2_classificacao_inicio.ows`. No Rank, `conta_corrente`, `prazo_meses`, `historico_credito` e `poupanca` lideram. No Distributions, `conta_corrente` dividido por risco: quem não tem conta corrente é o grupo mais seguro, uma peculiaridade conhecida desse dataset que rende uma pergunta boa (quem são essas pessoas?).
3. 15–40: ligam File → Test and Score, Logistic Regression e kNN → Test and Score, e Test and Score → Confusion Matrix. Com a matriz na tela, cada dupla calcula o custo de cada modelo: 5 × (maus aprovados) + 1 × (bons negados). O kNN sem normalizar perde para “aprovar todo mundo” em acurácia; a logística ganha em tudo.
4. 40–50 (quebra): no Confusion Matrix, selecionar a célula “mau previsto como bom” e mandar para um Data Table: são os 158 clientes que o modelo aprovaria e que deram prejuízo. Depois, o limiar: no Predictions ligado à Logistic Regression, ordenar pela probabilidade de `mau` e contar quantos seriam negados com corte 0,3 em vez de 0,5. Opcional: Preprocess (Normalize) → kNN, que sobe o kNN de 65 % para 73 %.
5. 50–60: cada dupla reporta o custo do melhor modelo. Encerramento com dois pontos: o modelo de menor acurácia pode ser o de menor custo, e `estado_civil_sexo` está entre os 12 atributos de maior peso. Removê-lo custa 0,6 ponto de acurácia; mantê-lo expõe o banco a uma decisão de crédito que depende de sexo e estado civil. O que o Banrisul faria?

**Números esperados** (10 folds; TP = maus corretamente negados, FN = maus aprovados, FP = bons negados):

| Modelo | Acurácia | AUC | FN (maus aprovados) | FP (bons negados) | Custo 5·FN + FP |
| --- | --- | --- | --- | --- | --- |
| Aprovar todo mundo | 0,700 | 0,500 | 300 | 0 | 1.500 |
| Regressão logística | 0,749 | 0,785 | 158 | 93 | 883 |
| kNN, k = 5, sem normalizar | 0,647 | 0,563 | 230 | 123 | 1.273 |
| kNN, k = 5, normalizado | 0,729 | 0,702 | 191 | 80 | 1.035 |
| kNN, k = 15, normalizado | 0,744 | 0,742 | 211 | 45 | 1.100 |
| Logística sem estado\_civil\_sexo | 0,743 | 0,784 | 161 | 96 | 901 |

Efeito do limiar na regressão logística (negar quando P(mau) ≥ t):

| Limiar t | Acurácia | Negados | Maus aprovados | Bons negados | Custo |
| --- | --- | --- | --- | --- | --- |
| 0,50 | 0,749 | 235 | 158 | 93 | 883 |
| 0,40 | 0,730 | 326 | 122 | 148 | 758 |
| 0,30 | 0,709 | 429 | 81 | 210 | 615 |
| 0,20 | 0,663 | 551 | 43 | 294 | 509 |
| 0,15 | 0,606 | 628 | 33 | 361 | 526 |

O mínimo de custo fica perto de t = 0,2, onde o banco nega mais da metade dos pedidos. Pergunte se a mesa de crédito aceitaria isso, e o que mudaria se o custo de negar um bom cliente fosse 2 em vez de 1.

**Perguntas para o fechamento.**

- Se a acurácia não serve, que número você pediria no relatório do modelo?
- Os 5 e 1 da matriz de custo vieram de onde? Quem no banco saberia os valores reais?
- O dataset tem 30 anos e é de outro país. O que precisaria ser verdade para o modelo valer para clientes do Banrisul?

## Prática 3 – Agrupamento: quem são os clientes de cartão?

A lição central: sem rótulo não existe gabarito, então o grupo é bom quando a área de negócio consegue nomeá-lo e agir sobre ele. Com normalização, o k-Means separa três comportamentos (pouco uso, compradores, sacadores); sem normalização, separa três faixas de valor, e o terceiro grupo são 134 clientes enormes.

**Dataset.** `cartao.csv` (Credit Card Dataset for Clustering, Kaggle): 8.950 clientes de cartão ao longo de seis meses, 17 variáveis de uso: saldo, compras à vista e parceladas, saque (cash advance), frequências de cada um, número de transações, limite, pagamentos, pagamento mínimo, percentual de meses com pagamento integral e tempo de cliente. A coluna `cliente` é identificador e o arquivo já a marca como meta. Há 313 valores faltantes em `pagamento_minimo` e 1 em `limite`; o k-Means do Orange imputa pela média sem avisar, o que vale mencionar. Pergunta de negócio: o produto de cartões quer três ou quatro campanhas, uma por perfil; quais são os perfis?

**Roteiro.**

1. 0–5: projete o Feature Statistics. Saldo vai de 0 a 19 mil, frequências vão de 0 a 1. Pergunte o que acontece com uma distância euclidiana entre essas colunas.
2. 5–15: duplas abrem `p3_agrupamento_inicio.ows`, olham Data Table e Feature Statistics, e escolhem no Scatter Plot compras × saque: a maioria está colada nos eixos, quase ninguém faz os dois.
3. 15–40: ligam File → k-Means com “From 2 to 10” e Normalize columns marcado. A tabela de silhuetas dá máximo em k = 3 (0,25). Ligam k-Means → Silhouette Plot, Scatter Plot (colorir por Cluster) e Box Plot (agrupar por Cluster, uma variável por vez). Cada dupla preenche uma linha por grupo: nome, tamanho, o que o caracteriza, uma ação.
4. 40–50 (quebra): desmarcar Normalize columns e refazer com k = 3. Os grupos viram pequeno, médio e grande em dinheiro, e um deles tem 134 pessoas. Segunda quebra, se houver tempo: tirar `saque` e `freq_saque` no Select Columns e rodar de novo; o grupo dos sacadores desaparece.
5. 50–60: cada dupla lê o nome que deu a um grupo. Os nomes convergem? Discussão: a silhueta de 0,25 é baixa em termos absolutos; os grupos existem mesmo ou o k-Means inventou? Mostre o PCA (duas componentes, colorido por cluster) para ver que há separação parcial com sobreposição grande.

**Números esperados** (normalizado, k = 3, semente 0; os rótulos 0/1/2 podem vir em outra ordem em cada máquina):

| Grupo | n | Saldo médio | Compras | Saque | Freq. compras | Freq. saque | Limite | Pagamentos | Pag. integral | Nome sugerido |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 6.108 | 804 | 500 | 335 | 0,46 | 0,07 | 3.266 | 910 | 15 % | Pouco uso |
| B | 1.261 | 2.190 | 4.214 | 453 | 0,95 | 0,06 | 7.682 | 4.098 | 30 % | Compradores |
| C | 1.581 | 4.003 | 387 | 3.887 | 0,23 | 0,45 | 6.697 | 3.027 | 3 % | Sacadores |

Silhueta por k (normalizado): 2 → 0,21; 3 → 0,25; 4 → 0,20; 5 → 0,19; 6 a 10 entre 0,20 e 0,22. Com k = 4 o grupo de compradores se divide em compradores frequentes (3.367) e grandes compradores (409, compras médias de 7.700), o que também é um resultado defensável para campanha.

Sem normalizar, k = 3: grupos de 6.514 (saldo 855, compras 603), 2.302 (saldo 3.384, compras 1.586, saque 2.091) e 134 (saldo 4.797, compras 10.471, pagamentos 17.991).

**Perguntas para o fechamento.**

- Os sacadores pagam só o mínimo em 97 % dos meses. Isso é um grupo de receita de juros ou um grupo de risco? Quem decide?
- Se o produto pediu quatro campanhas e a silhueta prefere três, o que você entrega?
- Em que momento um cliente muda de grupo, e como o banco saberia?

## Problemas comuns no Orange e como resolver em sala

| Sintoma | Causa provável | Solução em 30 segundos |
| --- | --- | --- |
| Widget File com ícone vermelho ao abrir o workflow | Rede bloqueou github.io | No File, trocar de URL para arquivo e apontar para o CSV do pendrive |
| Test and Score vazio ou em cinza | Falta a ligação de Data, ou o alvo não está definido | Conferir a linha File → Test and Score; no File, a coluna alvo deve ter papel target |
| Linear Regression com erro “numeric target expected” | Alguém mudou o papel de `custo_anual` | No File, devolver `custo_anual` para target e clicar Apply |
| Logistic Regression ou kNN com erro de dados faltantes | Só ocorre se trocarem de dataset; os três aqui não têm faltantes nos atributos usados | Inserir Impute entre File e o modelo |
| k-Means demora mais de um minuto | 8.950 linhas com k de 2 a 10 e 10 inicializações | Normal; se passar de dois minutos, reduzir “Re-runs” para 3 |
| Resultados diferentes entre duplas | Validação cruzada e k-Means usam embaralhamento aleatório | Esperado; use a variação no fechamento como argumento |
| Scatter Plot não mostra cor por cluster | Ligação veio do File e não do k-Means | Religar a partir da saída Data do k-Means |
| Confusion Matrix mostra números estranhos | Está em proporção e não em contagem | Mudar “Show” para “Number of instances” |
| Predictions não aceita o modelo | A entrada Predictors precisa do Model, e o widget do modelo precisa receber Data | Ligar File → Linear Regression (Data) e depois Linear Regression → Predictions (Model) |

Dois cuidados de preparação: abra os três workflows completos (`*_completo.ows`) na máquina da sala na véspera, com a rede do banco, e deixe uma cópia dos CSV em pendrive. O Orange guarda a URL no workflow, então qualquer troca de endereço no GitHub Pages exige regenerar os arquivos `.ows`.
