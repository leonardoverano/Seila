import os
from types import SimpleNamespace

os.environ.update(WEBHOOK_SECRET="s", NTFY_TOPIC="t", SEEN_FILE="/tmp/seen_test.json")
import pytest
from fastapi.testclient import TestClient

import bot


@pytest.fixture(autouse=True)
def limpa():
    bot.SEEN_FILE.unlink(missing_ok=True)


def fake_claude(resposta):
    msgs = SimpleNamespace(create=lambda **kw: SimpleNamespace(content=[SimpleNamespace(text=resposta)]))
    return SimpleNamespace(messages=msgs)


def test_classifica_memecoin():
    r = bot.classificar("Buy $TRUMP now", fake_claude('{"memecoin": true, "tokens": ["$TRUMP"], "motivo": "x"}'))
    assert r["memecoin"] and r["tokens"] == ["$TRUMP"]


def test_json_invalido_nao_notifica():
    assert not bot.classificar("oi", fake_claude("nao sei"))["memecoin"]


def test_extrair_formatos():
    assert bot.extrair_post({"data": {"id": "123", "text": "oi"}})["url"].endswith("/123")
    assert bot.extrair_post({"full_text": "oi", "link": "u"})["url"] == "u"


def test_webhook_fluxo(monkeypatch):
    enviados = []
    monkeypatch.setattr(bot, "classificar", lambda t: {"memecoin": "coin" in t, "tokens": [], "motivo": ""})
    monkeypatch.setattr(bot, "notificar", lambda p, r: enviados.append(p))
    c = TestClient(bot.app)
    h = {"X-Webhook-Secret": "s"}
    assert c.post("/webhook", json={"text": "x", "id": "1"}).status_code == 401
    assert c.post("/webhook", headers=h, json={"text": "meme coin!", "id": "1"}).json()["status"] == "notificado"
    assert c.post("/webhook", headers=h, json={"text": "meme coin!", "id": "1"}).json()["motivo"] == "duplicado"
    assert c.post("/webhook", headers=h, json={"text": "tarifas", "id": "2"}).json()["status"] == "sem_memecoin"
    assert len(enviados) == 1
