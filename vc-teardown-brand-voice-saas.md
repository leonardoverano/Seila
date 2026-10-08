# Teardown e plano: SaaS de conteúdo com voz própria (PT-BR)

Data da análise: 8 de outubro de 2026. Preços e números de terceiros vêm de páginas de comparação e de imprensa, não das páginas oficiais, e mudam com frequência. Onde um número não tem fonte, está marcado como **premissa**.

---

## 0. Veredito

A ideia original, "um Buffer com IA que escreve no meu jeito", não sobrevive como está. Agendamento é commodity (o Buffer entrega três canais e um assistente de IA no plano gratuito), e geração de texto com estilo próprio é o que um projeto do ChatGPT ou do Claude com um documento de estilo já faz razoavelmente bem. Quem compete nesses dois terrenos perde.

O que sobrevive é a observação de fundo: o texto de IA virou um problema real para quem posta. Em julho de 2026 o LinkedIn colocou um botão "parece lixo de IA" nos posts e aposentou a própria ferramenta de reescrita. O negócio está em fazer o texto nascer de algo que a pessoa viveu, e não de um prompt vazio.

**Reenquadramento:** um ritual diário em português. A pessoa registra em 30 segundos o que aconteceu no dia (áudio ou texto), e na hora combinada chega um rascunho na voz dela, adaptado a cada rede. O sistema só gera quando existe matéria-prima real, e aprende com cada edição que a pessoa faz. O app não agenda nem publica.

**Classificação honesta:** SaaS bootstrapped de porte pequeno a médio. Com 2.000 pagantes no Brasil, o faturamento fica perto de R$ 2,5 milhões por ano. Não é um negócio de capital de risco, a menos que a camada de voz e avaliação vire infraestrutura vendida a terceiros (questão para o ano 3).

**Próxima ação:** o teste concierge da seção 6, que custa tempo e quase nenhum dinheiro. **Critério de parada principal:** se, em teste cego, os rascunhos do sistema não superarem em pelo menos 20 pontos percentuais a aprovação de um projeto comum do ChatGPT ou Claude com documento de estilo, até 31 de dezembro de 2026, o produto não tem diferencial. Parar ou reformular.

---

## 1. Realidade do mercado

### Onde está a atividade

| Segmento | O que usa hoje | Quem paga | O que falta |
|---|---|---|---|
| Criador ou profissional com marca pessoal | Notas no celular, ChatGPT/Claude, às vezes Buffer ou Typefully | Ele mesmo, com pouca disposição | Texto que pareça dele e um motivo para escrever todo dia |
| Freelancer de social media | mLabs, Etus, Canva, planilha, ChatGPT | O próprio freelancer, com o custo repassado ao cliente | Manter 3 a 10 vozes distintas sem misturar, e aprovação do cliente |
| Agência pequena | Mesmas ferramentas, mais Trello/Notion | A agência | Padronizar a qualidade do texto entre redatores |
| Empresa com time interno | Suite de gestão (Sked, Hootsuite) | Departamento de marketing | Fora do alcance de um produto bootstrapped |

A assimetria que importa: o dinheiro por usuário está nos dois segmentos do meio (quem gerencia várias vozes), e a dor mais aguda está no primeiro (quem escreve sobre si mesmo e se incomoda com texto genérico). A estratégia precisa servir os dois com planos diferentes.

### Mapa competitivo

| Concorrente | Posição | Preço (fonte de terceiros) |
|---|---|---|
| Buffer | Agendamento. Plano gratuito com 3 canais e assistente de IA incluído.[^buffer] | Pago a partir de cerca de US$ 5 por canal ao mês (anual)[^buffer] |
| Ocoya | Agendamento mais geração por créditos. 7 dias de teste, sem plano gratuito.[^ocoya] | US$ 15 a US$ 159 ao mês[^ocoya] |
| Typefully / Hypefury | Escrita e automação focadas em X, com IA nos planos de cima.[^tf] | Entre US$ 12,50 e US$ 65 ao mês, dependendo da fonte[^tf] |
| Postiz | Agendador open source, lançado em 2024, solo founder, licença AGPL-3.0. Cloud a partir de US$ 29.[^postiz] | US$ 29 ao mês no cloud, grátis se hospedado por conta própria |
| Sked | Já tem "Brand Kit" com atributos de voz, posts de exemplo e lista de proibições.[^sked] | Voltado a agências |
| mLabs, Etus | Agendadores brasileiros, em reais, com IA para legendas.[^mlabs] | Por número de contas (não encontrei valores) |
| Jasper | Voz de marca para times, com reclamações de texto genérico e de cobrança.[^jasper] | A partir de US$ 39 ao mês (anual) |
| ChatGPT / Claude com projeto e documento de estilo | Substituto gratuito ou de baixo custo | Assinatura que a pessoa já paga |

