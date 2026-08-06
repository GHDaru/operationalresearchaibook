"""Smoke tests do companion — sem rede, sem banco (adapter echo + memória).

Cobrem o fluxo (chat, histórico, capacidades), o gating progressivo e o
rate limit. Rodar:  cd chat-companion/backend && python -m pytest
"""

import os
import sys

os.environ.setdefault("LLM_ADAPTER", "echo")   # sem rede
os.environ.pop("DATABASE_URL", None)           # força MemoryStore
os.environ["RATE_LIMIT_MSGS"] = "3"
os.environ["RATE_LIMIT_WINDOW_S"] = "60"
os.environ["RATE_LIMIT_IP_FACTOR"] = "100"  # guarda por IP fora do caminho nos testes

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402

import capabilities  # noqa: E402
import app as appmod  # noqa: E402

client = TestClient(appmod.app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["store"] == "memory"


def test_chat_and_history():
    sid = "s-chat"
    r = client.post("/chat", json={"session_id": sid, "message": "olá", "chapter": 1,
                                   "mode": "progressivo"})
    assert r.status_code == 200
    body = r.json()
    assert "echo" in body["reply"]
    assert any(c["chave"] == "tutor" for c in body["capabilities_ativas"])
    h = client.get("/history", params={"session_id": sid}).json()["messages"]
    assert h[0]["role"] == "user" and h[-1]["role"] == "assistant"


def test_gating_progressive_hides_future_tools():
    # A busca no livro vale desde a capa: o tutor precisa citar a fonte já na
    # primeira pergunta, então o loop nasce ativo (cap. 0).
    assert capabilities.tools_ativas(0, "progressivo") == {"buscar_no_livro"}
    # O registro de tentativa só entra com o primeiro capítulo numerado.
    assert "exercicio_registrar_tentativa" not in capabilities.tools_ativas(0, "progressivo")
    assert "exercicio_registrar_tentativa" in capabilities.tools_ativas(1, "progressivo")
    # avançado libera tudo mesmo no cap. 0
    assert {"exercicio_registrar_tentativa", "buscar_no_livro"} <= capabilities.tools_ativas(0, "avancado")


def test_capabilities_endpoint():
    r = client.get("/capabilities", params={"chapter": 0, "mode": "progressivo"})
    j = r.json()
    assert j["loop_ativo"] is True
    ativos = {c["chave"] for c in j["capabilities"] if c["ativa"]}
    # na capa: tutor, busca e mapa ativos; a prática, ainda não
    assert {"tutor", "busca_livro", "mapa"} <= ativos
    assert "exercicios" not in ativos
    # a partir do primeiro capítulo numerado, a prática entra
    ativos1 = {c["chave"] for c in client.get(
        "/capabilities", params={"chapter": 1, "mode": "progressivo"}).json()["capabilities"] if c["ativa"]}
    assert "exercicios" in ativos1


def test_rate_limit_429():
    sid = "s-rate"
    for _ in range(3):
        assert client.post("/chat", json={"session_id": sid, "message": "hi"}).status_code == 200
    # 4ª na janela estoura
    assert client.post("/chat", json={"session_id": sid, "message": "hi"}).status_code == 429


def test_byok_bypasses_rate_limit():
    sid = "s-byok"
    for _ in range(3):
        client.post("/chat", json={"session_id": sid, "message": "hi"})
    r = client.post("/chat", json={"session_id": sid, "message": "hi", "byok_key": "nvapi-x"})
    # BYOK isenta do limite do projeto; echo ignora a chave, mas não deve dar 429
    assert r.status_code == 200


def test_delete_session():
    sid = "s-del"
    client.post("/chat", json={"session_id": sid, "message": "oi"})
    client.delete(f"/session/{sid}")
    assert client.get("/history", params={"session_id": sid}).json()["messages"] == []


def test_suggestion_persists_and_lists():
    sid = "s-sug"
    r = client.post("/suggestion", json={"session_id": sid, "texto": "ótimo livro, cap 5 podia ter mais exemplos", "pagina": "05-ferramentas.html"})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True and body["email_enviado"] is False  # sem SMTP no teste
    # sem ADMIN_TOKEN -> 403
    assert client.get("/suggestions", params={"token": "x"}).status_code == 403


def test_suggestion_empty_400():
    assert client.post("/suggestion", json={"session_id": "s", "texto": "  "}).status_code == 400


def test_chat_stream_echo():
    """spec 047: o stream emite deltas e um done com a resposta completa,
    idêntica à que fica persistida no histórico."""
    import json
    sid = "t-stream"
    with client.stream("POST", "/chat/stream",
                       json={"session_id": sid, "message": "olá streaming"}) as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        eventos = []
        for linha in r.iter_lines():
            if linha.startswith("data: "):
                eventos.append(json.loads(linha[6:]))
    deltas = [e["delta"] for e in eventos if "delta" in e]
    done = [e for e in eventos if e.get("done")]
    assert len(deltas) > 1, "deveria vir em mais de um pedaço"
    assert len(done) == 1
    assert "".join(deltas) == done[0]["reply"]
    hist = client.get("/history", params={"session_id": sid}).json()["messages"]
    assert hist[-1]["role"] == "assistant" and hist[-1]["content"] == done[0]["reply"]


def test_rate_limit_sobrevive_a_restart():
    """spec 049: o 429 por sessão vem do STORE (mensagens persistidas), não do
    deque em memória — limpar o deque (simulando deploy) não zera o limite."""
    sid = "t-rl-persistente"
    for i in range(3):  # RATE_LIMIT_MSGS = 3 nos testes
        r = client.post("/chat", json={"session_id": sid, "message": f"m{i}"})
        assert r.status_code == 200
    appmod._hits.clear()  # "restart" da instância
    r = client.post("/chat", json={"session_id": sid, "message": "m-extra"})
    assert r.status_code == 429


def test_debug_bastidores():
    """spec 053: /chat e o done do stream expõem o bloco debug (transparência)."""
    import json
    r = client.post("/chat", json={"session_id": "t-debug", "message": "o que é loop?"})
    d = r.json()["debug"]
    assert d["tokens_estimados"] > 0 and d["janela_tokens"] > 0
    assert d["historico_msgs"] >= 1 and isinstance(d["trechos"], list)
    assert "Tutor do handbook" in d["capacidades_ativas"]

    with client.stream("POST", "/chat/stream",
                       json={"session_id": "t-debug2", "message": "e compactação?"}) as r:
        eventos = [json.loads(l[6:]) for l in r.iter_lines() if l.startswith("data: ")]
    done = [e for e in eventos if e.get("done")][0]
    assert done["debug"]["tokens_estimados"] > 0


def test_consent_telemetria_objetivo():
    """spec 054: aceite gravado; telemetria só com consentimento; objetivo
    persiste, aparece no GET e entra como camada do system prompt (debug)."""
    sid = "t-054"
    # telemetria ANTES do aceite: não grava
    r = client.post("/telemetry", json={"session_id": sid, "slug": "02-loop-do-agente"})
    assert r.json()["ok"] is False
    # aceite
    r = client.post("/consent", json={"session_id": sid, "versao": "v1"})
    assert r.json()["ok"] is True
    # telemetria depois: grava
    r = client.post("/telemetry", json={"session_id": sid, "slug": "02-loop-do-agente"})
    assert r.json()["ok"] is True
    # resumo exige token
    assert client.get("/telemetry").status_code == 403
    # objetivo
    r = client.post("/objetivo", json={"session_id": sid, "texto": "construir um agente para meu ERP"})
    assert r.json()["ok"] is True
    assert client.get("/objetivo", params={"session_id": sid}).json()["objetivo"].startswith("construir")
    # camada no prompt: via debug do /chat
    d = client.post("/chat", json={"session_id": sid, "message": "por onde começo?"}).json()["debug"]
    assert d["objetivo"].startswith("construir")
    # e o system prompt de fato contém a camada
    assert "Objetivo declarado do leitor" in appmod._system_prompt(2, "progressivo", [], "x")


def test_telemetry_publico_agregado():
    """spec 055: projeção pública só tem agregados — nada de sessões/timestamps."""
    sid = "t-055"
    client.post("/consent", json={"session_id": sid, "versao": "v1"})
    for slug in ("02-loop-do-agente", "02-loop-do-agente", "glossario"):
        client.post("/telemetry", json={"session_id": sid, "slug": slug})
    d = client.get("/telemetry/publico").json()
    assert d["total"] >= 3 and d["paginas_distintas"] >= 2
    assert d["por_pagina"].get("02-loop-do-agente", 0) >= 2
    assert set(d.keys()) == {"total", "paginas_distintas", "por_pagina"}  # nada além do agregado


# ---------------------------------------------------------------- spec 005
# Exercícios via chat: a página declara o exercício, o servidor resolve o
# enunciado, o tutor avalia e a tentativa é registrada.

# Estes são testes de MECANISMO, e mecanismo não pode depender de conteúdo
# editorial: o registro de exercícios muda a cada rodada do livro, e um teste
# ancorado num identificador real quebra sem que nada do backend tenha quebrado.
# (Foi exatamente o que aconteceu quando este repositório trocou de livro.)
# Por isso semeamos um exercício SINTÉTICO no índice em memória.
EX_FIXTURE = {
    "id": "cap07.exA", "capitulo": 7, "serie": "cap07", "variante": "A",
    "tipo": "formular", "capacidade": "exercicios",
    "titulo": "Formular um mix de produção",
    "enunciado": "Uma fábrica produz dois itens com dois recursos escassos...",
    "criterios": ["As variáveis de decisão estão declaradas com unidade",
                  "A função objetivo maximiza margem, não receita",
                  "Há uma restrição por recurso escasso"],
    "erro_provavel": "Maximizar receita em vez de margem de contribuição.",
    "resposta_guia": "Sejam x1 e x2 as quantidades a produzir...",
}
appmod._exercicios._por_id[EX_FIXTURE["id"]] = EX_FIXTURE
EX_ID = EX_FIXTURE["id"]
EX_CAP = EX_FIXTURE["capitulo"]


def _snap(exercicio_id):
    return {"screen": {"id": "capitulo.exercicio", "route": "/07-formulacao"},
            "selected_entity": {"type": "exercicio", "id": exercicio_id}}


def test_exercicio_desconhecido_e_recusado_na_borda():
    """CA-1: o enunciado nunca vem do cliente — id inexistente para antes do modelo."""
    r = client.post("/chat", json={"session_id": "s-ex-1", "message": "oi",
                                   "chapter": EX_CAP, "snapshot": _snap("cap99.ex99")})
    assert r.status_code == 400
    assert "desconhecido" in r.json()["detail"]


def test_snapshot_com_campo_extra_e_rejeitado():
    """Schema fechado: campo desconhecido não passa na borda."""
    mau = _snap(EX_ID)
    mau["selected_entity"]["senha"] = "vazando"
    r = client.post("/chat", json={"session_id": "s-ex-2", "message": "oi",
                                   "chapter": EX_CAP, "snapshot": mau})
    assert r.status_code == 422


def test_enunciado_entra_como_mensagem_de_sistema_propria():
    """CA-2: camadas separadas — o exercício não é concatenado ao texto do leitor."""
    import app as appmod
    capturado = {}
    original = appmod._preparar_chat

    def espiao(inp, request):
        r = original(inp, request)
        capturado["history"] = r[2]
        return r

    appmod._preparar_chat = espiao
    try:
        client.post("/chat", json={"session_id": "s-ex-3", "message": "aqui vai minha resposta",
                                   "chapter": EX_CAP, "snapshot": _snap(EX_ID)})
    finally:
        appmod._preparar_chat = original
    systems = [m for m in capturado["history"] if m["role"] == "system"]
    assert len(systems) >= 2, "persona e exercício devem ser mensagens distintas"
    assert any(EX_ID in m["content"] and "Critérios de avaliação" in m["content"]
               for m in systems), "o enunciado e a rubrica devem chegar ao modelo"
    # a rubrica NUNCA vai junto do texto do leitor
    users = [m for m in capturado["history"] if m["role"] == "user"]
    assert all("Critérios de avaliação" not in m["content"] for m in users)


def test_acao_de_registro_so_existe_com_exercicio_em_foco():
    """CA-3: sem exercício declarado, a ferramenta some do catálogo do modelo."""
    import app as appmod
    from types import SimpleNamespace
    req = SimpleNamespace(client=SimpleNamespace(host="1.2.3.4"))

    sem = appmod.ChatIn(session_id="s-ex-4a", message="oi", chapter=EX_CAP)
    assert "exercicio_registrar_tentativa" not in appmod._preparar_chat(sem, req)[3]

    com = appmod.ChatIn(session_id="s-ex-4b", message="oi", chapter=EX_CAP,
                        snapshot=appmod.Snapshot(**_snap(EX_ID)))
    assert "exercicio_registrar_tentativa" in appmod._preparar_chat(com, req)[3]


def test_registro_persiste_e_aparece_no_progresso():
    """CA-4: a tentativa vira traço consultável."""
    import app as appmod
    appmod._tools.contexto = {"session_id": "s-ex-5",
                              "exercicio": {"id": EX_ID, "capitulo": EX_CAP}}
    out = appmod._tools.executar("exercicio_registrar_tentativa",
                                 {"veredito": "parcial", "resumo_feedback": "faltou a suficiência"},
                                 {"exercicio_registrar_tentativa"})
    assert "registrada" in out
    prog = client.get("/progresso", params={"session_id": "s-ex-5"}).json()["tentativas"]
    assert len(prog) == 1 and prog[0]["exercicio_id"] == EX_ID
    assert prog[0]["veredito"] == "parcial"


def test_dedup_de_clique_duplo():
    """CA-5: chave natural — o mesmo veredito duas vezes não vira dois registros."""
    import app as appmod
    appmod._tools.contexto = {"session_id": "s-ex-6",
                              "exercicio": {"id": "cap03.exA", "capitulo": 3}}
    args = {"veredito": "aprovado", "resumo_feedback": "ok"}
    appmod._tools.executar("exercicio_registrar_tentativa", args, {"exercicio_registrar_tentativa"})
    segunda = appmod._tools.executar("exercicio_registrar_tentativa", args, {"exercicio_registrar_tentativa"})
    assert "já registrada" in segunda
    assert len(client.get("/progresso", params={"session_id": "s-ex-6"}).json()["tentativas"]) == 1


def test_modelo_nao_registra_exercicio_de_outra_pagina():
    """O substituto barato do context_hash: comparar o id do exercício."""
    import app as appmod
    appmod._tools.contexto = {"session_id": "s-ex-7",
                              "exercicio": {"id": EX_ID, "capitulo": EX_CAP}}
    out = appmod._tools.executar("exercicio_registrar_tentativa",
                                 {"exercicio_id": "cap09.ex01", "veredito": "aprovado"},
                                 {"exercicio_registrar_tentativa"})
    assert out.startswith("erro:") and EX_ID in out
    assert client.get("/progresso", params={"session_id": "s-ex-7"}).json()["tentativas"] == []


def test_veredito_invalido_recusado():
    import app as appmod
    appmod._tools.contexto = {"session_id": "s-ex-8",
                              "exercicio": {"id": EX_ID, "capitulo": EX_CAP}}
    out = appmod._tools.executar("exercicio_registrar_tentativa",
                                 {"veredito": "genial"}, {"exercicio_registrar_tentativa"})
    assert out.startswith("erro:")


def test_esquecimento_apaga_o_progresso():
    """CA-7: o direito ao esquecimento vale para as tentativas."""
    import app as appmod
    appmod._tools.contexto = {"session_id": "s-ex-9",
                              "exercicio": {"id": "cap04.exA", "capitulo": 4}}
    appmod._tools.executar("exercicio_registrar_tentativa", {"veredito": "aprovado"},
                           {"exercicio_registrar_tentativa"})
    assert client.get("/progresso", params={"session_id": "s-ex-9"}).json()["tentativas"]
    client.delete("/session/s-ex-9")
    assert client.get("/progresso", params={"session_id": "s-ex-9"}).json()["tentativas"] == []


def test_rota_de_exercicios_nao_expoe_a_rubrica():
    """O leitor não deve poder ler por quais critérios será avaliado."""
    j = client.get("/exercicios", params={"capitulo": EX_CAP}).json()
    ids = {e["id"] for e in j["exercicios"]}
    assert EX_ID in ids, ids
    for e in j["exercicios"]:
        assert "criterios" not in e
        assert "erro_provavel" not in e, "o mecanismo do erro é do tutor, não do leitor"
        assert "resposta_guia" not in e, "a resposta-guia nunca vai ao cliente"
