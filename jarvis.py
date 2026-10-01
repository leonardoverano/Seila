#!/usr/bin/env python3
"""Jarvis: assistente de linha de comando com tool use, inspirado no J.A.R.V.I.S."""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import anthropic

MODELO = os.environ.get("JARVIS_MODELO", "claude-sonnet-5-5")
NOME_USUARIO = os.environ.get("JARVIS_USUARIO", "senhor")
RAIZ = Path(os.environ.get("JARVIS_RAIZ", ".")).resolve()
ARQ_MEMORIA = Path(os.environ.get("JARVIS_MEMORIA", Path.home() / ".jarvis" / "memoria.json"))
MAX_VOLTAS = 15

PERSONA = f"""Você é Jarvis, assistente pessoal de {NOME_USUARIO}, inspirado no J.A.R.V.I.S. dos filmes do Homem de Ferro.

Estilo: português do Brasil, educado, sereno e objetivo, com um humor seco e raro. Trate o usuário por "{NOME_USUARIO}". Comece pelo resultado e só explique o que for necessário para a decisão. Sem entusiasmo exagerado, sem sermões.

Conduta:
- Use as ferramentas quando elas resolverem o pedido; não invente conteúdo de arquivos, horários ou saídas de comando.
- Antes de ações com efeito colateral (escrever arquivos, rodar comandos), diga em uma frase o que vai fazer.
- Se um pedido for ambíguo e a resposta mudar o resultado, pergunte. Caso contrário, adote o padrão mais razoável e informe qual foi.
- Quando {NOME_USUARIO} disser algo que valha lembrar depois (preferência, nome, rotina), registre com a ferramenta `lembrar`.
- Se uma ferramenta falhar, relate o erro real e proponha o próximo passo.
- Arquivos e comandos ficam restritos ao diretório de trabalho: {RAIZ}
"""

FERRAMENTAS = [
    {
        "name": "data_hora",
        "description": "Retorna a data e a hora atuais do sistema.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "listar_diretorio",
        "description": "Lista arquivos e pastas de um diretório dentro do diretório de trabalho.",
        "input_schema": {
            "type": "object",
            "properties": {"caminho": {"type": "string", "description": "Caminho relativo. Padrão: '.'"}},
        },
    },
    {
        "name": "ler_arquivo",
        "description": "Lê um arquivo de texto dentro do diretório de trabalho (até 20 mil caracteres).",
        "input_schema": {
            "type": "object",
            "properties": {"caminho": {"type": "string"}},
            "required": ["caminho"],
        },
    },
    {
        "name": "escrever_arquivo",
        "description": "Cria ou sobrescreve um arquivo de texto dentro do diretório de trabalho. Pede confirmação ao usuário.",
        "input_schema": {
            "type": "object",
            "properties": {"caminho": {"type": "string"}, "conteudo": {"type": "string"}},
            "required": ["caminho", "conteudo"],
        },
    },
    {
        "name": "executar_comando",
        "description": "Executa um comando de shell no diretório de trabalho e retorna a saída. Pede confirmação ao usuário.",
        "input_schema": {
            "type": "object",
            "properties": {"comando": {"type": "string"}},
            "required": ["comando"],
        },
    },
    {
        "name": "lembrar",
        "description": "Salva um fato duradouro sobre o usuário ou suas preferências na memória persistente.",
        "input_schema": {
            "type": "object",
            "properties": {"fato": {"type": "string"}},
            "required": ["fato"],
        },
    },
    {
        "name": "esquecer",
        "description": "Remove da memória o fato de número indicado (1 é o primeiro).",
        "input_schema": {
            "type": "object",
            "properties": {"numero": {"type": "integer"}},
            "required": ["numero"],
        },
    },
]


# --- memória -----------------------------------------------------------------

