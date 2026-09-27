# Estratégias de Scalping para Opções Binárias — Guia Detalhado

## Aviso importante

Opções binárias são instrumentos de altíssimo risco. Na maioria das corretoras o payoff é assimétrico (ganho médio de 70-90% contra perda de 100% do valor investido), o que exige uma taxa de acerto estrutural acima de 55-60% só para empatar no longo prazo. Nenhuma estratégia listada aqui garante lucro. Backtestes e contas demo antes de operar com dinheiro real, controle de risco por operação (1-2% da banca) e disciplina para parar após perdas consecutivas são pré-requisitos, não detalhes opcionais. Timeframes de 10 segundos a 1 minuto são dominados por ruído e spread/slippage da corretora — trate os resultados de qualquer estratégia nessa faixa com ceticismo redobrado.

---

## Parte 1 — 20 estratégias para scalping ultracurto (10 segundos a 1 minuto)

Nessa faixa de tempo, o preço se comporta de forma quase aleatória em grande parte do tempo. As estratégias abaixo tentam capturar micro-ineficiências em momentos específicos (rompimento de nível, exaustão de movimento, reversão à média), não prever a direção do mercado de forma genérica.

### 1. Reversão nas Bandas de Bollinger (M1, expiração 1-2 velas)
- **Indicador:** Bandas de Bollinger (20, 2).
- **Entrada:** compra (CALL) quando o preço toca ou rompe levemente a banda inferior e a vela seguinte fecha de volta dentro do canal; venda (PUT) no espelho na banda superior.
- **Filtro:** evitar entradas quando as bandas estão se abrindo de forma acentuada (indica tendência forte, não faixa lateral).
- **Expiração:** 1 a 3 candles de M1.

### 2. Cruzamento de médias móveis rápidas (EMA 3 x EMA 8)
- **Indicador:** EMA de 3 e EMA de 8 períodos em M1.
- **Entrada:** CALL quando EMA 3 cruza EMA 8 para cima; PUT no cruzamento inverso.
- **Filtro:** operar só a favor da EMA de 21 períodos (tendência de fundo) para reduzir sinais falsos.
- **Expiração:** 1-2 minutos.

### 3. Pin Bar em suporte/resistência de curto prazo
- **Setup:** identificar um nível de suporte/resistência formado nas últimas 20-30 velas de M1.
- **Entrada:** vela com pavio longo rejeitando o nível (pin bar) — CALL no suporte, PUT na resistência.
- **Confirmação:** volume/tick maior que a média nas 2 últimas velas, se a plataforma exibir tick volume.
- **Expiração:** 1-2 minutos.

### 4. RSI(2) em extremos
- **Indicador:** RSI de período 2 (muito sensível).
- **Entrada:** CALL quando RSI(2) cai abaixo de 5 e começa a virar para cima; PUT quando ultrapassa 95 e começa a cair.
- **Contexto:** funciona melhor em mercado lateral; evitar em tendência forte (RSI pode ficar "preso" no extremo).
- **Expiração:** 1 candle.

### 5. Estocástico rápido (5,3,3) em zonas extremas
- **Indicador:** Estocástico configurado 5,3,3.
- **Entrada:** CALL no cruzamento %K sobre %D abaixo de 20; PUT no cruzamento %K sob %D acima de 80.
- **Filtro adicional:** confirmar com uma vela de reversão (martelo, engolfo) no mesmo ponto.
- **Expiração:** 1-2 minutos.

### 6. Rompimento de canal de Donchian curto (10 períodos)
- **Indicador:** Canal de Donchian (10).
- **Entrada:** CALL no rompimento da máxima das últimas 10 velas com fechamento acima; PUT no rompimento da mínima.
- **Uso:** captura início de micro-tendências, não reversões.
- **Expiração:** 2-3 minutos (dar tempo ao movimento se desenvolver).

### 7. Padrão de Engolfo (Engulfing) em nível-chave
- **Setup:** vela de engolfo de alta/baixa ocorrendo exatamente sobre suporte/resistência previamente respeitado.
- **Entrada:** CALL no engolfo de alta sobre suporte; PUT no engolfo de baixa sobre resistência.
- **Expiração:** 1-2 minutos.

### 8. Retração de Fibonacci intrabar
- **Setup:** identificar um impulso claro nas últimas 15-20 velas de M1 e traçar Fibonacci do início ao fim do movimento.
- **Entrada:** CALL na zona de 61,8%-78,6% de retração em tendência de alta com sinal de reversão; espelho para PUT.
- **Expiração:** 1-2 minutos.

