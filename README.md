# Jarvis

Agente de IA de linha de comando, em português, com personalidade inspirada no J.A.R.V.I.S. Usa a API da Anthropic com tool use.

## Uso

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
export JARVIS_USUARIO="Bernardo"   # como ele vai te chamar (padrão: "senhor")
python jarvis.py
```

## O que ele faz

| Ferramenta | Efeito | Confirmação |
|---|---|---|
| `data_hora` | Data e hora do sistema | não |
| `listar_diretorio`, `ler_arquivo` | Leitura dentro do diretório de trabalho | não |
| `escrever_arquivo` | Cria ou sobrescreve arquivos | sim |
| `executar_comando` | Roda comando de shell (timeout de 60 s) | sim |
| `lembrar`, `esquecer` | Memória persistente em `~/.jarvis/memoria.json`, injetada no prompt a cada turno | não |

Arquivos ficam restritos a `JARVIS_RAIZ` (padrão: diretório atual). O comando de shell não tem essa restrição além do `cwd`; por isso exige confirmação.

## Configuração

Variáveis: `JARVIS_USUARIO`, `JARVIS_MODELO`, `JARVIS_RAIZ`, `JARVIS_MEMORIA`. A persona está na constante `PERSONA` em `jarvis.py`.

## Extensão

Para adicionar uma ferramenta: inclua o schema em `FERRAMENTAS` e um ramo em `executar_ferramenta`. Candidatos naturais: busca na web, agenda, e-mail, voz (STT/TTS).