Dois fatos pesam mais do que o resto. Primeiro, "voz de marca" já existe dentro de agendadores (Sked). Segundo, o substituto mais forte não é nenhuma dessas empresas, e sim a pessoa abrir o próprio ChatGPT ou Claude.

### Evidência de que a dor existe

- O LinkedIn adicionou em julho de 2026 uma opção "Seems like AI slop" no menu dos posts e comentários, e usa esse sinal para decidir o alcance fora da rede do autor. No mesmo período aposentou seu recurso de melhoria de post com IA.[^lislop1]
- O LinkedIn diz que conteúdo classificado como slop recebe cerca de 40% menos visualizações do que algumas semanas antes. O número é da própria empresa e não tem metodologia pública.[^lislop2]
- Um estudo da Pangram Labs estimou que mais de 40% dos posts longos do LinkedIn têm texto de máquina. O dado vem de um detector, portanto é estimativa.[^lislop2]

O que **não** encontrei: nenhum estudo independente mostrando queda sustentada de engajamento por causa de texto de IA. A dor existe como percepção e como política de plataforma, e o efeito sobre resultado ainda é difuso.

---

## 2. Teardown

**C1. A observação de que o agendamento é secundário está certa, e o mercado já deu essa parte de graça.**
O Buffer oferece três canais com assistente de IA sem custo.[^buffer] O Ocoya cobra a partir de US$ 15 e o Typefully, a partir de US$ 12,50.[^ocoya][^tf] Agendar ou gerar texto genérico não sustenta uma assinatura.
→ **Mudança:** agendamento e publicação saem da proposta de valor. O produto fica a montante de qualquer agendador, e a saída do app deve ser fácil de levar para o que a pessoa já usa.

**C2. Largar as APIs de publicação reduziu muito o custo de construir, e aproximou o produto do substituto mais difícil de bater.**
Sem publicar, o app vira um gerador de texto com notificação. O concorrente real passa a ser um projeto do ChatGPT ou do Claude com o documento de estilo da pessoa, mais um lembrete no celular. Isso funciona para quem tem paciência de manter o documento.
→ **Mudança:** o teste de existência é a comparação cega com essa linha de base (seção 6). O produto precisa entregar o que o ChatGPT sozinho não entrega: banco de matéria-prima, memória do que já foi dito, nota de qualidade e aprendizado com as edições.

**C3. A tese de que o texto genérico incomoda é verdadeira e está datada de agora, mas a plataforma que mais pune é a mesma que você quer abastecer.**
O LinkedIn aposentou a própria ferramenta de IA e passou a reduzir alcance de conteúdo marcado como slop.[^lislop1][^lislop2] Isso valida a dor e cria um risco: texto detectável como de IA pode ser rebaixado, mesmo bem escrito.
→ **Mudança:** o produto não promete "texto indetectável". Promete texto que parte de algo vivido e declarado pela pessoa. A exigência de matéria-prima (C4) é ao mesmo tempo a defesa de qualidade e a defesa contra a política das plataformas.

**C4. Gerar todo dia sem a pessoa pedir é o recurso que mais vende e o que mais produz slop.**
Uma rotina diária sem insumo novo inventa assunto. A promessa de automação contradiz a promessa de qualidade, e é nesse ponto que o produto pode se diferenciar dos concorrentes de créditos, que ganham mais quanto mais a pessoa gera.
→ **Mudança:** a rotina vira uma "rotina de pauta". Às 8h o app pede um áudio de 30 segundos ou um tópico, e às 19h entrega o rascunho. Sem insumo, o sistema avisa que hoje não há post e não inventa nada. Isso é uma diferença de modelo de negócio e não só de prompt.

**C5. A disposição de pagar de quem escreve sobre si mesmo é baixa, e o benchmark gringo já está em US$ 12 a US$ 20.**
Typefully e Ocoya mostram o teto percebido para criadores individuais.[^tf][^ocoya] Em reais, o ponto razoável fica entre R$ 49 e R$ 99, e quem paga é a própria pessoa, sem orçamento de empresa. Resenhas do Jasper mostram que quem paga mais caro e recebe texto genérico reclama de preço e de cobrança.[^jasper]
→ **Mudança:** o plano para quem gerencia várias vozes (freelancer e agência) vira a principal linha de receita. O valor para esse comprador é medido em horas economizadas por cliente e em rodadas de aprovação a menos.

