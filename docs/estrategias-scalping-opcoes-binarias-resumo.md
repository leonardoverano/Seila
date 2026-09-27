# Resumo — Estratégias de Scalping para Opções Binárias

Este arquivo resume o que está no documento detalhado (`estrategias-scalping-opcoes-binarias-detalhado.md`).

## O que foi entregue

- **20 estratégias** para operações ultracurtas, de 10 segundos a 1 minuto de expiração.
- **10 estratégias adicionais** para operações de até 15 minutos, totalizando 30.
- Cada estratégia traz: indicador ou padrão usado, regra de entrada (CALL/PUT), filtro de confirmação quando aplicável, e tempo de expiração sugerido.

## Lógica geral por grupo

**Grupo 1 (10s a 1min):** foca em micro-reversões e rompimentos de curtíssimo prazo — bandas de Bollinger, cruzamento de médias rápidas, osciladores (RSI, Estocástico, CCI) em zonas extremas, e padrões de vela (pin bar, engolfo, doji, inside bar) sobre níveis de suporte/resistência recém-formados. Nesse timeframe o ruído é dominante, então a maioria das estratégias exige um filtro de confirmação (segunda vela, volume, contexto de tendência) antes de entrar.

**Grupo 2 (até 15min):** usa indicadores de período mais longo (EMA 9/21, ADX, Ichimoku, Keltner), padrões gráficos estruturais (OCO, topos e fundos) e a técnica de confluência entre M1/M5/M15. Tende a gerar sinais mais confiáveis por ter mais dados de preço para confirmar o movimento antes da entrada.

## Pontos de atenção

- Nenhuma estratégia tem taxa de acerto garantida; o payoff assimétrico das opções binárias exige acerto consistente acima de 55-60% só para não perder dinheiro no longo prazo.
- Timeframes de 10s a 1min sofrem mais com spread, atraso de execução e ruído — trate como a faixa de maior risco entre as 30 estratégias.
- Gerenciamento de risco (1-2% da banca por operação, limite de perdas consecutivas, sem martingale) é tratado no documento como parte obrigatória de qualquer uma dessas estratégias, não como recomendação separada.

## Arquivos gerados

1. `docs/estrategias-scalping-opcoes-binarias-detalhado.md` — versão completa com as 30 estratégias.
2. `docs/estrategias-scalping-opcoes-binarias-resumo.md` — este resumo.