### 9. Linha de tendência de curtíssimo prazo
- **Setup:** traçar linha de tendência conectando pelo menos 3 fundos (alta) ou topos (baixa) recentes em M1.
- **Entrada:** CALL no toque da linha de tendência ascendente com vela de rejeição; PUT no toque da descendente.
- **Expiração:** 1 minuto.

### 10. Três Soldados Brancos / Três Corvos Negros em M1
- **Padrão:** três velas consecutivas de alta (ou baixa) com corpos crescentes e poucos pavios.
- **Entrada:** CALL após o padrão de três soldados em suporte; PUT após três corvos em resistência.
- **Cuidado:** evitar entrar após o padrão já muito esticado — priorizar quando ele surge de um nível relevante.
- **Expiração:** 1-2 minutos.

### 11. Momentum com histograma do MACD rápido (6,13,5)
- **Indicador:** MACD ajustado para períodos curtos (6,13,5) em vez do padrão (12,26,9).
- **Entrada:** CALL quando o histograma cruza de negativo para positivo; PUT no cruzamento inverso.
- **Expiração:** 1-2 minutos.

### 12. Números redondos (níveis psicológicos)
- **Setup:** em ativos como Forex ou índices sintéticos, marcar níveis redondos (ex.: 1,1000 / 1,1050).
- **Entrada:** operar reversão quando o preço testa o nível redondo pela primeira ou segunda vez com sinal de exaustão (pavio longo, volume decrescente).
- **Expiração:** 1 minuto.

### 13. CCI (Commodity Channel Index) em extremos
- **Indicador:** CCI(14).
- **Entrada:** CALL quando CCI cruza de volta para cima após ficar abaixo de -100; PUT no espelho acima de +100.
- **Expiração:** 1-2 minutos.

### 14. Inside Bar seguida de rompimento
- **Padrão:** vela "inside bar" (contida na máxima/mínima da vela anterior) seguida de rompimento de um dos extremos.
- **Entrada:** CALL no rompimento da máxima da inside bar; PUT no rompimento da mínima.
- **Expiração:** 1-2 minutos.

### 15. Spike de tick volume
- **Indicador:** volume de ticks (disponível em MT4/MT5 e várias plataformas de OTC).
- **Entrada:** entrar na direção do rompimento quando há um pico de volume 2-3x acima da média das últimas 20 velas, combinado com fechamento de vela forte.
- **Expiração:** 1 minuto.

### 16. ADX + Parabolic SAR para scalping direcional
- **Indicador:** ADX(14) e Parabolic SAR (0,02 / 0,2).
- **Entrada:** operar apenas quando ADX > 25 (tendência confirmada); CALL quando o SAR vira para baixo do preço, PUT quando vira para cima.
- **Expiração:** 1-2 minutos.

### 17. VWAP intrabar para reversão à média
- **Indicador:** VWAP (Volume Weighted Average Price), quando disponível intraday.
- **Entrada:** CALL quando o preço se afasta 2+ desvios do VWAP para baixo e começa a reverter; PUT no espelho acima.
- **Expiração:** 1 minuto.

### 18. Doji em zona de exaustão
- **Padrão:** vela Doji após sequência de 4-5 velas na mesma direção, sinalizando indecisão.
- **Entrada:** operar reversão na direção contrária à sequência anterior, confirmando com a vela seguinte ao Doji.
- **Expiração:** 1-2 minutos.

### 19. Canal de regressão linear curto (20 períodos)
- **Indicador:** canal de regressão linear de 20 períodos em M1.
- **Entrada:** CALL no toque da banda inferior do canal com o preço ainda dentro da tendência de alta do canal; PUT no toque da banda superior em canal de baixa.
- **Expiração:** 1-2 minutos.

### 20. Volatilidade controlada em spikes de notícia (apenas ativos sintéticos/OTC)
- **Contexto:** específico para ativos sintéticos (ex.: índices de volatilidade) que não sofrem gaps de notícia real, reduzindo o risco de slippage extremo.
- **Entrada:** aguardar um movimento de spike acima do desvio padrão normal do ativo e operar a reversão à média assim que a primeira vela de correção aparecer.
- **Expiração:** 1 minuto.
- **Observação:** esta estratégia não deve ser usada em pares de Forex ou ativos reais durante notícias macroeconômicas — o risco de gap contra a posição é alto e a "expiração" de opções binárias não protege contra isso.

---

## Parte 2 — 10 estratégias adicionais para operações de até 15 minutos

Com mais tempo de expiração, é possível usar indicadores de período mais longo, aguardar confirmações estruturais e considerar múltiplos timeframes, o que tende a reduzir ruído em relação ao scalping ultracurto.