**C6. O ritual diário é um bom mecanismo de retenção, e quebra no dia em que a pessoa pula três avisos seguidos.**
Sem publicação automática, o último passo (copiar, colar, postar) depende da disciplina do usuário. Quem some deixa de abrir o rascunho, mas o custo de geração continua.
→ **Mudança:** pausa automática da rotina após 5 dias sem abrir, resumo semanal por e-mail para reativar, e custo por usuário inativo limitado a zero.

**C7. Onze redes sociais são onze formatos, onze conjuntos de limites e onze maneiras de dar errado.**
Slack, Discord, Telegram e Pinterest não são onde marca pessoal gera receita para o usuário. Cada rede acrescenta regras de tamanho, de imagem e de linguagem que precisam de teste.
→ **Mudança:** MVP com LinkedIn, X e Threads, mais legenda de Instagram como texto. As demais entram quando houver pedido de pagantes. A análise de vídeo e a estruturação de perfil (bio, banner) ficam para a v2, porque são um produto de custo e de frequência diferentes: a pessoa estrutura o perfil uma vez, e isso não gera uso recorrente.

**C8. Colocar a voz como diferencial é correto, e prompt mais interface é exatamente o que os modelos absorvem.**
Voz de marca já aparece em agendadores como o Sked.[^sked] Modelos melhoram e ficam mais baratos a cada trimestre, e o recurso de memória e estilo dos assistentes gerais avança. Um prompt bem escrito se copia em uma tarde.
→ **Mudança:** o valor migra para o que acumula com o uso: o conjunto de avaliação (briefings e o que a pessoa aprova), o histórico de edições antes e depois, o catálogo de vícios de IA em português e o banco de matéria-prima. Isso fica no produto quando o modelo muda.

**C9. Você não depende de APIs de redes sociais, e passou a depender de duas coisas menos visíveis.**
Uma é o preço e a disponibilidade do fornecedor de modelo. A outra é a política das plataformas sobre conteúdo gerado por IA, que mudou em semanas no LinkedIn.[^lislop1]
→ **Mudança:** camada de modelo trocável por configuração, rótulo opcional de "escrito com IA" por rede, e item específico no registro de riscos para mudança de política.

**C10. Ser o primeiro usuário é a melhor credencial e deixa em aberto a pergunta de distribuição.**
Você conhece o problema por usá-lo e vai medir a qualidade por conta própria. Mas nenhum canal de aquisição foi definido, e o público brasileiro de criadores e freelancers não se alcança com anúncio nesse ticket.
→ **Mudança:** distribuição concedida (curso, mentoria ou comunidade que recomenda a ferramenta), uma ferramenta gratuita de detecção de vícios de IA em português como atrativo, e 10 parceiros de design antes de abrir cadastro.

**C11. Guardar texto pessoal e profissional dos usuários cria responsabilidades que o plano ainda não mencionava.**
LGPD (dados, direito de exclusão, bases legais), direitos autorais do material importado, e conteúdo que o sistema gere com alegações problemáticas. Para profissões reguladas (advocacia, medicina), existem regras de publicidade dos conselhos profissionais que precisam de verificação, e as regras de identificação de publicidade do CONAR para influenciadores.
→ **Mudança:** política de não treinar modelos com dados dos clientes (também argumento de venda), exclusão completa em um clique, aviso de publicidade nos rascunhos que citem marca ou produto, e consulta jurídica antes de atender profissões reguladas.

**C12. A conta fecha como negócio sustentável e não como negócio de escala.**
Com o mix de planos abaixo, 500 pagantes geram cerca de R$ 636 mil por ano, e 2.000 geram cerca de R$ 2,5 milhões.
→ **Mudança:** estratégia de financiamento por receita própria, sem captar. Detalhes na seção 5.

**Tese que sobrevive:** *A percepção de que o texto de IA virou um problema é real, e o LinkedIn confirmou isso em julho de 2026. Um agendador com prompts melhores é a forma errada de explorar isso, porque Buffer, Typefully e o próprio ChatGPT já cobrem esse espaço a custo zero ou quase. O negócio é o ritual diário em português, que parte da matéria-prima da pessoa, só gera quando há algo real a dizer e aprende com cada edição, vendido primeiro a quem precisa manter várias vozes sem misturá-las.*

---

## 3. Estratégia revisada

**Posicionamento, em uma frase que você pode dizer em voz alta:**
*Você conta em 30 segundos o que aconteceu hoje, e às 19h chega o post pronto, na sua voz, ou o aviso de que hoje não há nada de seu para publicar.*

### O produto em camadas