def carregar_memoria() -> list[str]:
    try:
        return json.loads(ARQ_MEMORIA.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_memoria(fatos: list[str]) -> None:
    ARQ_MEMORIA.parent.mkdir(parents=True, exist_ok=True)
    ARQ_MEMORIA.write_text(json.dumps(fatos, ensure_ascii=False, indent=2), encoding="utf-8")


def prompt_de_sistema() -> str:
    fatos = carregar_memoria()
    if not fatos:
        return PERSONA
    lista = "\n".join(f"{i}. {f}" for i, f in enumerate(fatos, 1))
    return f"{PERSONA}\nMemória sobre {NOME_USUARIO}:\n{lista}\n"


# --- ferramentas -------------------------------------------------------------

def _caminho_seguro(caminho: str) -> Path:
    destino = (RAIZ / caminho).resolve()
    if destino != RAIZ and RAIZ not in destino.parents:
        raise PermissionError(f"'{caminho}' está fora do diretório de trabalho")
    return destino


def _confirmar(descricao: str) -> bool:
    resposta = input(f"\n  [confirmação] {descricao}\n  Autoriza? [s/N] ").strip().lower()
    return resposta in ("s", "sim", "y", "yes")


def executar_ferramenta(nome: str, args: dict) -> str:
    try:
        if nome == "data_hora":
            return datetime.now().astimezone().strftime("%A, %d/%m/%Y %H:%M:%S %Z")

        if nome == "listar_diretorio":
            pasta = _caminho_seguro(args.get("caminho", "."))
            itens = sorted(pasta.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
            return "\n".join(f"{p.name}{'/' if p.is_dir() else ''}" for p in itens) or "(vazio)"

        if nome == "ler_arquivo":
            texto = _caminho_seguro(args["caminho"]).read_text(encoding="utf-8", errors="replace")
            return texto[:20000] + ("\n[truncado]" if len(texto) > 20000 else "")

        if nome == "escrever_arquivo":
            destino = _caminho_seguro(args["caminho"])
            if not _confirmar(f"Escrever {len(args['conteudo'])} caracteres em {destino}"):
                return "Ação recusada pelo usuário."
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(args["conteudo"], encoding="utf-8")
            return f"Arquivo gravado: {destino}"

        if nome == "executar_comando":
            if not _confirmar(f"Executar: {args['comando']}"):
                return "Ação recusada pelo usuário."
            r = subprocess.run(
                args["comando"], shell=True, cwd=RAIZ, capture_output=True, text=True, timeout=60
            )
            saida = (r.stdout + r.stderr)[-8000:]
            return f"código de saída {r.returncode}\n{saida}"

        if nome == "lembrar":
            fatos = carregar_memoria()
            fatos.append(args["fato"])
            salvar_memoria(fatos)
            return f"Registrado como item {len(fatos)}."

        if nome == "esquecer":
            fatos = carregar_memoria()
            n = args["numero"]
            if not 1 <= n <= len(fatos):
                return f"Não existe item {n}."
            removido = fatos.pop(n - 1)
            salvar_memoria(fatos)
            return f"Removido: {removido}"

        return f"Ferramenta desconhecida: {nome}"
    except subprocess.TimeoutExpired:
        return "Erro: o comando excedeu 60 segundos."
    except Exception as e:  # o erro volta ao modelo para que ele possa reagir
        return f"Erro: {type(e).__name__}: {e}"


# --- laço do agente ----------------------------------------------------------

def responder(cliente: anthropic.Anthropic, historico: list[dict]) -> None:
    """Roda o laço de tool use até o modelo terminar de responder."""
    for _ in range(MAX_VOLTAS):
        with cliente.messages.stream(
            model=MODELO,
            max_tokens=4096,
            system=prompt_de_sistema(),
            tools=FERRAMENTAS,
            messages=historico,
        ) as fluxo:
            for pedaco in fluxo.text_stream:
                print(pedaco, end="", flush=True)
            mensagem = fluxo.get_final_message()
        print()

        historico.append({"role": "assistant", "content": mensagem.content})
        if mensagem.stop_reason != "tool_use":
            return

        resultados = []
        for bloco in mensagem.content:
            if bloco.type == "tool_use":
                print(f"  · {bloco.name}({json.dumps(bloco.input, ensure_ascii=False)[:120]})")
                resultados.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": bloco.id,
                        "content": executar_ferramenta(bloco.name, bloco.input),
                    }
                )
        historico.append({"role": "user", "content": resultados})
    print("(limite de passos atingido; peça para eu continuar)")


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Defina ANTHROPIC_API_KEY antes de iniciar.")
    cliente = anthropic.Anthropic()
    historico: list[dict] = []
    hora = datetime.now().hour
    saudacao = "Bom dia" if hora < 12 else "Boa tarde" if hora < 18 else "Boa noite"
    print(f"{saudacao}, {NOME_USUARIO}. Jarvis à disposição. (digite 'sair' para encerrar)\n")
    while True:
        try:
            entrada = input("você> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if entrada.lower() in ("sair", "exit", "quit"):
            break
        if not entrada:
            continue
        historico.append({"role": "user", "content": entrada})
        print("jarvis> ", end="")
        try:
            responder(cliente, historico)
        except anthropic.APIError as e:
            print(f"\nFalha na API: {e}")
            historico.pop()
    print("Até logo.")


if __name__ == "__main__":
    main()