### 21. Cruzamento de médias móveis 9/21 em M5
- **Indicador:** EMA 9 e EMA 21 em gráfico de M5.
- **Entrada:** CALL no cruzamento da EMA 9 sobre a EMA 21; PUT no cruzamento inverso.
- **Expiração:** 10-15 minutos (2-3 velas de M5).

### 22. Bandas de Bollinger + RSI combinado (M5)
- **Indicadores:** Bandas de Bollinger (20,2) e RSI(14).
- **Entrada:** CALL quando o preço toca a banda inferior e o RSI está abaixo de 30; PUT no espelho com RSI acima de 70.
- **Vantagem:** dupla confirmação reduz falsos sinais em relação ao uso isolado das bandas.
- **Expiração:** 15 minutos.

### 23. Rompimento de suporte/resistência diário em M15
- **Setup:** marcar máximas e mínimas do dia anterior e da abertura da sessão atual.
- **Entrada:** CALL no rompimento confirmado (fechamento de vela de M15 acima da resistência) com retest do nível; PUT no espelho.
- **Expiração:** 15 minutos.

### 24. Tendência com ADX > 25 e pullback na EMA 20
- **Indicadores:** ADX(14) e EMA(20) em M5.
- **Entrada:** com ADX confirmando tendência, aguardar o preço recuar até a EMA 20 e retomar a direção da tendência com uma vela de força.
- **Expiração:** 15 minutos.

### 25. Canal de Keltner para reversão à média
- **Indicador:** Canal de Keltner (20, ATR x2).
- **Entrada:** CALL quando o preço rompe a banda inferior e retorna para dentro do canal; PUT no espelho.
- **Diferença em relação a Bollinger:** Keltner usa ATR em vez de desvio padrão, reagindo de forma mais suave a picos de volatilidade.
- **Expiração:** 15 minutos.

### 26. Padrão Ombro-Cabeça-Ombro (OCO) curto em M5-M15
- **Padrão gráfico:** OCO ou OCO invertido formado ao longo de 15-30 velas.
- **Entrada:** operar o rompimento da "linha de pescoço" (neckline) na direção do padrão.
- **Expiração:** 15 minutos, podendo estender conforme o alvo projetado do padrão.

### 27. Ichimoku Kinko Hyo simplificado
- **Indicador:** Ichimoku com parâmetros padrão (9,26,52) em M15.
- **Entrada:** CALL quando o preço está acima da nuvem (Kumo) e a linha Tenkan-sen cruza acima da Kijun-sen; PUT no espelho abaixo da nuvem.
- **Expiração:** 15 minutos.

### 28. Estrutura de topos e fundos (Higher Highs / Higher Lows)
- **Método:** price action puro, sem indicadores — mapear se o ativo está formando topos e fundos ascendentes (tendência de alta) ou descendentes (tendência de baixa) em M5.
- **Entrada:** CALL no rompimento do último topo em estrutura de alta; PUT no rompimento do último fundo em estrutura de baixa.
- **Expiração:** 15 minutos.

### 29. Confluência multi-timeframe (M1 / M5 / M15)
- **Método:** verificar a direção da tendência em M15, confirmar em M5 e buscar o ponto de entrada preciso em M1.
- **Entrada:** só operar quando as três referências de tempo apontam na mesma direção.
- **Vantagem:** reduz sinais contra a tendência de fundo, um dos principais motivos de perda em scalping isolado de M1.
- **Expiração:** 10-15 minutos.

### 30. Suporte e resistência dinâmica com médias móveis 50/100 (M15)
- **Indicador:** SMA 50 e SMA 100 em M15, atuando como suporte/resistência dinâmica.
- **Entrada:** CALL quando o preço testa a SMA 50 ou SMA 100 de baixo para cima em tendência de alta e reage com vela de força; PUT no espelho em tendência de baixa.
- **Expiração:** 15 minutos.

---

## Notas finais sobre gerenciamento

- **Tamanho de posição:** 1-2% da banca por operação, independentemente da estratégia.
- **Sequência de perdas:** definir um limite diário de perdas consecutivas (ex.: 3) que interrompe as operações do dia.
- **Martingale:** aumentar o valor da entrada após uma perda para "recuperar" o prejuízo é uma prática de alto risco que amplia a curva de drawdown; não é recomendada como parte de nenhuma das estratégias acima.
- **Corretora e execução:** spread, atraso de execução (latência) e a política de payoff da corretora afetam diretamente o resultado de estratégias de timeframe curto — validar isso antes de qualquer operação real.