| Camada | O que é | Por quê |
|---|---|---|
| Cunha (paga) | Rotina de pauta, rascunho por rede, nota de qualidade, aviso de entrega | Resolve a dor de escrever sem cair em texto genérico |
| Retenção (gera os dados) | Banco de matéria-prima, histórico de edições, perfil de voz editável | Quanto mais a pessoa usa, melhor o perfil e mais difícil sair |
| Aquisição (gratuita) | Detector de vícios de IA em português (cole um texto, veja os padrões) e perfil de voz de amostra | Atrai quem já sente o problema, sem custo por usuário |

### Por que é defensável, em ordem de quando passa a valer

1. **No lançamento:** foco, velocidade e relação direta com os primeiros usuários. É real e temporário.
2. **Meses 3 a 9:** o perfil de voz e o histórico de uma pessoa ou de um cliente de agência vivem dentro do produto. Trocar de ferramenta significa recomeçar o aprendizado, e para a agência, refazer as vozes de todos os clientes.
3. **Ano 2:** o conjunto de avaliação em português, com milhares de casos de "isto soa como a pessoa" e "isto soa como IA", e o catálogo de vícios. Um concorrente copia o prompt em uma tarde e não consegue copiar dois anos de aprovações e correções.
4. **Incompatibilidade de modelo de negócio:** concorrentes que cobram por crédito de geração ganham quando a pessoa gera mais. Um produto que se recusa a gerar sem matéria-prima corre contra essa métrica, e essa recusa é difícil de imitar sem mudar o preço.

### Extensão internacional

Projetar agora: idioma como atributo do perfil de voz, catálogo de vícios separado por idioma, moeda e imposto fora do núcleo. Construir depois: inglês e espanhol. O mercado em inglês é o mais disputado (Buffer, Typefully, Hypefury, Sked), então a entrada lá só faz sentido com a base brasileira já pagando.

### O que não estamos fazendo

Agendar e publicar, analytics de desempenho, onze redes, análise de vídeo e estruturação de perfil no MVP, geração de imagem por modelo, integração com APIs de redes sociais.

---

## 4. Stakeholders e casos de uso

### Criador ou profissional com marca pessoal

- **[MVP]** Importar posts anteriores e ver o perfil de voz resultante, com edição manual.
- **[MVP]** Registrar matéria-prima por áudio ou texto, a qualquer hora.
- **[MVP]** Caixa de entrada de rascunhos com cópia em um toque e abertura da rede.
- **[MVP]** Rotina de pauta com aviso por e-mail e Telegram.
- **[v1.1]** Resumo semanal do que foi aprovado, editado e descartado.
- **[v1.1]** Templates de imagem com a marca da pessoa e texto sobreposto.
- **[v2]** Aviso por WhatsApp (custo por mensagem, plano mais alto).

### Freelancer de social media e agência

- **[MVP]** Vários perfis de voz por conta, cada um isolado dos outros.
- **[v1.1]** Link de aprovação para o cliente final, sem login.
- **[v1.1]** Exportação em CSV no formato de importação em massa dos agendadores que o profissional já usa (a viabilidade em cada ferramenta precisa ser verificada).
- **[v2]** Painel por cliente com consumo e histórico.

### Administrador da plataforma (você)

- **[MVP]** Painel de custo por usuário e por rotina, com bloqueio ao atingir o limite do plano.
- **[MVP]** Catálogo de vícios de IA em português, com revisão semanal.
- **[v1.1]** Revisão de amostras de rascunhos reprovados pelos usuários para melhorar o crítico.
- **[v1.1]** Fluxo de exclusão de dados (LGPD) e registro de pedidos.

---

## 5. Modelo de negócio

### Linhas de receita, em ordem de quando ligam

| # | Linha | Quem paga | Preço (premissa) | Quando |
|---|---|---|---|---|
| 1 | Plano Solo | Criador individual | R$ 59 por mês | Lançamento |
| 2 | Plano Pro | Criador com várias redes e rotinas | R$ 119 por mês | Lançamento |
| 3 | Plano Agência | Freelancer ou agência, 5 vozes | R$ 349 por mês | Lançamento |
| 4 | Voz adicional | Agência | R$ 59 por voz | Mês 6 |
| 5 | Aviso por WhatsApp | Planos Pro e Agência | Repasse do custo mais margem | Mês 9 |
| 6 | API de voz e avaliação para terceiros | Outras ferramentas | A definir | Ano 3 ou depois |

A linha 6 não deve ser mencionada a ninguém como produto, porque depende de um conjunto de avaliação que ainda não existe.

### Limites por plano (premissa)

| | Solo | Pro | Agência |
|---|---|---|---|
| Vozes | 1 | 1 | 5 |
| Rotinas ativas | 1 | 3 | 10 |
| Gerações por mês (uma versão para uma rede) | 40 | 150 | 500 |

### Economia por usuário, com a aritmética

Premissas: câmbio de R$ 5,50 por dólar; custo de modelo de US$ 0,04 por geração, considerando rascunho, nota do crítico e uma reescrita em parte dos casos, com o perfil de voz em cache. Esse valor é a premissa mais importante e deve ser medido na fase 0. Imposto de 8% sobre faturamento (premissa, depende do enquadramento tributário), taxa de pagamento de 4% e infraestrutura de R$ 3 por usuário, R$ 10 na agência.

Custo por geração: US$ 0,04 × 5,50 = **R$ 0,22**.

| Plano | Receita | Imposto 8% | Pagamento 4% | Infra | Modelo no limite do plano | Margem de contribuição | % |
|---|---|---|---|---|---|---|---|
| Solo | 59,00 | 4,72 | 2,36 | 3,00 | 40 × 0,22 = 8,80 | **40,12** | 68% |
| Pro | 119,00 | 9,52 | 4,76 | 3,00 | 150 × 0,22 = 33,00 | **68,72** | 58% |
| Agência | 349,00 | 27,92 | 13,96 | 10,00 | 500 × 0,22 = 110,00 | **187,12** | 54% |

Com uso médio de 60% do limite, as margens sobem para cerca de 72% (Solo), 69% (Pro) e 66% (Agência).

**Mix assumido:** 60% Solo, 30% Pro, 10% Agência.
Receita média por pagante: 0,6 × 59 + 0,3 × 119 + 0,1 × 349 = 35,40 + 35,70 + 34,90 = **R$ 106,00 por mês**.
Margem de contribuição média: 0,6 × 40,12 + 0,3 × 68,72 + 0,1 × 187,12 = 24,07 + 20,62 + 18,71 = **R$ 63,40 por mês**.

### Receita por escala

| Pagantes | Receita mensal | Receita anual | Equivalente em dólar |
|---|---|---|---|
| 200 | R$ 21.200 | R$ 254.400 | cerca de US$ 46 mil |
| 500 | R$ 53.000 | R$ 636.000 | cerca de US$ 116 mil |
| 2.000 | R$ 212.000 | R$ 2.544.000 | cerca de US$ 463 mil |

**Ponto de equilíbrio.** Se você quer cobrir R$ 10.000 de retirada mais R$ 4.000 de custos fixos (ferramentas, domínio, contabilidade, suporte), precisa de R$ 14.000 de margem de contribuição por mês: 14.000 ÷ 63,40 = **221 pagantes**.

### CAC, retenção e LTV

- **CAC:** nos primeiros 12 meses é tempo seu, e não dinheiro. Premissa de R$ 150 a R$ 250 por pagante em horas de conversa, conteúdo e suporte.
- **Retenção:** premissa de 6% de cancelamento mensal, comum em ferramentas de criador e SMB (não encontrei dado brasileiro). Vida média: 1 ÷ 0,06 ≈ 16,7 meses.
- **LTV de contribuição:** 63,40 × 16,7 ≈ **R$ 1.058**.
- **Teto de CAC para uma relação LTV/CAC de 3:** cerca de R$ 350. Isso deixa pouco espaço para anúncios pagos, que só devem ser testados com orçamento pequeno e depois que a retenção medida confirmar a premissa.
- **Retorno do CAC:** R$ 200 ÷ 63,40 ≈ 3,2 meses.

### Veredito de escala

Este é um **SaaS bootstrapped com potencial de negócio individual sólido**: 221 pagantes cobrem uma retirada modesta, e 2.000 pagantes formam uma empresa de R$ 2,5 milhões por ano. Para chegar a escala de capital de risco, seria preciso que a camada de voz e avaliação se tornasse infraestrutura usada por outras ferramentas, ou que o produto fosse bem em inglês, onde a concorrência é maior. Nenhuma das duas hipóteses pode ser sustentada hoje.

---

## 6. Escopo do MVP e plano técnico

### Dentro do escopo

1. Importação de 20 a 50 posts anteriores e extração do perfil de voz (editável).
2. Banco de matéria-prima com captura por texto e áudio (com transcrição).
3. Pipeline de geração: rascunho, nota do crítico contra o perfil e contra o catálogo de vícios, reescrita quando a nota ficar abaixo do limite.
4. Versões para LinkedIn, X e Threads; legenda de Instagram como texto.
5. Caixa de entrada com copiar, editar e marcar como postado.
6. Rotina de pauta (pedido de insumo, geração antecipada, aviso na hora combinada), com e-mail e Telegram.
7. Registro de toda edição (antes e depois) desde o primeiro dia.
8. Limites por plano, pausa automática e painel de custo.

### Fora do escopo, com motivo

| Item | Motivo |
|---|---|
| Publicação por API | Decisão já tomada; reduz custo e prazo |
| Onze redes | Cada rede multiplica testes e formatos |
| Análise de vídeo | Produto diferente, custo maior |
| Estruturação de perfil e banner | Uso único, sem recorrência |
| Imagem gerada por modelo | Custo e aspecto de IA; templates entram na v1.1 |
| Analytics | Sem acesso às métricas das redes |
| WhatsApp | Custo por mensagem; entra quando houver pagantes |

### O teste mais barato

**Concierge de 3 semanas, com 10 pessoas.** Recrute 10 criadores ou freelancers de língua portuguesa. Para cada um, reúna 20 posts anteriores e monte o perfil de voz à mão (num projeto do Claude). Durante 3 semanas, peça o insumo do dia por Telegram e devolva o rascunho às 19h, também manualmente.

Meça: percentual de rascunhos aprovados sem edição, percentual copiado para postar, quantos continuam respondendo na terceira semana. Faça em paralelo a comparação cega de 40 briefings com a linha de base do ChatGPT/Claude com documento de estilo, e inclua textos reais das próprias pessoas como controle.

**Não construir até que isto passe:** contas de usuário, cobrança, infraestrutura de rotinas, mais de uma rede, templates de imagem, qualquer coisa de vídeo.

### Stack

| Camada | Escolha | Motivo |
|---|---|---|
| Aplicação | Next.js com TypeScript, Tailwind e shadcn/ui | Combina com o fluxo de trabalho no Claude Code |
| Banco | Postgres (Supabase ou Neon) com pgvector | Perfis de voz e exemplos para recuperação |
| Filas e rotinas | Inngest ou Trigger.dev | Execução agendada, tentativas e registro de falhas |
| Modelo | API da Anthropic, com cache de prompt para o perfil de voz | O perfil é longo e repetido; o cache reduz o custo |
| Transcrição | Serviço de fala para texto | Captura por áudio |
| Aviso | Telegram Bot API e e-mail (Resend) | Baixo custo, entrega imediata |
| Cobrança | Asaas ou Stripe | Verificar Pix recorrente |
| Qualidade | Playwright (fluxos e capturas), conjunto de avaliação próprio | Regressão visual e de texto |

### Decisões difíceis de reverter

- **Modelo de dados com workspace, vozes e rascunhos separados desde o início.** A agência precisa de várias vozes por conta, e adaptar isso depois é migração.
- **Armazenar todas as versões e edições.** Se esse histórico não for guardado desde o dia 1, o ativo mais valioso do produto não existe.
- **Idioma como atributo da voz, não como configuração global.**

### Modelo de dados (resumido)

`users` · `workspaces` · `voice_profiles` (versionado) · `voice_samples` · `raw_materials` · `routines` · `runs` · `drafts` (rede, nota, status) · `draft_edits` (antes/depois) · `slop_rules` (por idioma) · `usage_ledger` (custo por geração)

### Sequência de construção

| Semana | Entrega | Observação |
|---|---|---|
| 1 | PRD, conjunto de 40 briefings, catálogo de vícios v1, abertura de CNPJ/conta de cobrança e domínio | Itens com prazo longo começam aqui |
| 2 a 3 | Extração de voz e pipeline em linha de comando, comparação cega | Maior risco do projeto vem primeiro |
| 4 a 6 | Concierge com 10 pessoas via Telegram | Decide se continua |
| 7 a 8 | Caixa de entrada e banco de matéria-prima, com direção visual definida | Design entra aqui |
| 9 a 10 | Rotinas, despachante, aviso, barreira de qualidade, pausa automática | Só se o concierge passar |
| 11 a 12 | Cobrança, limites, onboarding, exclusão de dados | |
| 13 a 16 | Beta fechado com 30 pessoas, ajustes de preço e de limites | |

---

## 7. Go to market

### Escolha do beachhead

Critérios com peso: quem você já conhece e alcança (maior peso), dor com texto genérico, presença no LinkedIn/X/Threads, disposição de pagar, e facilidade de atender sem profissão regulada.

O candidato mais forte é **profissionais autônomos e criadores de conteúdo de negócios e tecnologia que escrevem sobre o próprio trabalho**, atendidos por você e pelos primeiros parceiros. O segundo é o **freelancer de social media** que já paga por ferramentas. Advogados e médicos ficam para depois da checagem das regras de publicidade de cada conselho.

### Motor principal de aquisição

1. Você usa o produto no seu próprio conteúdo e deixa isso visível, com exemplos reais de antes e depois.
2. Convide 10 parceiros de design do seu círculo e rode o concierge.
3. Publique o resultado do teste cego (percentual de aprovação sem edição) em formato aberto.
4. Lance a ferramenta gratuita de detecção de vícios de IA em português, com chamada para o perfil de voz.
5. Feche acordo com um curso, mentoria ou comunidade de marca pessoal para recomendar ou incluir a ferramenta (distribuição concedida).
6. Abra para os primeiros 30 pagantes com preço de fundador.

### Canais, por valor esperado

| Canal | Expectativa | Observação |
|---|---|---|
| Uso público do próprio produto | Alta | Barato, e é prova |
| Parceiros de design e indicação | Alta | Qualidade do primeiro cliente |
| Curso, mentoria ou comunidade parceira | Alta se fechar | Depende de relacionamento |
| Ferramenta gratuita de detecção | Média | Atrai curiosos; mede-se conversão |
| Conteúdo e SEO em português | Média, lenta | Retorno no ano 2 |
| Anúncios pagos | Baixa no início | Teto de CAC apertado (seção 5) |
| Lançamento em Product Hunt em inglês | Baixa | Fora do beachhead |
| Mensagens frias | Baixa | Ruído e custo de tempo |

### Retenção

O motivo semanal para abrir o app é o aviso da rotina. O mecanismo de longo prazo é o perfil de voz, que melhora a cada edição, e o histórico de matéria-prima, que a pessoa passa a consultar como diário profissional.

### Fases

| Fase | Período | Métrica de sucesso |
|---|---|---|
| 0. Teste de voz | Out a dez 2026 | Superar a linha de base em 20 pontos |
| 1. Concierge | Nov a dez 2026 | 7 de 10 ativos na terceira semana |
| 2. Produto básico | Jan a mar 2027 | 30 beta ativos |
| 3. Primeiros pagantes | Abr a jun 2027 | 40 pagantes em julho |
| 4. Agência | Jul a dez 2027 | 8 contas de agência pagando |
| 5. Escala orgânica | 2028 | 221 pagantes (equilíbrio) |

---

## 8. Métricas, riscos e critérios de parada

### Métrica principal

**Rascunhos copiados para postar por usuário ativo por semana.** Mede uso real e não cadastro.

### Métricas de apoio

- Percentual de rascunhos aprovados sem edição (qualidade da voz).
- Tempo entre o aviso e a cópia.
- Taxa de dias com matéria-prima registrada (saúde da rotina).
- Retenção na semana 4 e no mês 3.
- Custo de modelo por usuário ativo.
- Taxa de pausa automática.

### Registro de riscos

| Risco | Gravidade | Mitigação |
|---|---|---|
| A voz não supera a linha de base do ChatGPT/Claude | Alta | Teste cego na fase 0; parar se não passar |
| Plataforma rebaixa texto de IA (política já vigente no LinkedIn) | Alta | Matéria-prima real, rótulo opcional, não prometer indetectabilidade |
| Custo de modelo acima da premissa | Média | Medir na fase 0; cache de prompt; limites por plano |
| Usuário inativo gerando custo | Média | Pausa automática |
| Fornecedor de modelo muda preço ou política | Média | Camada trocável por configuração |
| Dado pessoal vazado ou mal usado | Alta | Isolamento por workspace, exclusão total, sem treino com dados de clientes |
| Texto com alegação indevida (saúde, finanças, publicidade) | Média | Aviso de publicidade, regras por perfil, revisão humana por padrão |
| Você como único desenvolvedor e suporte | Alta | Escopo mínimo, suporte por Telegram em horário fixo, automatizar o onboarding |
| Preço de criador individual baixo demais | Média | Concentrar receita no plano Agência e testar preço no beta |
| Concorrente grande lança voz de marca em português | Média | Acúmulo de avaliação e edições, foco em agência pequena |

### Critérios de parada (acordados antes de gastar)

1. **Até 31 de dezembro de 2026:** se o sistema não superar a linha de base em 20 pontos percentuais de aprovação sem edição no teste cego, o produto não tem diferencial. Parar ou reformular a tese.
2. **Até 31 de março de 2027:** se menos de metade dos 30 parceiros do beta abrir os rascunhos em 4 dias ou mais por semana na quarta semana de uso, o ritual diário não se sustenta. Parar de construir rotinas.
3. **Até 31 de julho de 2027:** se houver menos de 40 pagantes a R$ 59 ou mais, esse segmento não paga o suficiente por isso. Encerrar ou manter como projeto próprio, sem investimento adicional.

---

## 9. Perguntas em aberto

Ordenadas por quanto mudam o plano.

1. **Quem é o primeiro público pagante?** Criador individual ou freelancer/agência? Muda o preço, o produto e o canal.
2. **Qual é o tamanho e a natureza da sua audiência hoje?** Ela define se o motor de aquisição da seção 7 funciona sem curso ou comunidade parceira.
3. **Quanto tempo por semana você tem, junto com outras atividades?** O plano supõe dedicação regular; com menos de 15 horas por semana, o cronograma dobra.
4. **Você aceita um produto que se recusa a gerar em dias sem matéria-prima?** É o diferencial, e também o que mais atrito causa com quem espera automação total.
5. **Pretende atender profissões reguladas (advocacia, medicina)?** Exige verificação jurídica antes.
6. **O exigido de qualidade para o piloto automático** (publicação sem revisão humana) fica de fora do MVP. Você concorda em tratar rascunho e aprovação rápida como únicos modos até haver dados?

---

## Apêndice: a ideia original, mapeada

| Elemento original | Veredito | Onde ficou |
|---|---|---|
| Plataforma para agendar, automatizar e analisar mídias | **Cortado** | Buffer e Typefully cobrem o agendamento; sem API, não há analytics |
| Postagem automática | **Cortado** (decisão sua) | Substituída por entrega de rascunho e abertura da rede |
| Brand Voice, "meu jeito de falar" | **Mantido, é o núcleo** | Perfil de voz editável, avaliação cega, edições registradas |
| Sem AI slop | **Mantido, é a tese** | Catálogo de vícios, barreira de qualidade, exigência de matéria-prima |
| Geração agendada por dia | **Mantido, redefinido** | Rotina de pauta: pede insumo e só gera com material real |
| Foco em design | **Mantido** | Direção visual definida na semana 7 e templates de imagem na v1.1 |
| Onze redes | **Reduzido a 3 mais Instagram em texto** | Demais redes por demanda |
| Vídeo, descrição e estruturação de perfil | **Adiado para a v2** | Uso único e custo diferente |
| Vários planos | **Mantido** | Solo, Pro e Agência, com limites de uso |
| Primeiro uso só seu, depois produto | **Mantido** | Fase 0 e concierge |
| Brasil primeiro | **Mantido** | Português como vantagem de nicho; idioma como atributo desde o início |
| Programar com Claude Code | **Mantido** | Sequência da seção 6 |

---

## Fontes

[^buffer]: [Buffer Pricing, August 2026: What Per-Channel Billing Actually Costs (NapoleonCat)](https://napoleoncat.com/blog/buffer-pricing/) e [Buffer Pricing Breakdown (SocialBu)](https://socialbu.com/blog/buffer-pricing). As fontes discordam em parte dos valores; conferir na página oficial.
[^ocoya]: [Ocoya pricing (Toolradar)](https://toolradar.com/tools/ocoya/pricing). Dados de terceiros, verificados em agosto de 2026.
[^tf]: [Hypefury vs Typefully 2026 (We Are Founders)](https://www.wearefounders.uk/hypefury-vs-typefully-2026-which-x-tool-is-worth-paying-for/). Preços e recursos de voz divergem entre comparativos, vários escritos por concorrentes.
[^postiz]: [Postiz vs concorrentes (AdaptlyPost)](https://adaptlypost.com/vs/postiz). Dados de comparativo, não da página oficial.
[^sked]: [The 2026 brand voice playbook (Sked)](https://skedsocial.com/resources/brand-voice-ebook.md). Material da própria empresa.
[^mlabs]: [Melhores ferramentas de redes sociais (Guia Ferramentas Digitais)](https://guiaferramentasdigitais.com.br/guias/melhores-ferramentas-redes-sociais/) e [mLabs: agendamento de posts](https://www.mlabs.com.br/blog/agendamento-de-posts). Valores de plano não localizados.
[^jasper]: [Jasper reviews (Capterra)](https://www.capterra.com/p/217242/Jasper//reviews/) e [Jasper review (WPShout)](https://wpshout.com/jasper-ai-review/).
[^lislop1]: [LinkedIn says 1M people have reported AI slop (Social Media Today)](https://socialmediatoday.com/news/linkedin-says-1m-people-have-reported-ai-slop/828465) e [LinkedIn AI slop button (DSMN8)](https://dsmn8.com/blog/linkedin-ai-slop-button/).
[^lislop2]: [LinkedIn's AI Slop Crisis (WebProNews)](https://www.webpronews.com/linkedins-ai-slop-crisis-new-data-shows-over-40-of-long-posts-machine-written-as-platform-fights-back/). Os 40% de menos visualizações são dados da própria empresa; o percentual de posts longos de máquina vem de um detector de IA.
