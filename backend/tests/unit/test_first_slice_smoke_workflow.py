from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]


def test_first_slice_smoke_script_documents_owner_workflow() -> None:
    script = ROOT_DIR / "scripts" / "first-slice-smoke.sh"

    script_text = script.read_text(encoding="utf-8")

    assert "DB startup" in script_text
    assert "migrations" in script_text
    assert "API health" in script_text
    assert "GeekNews fetch" in script_text
    assert "AI usage inspection" in script_text
    assert "summary-runs" not in script_text
    assert "AI Cost Dashboard" in script_text
    assert "Telegram /geeknews and /cost" in script_text


def test_first_slice_smoke_doc_lists_env_and_slice_boundaries() -> None:
    doc = (ROOT_DIR / "docs" / "first-slice-smoke.md").read_text(encoding="utf-8")

    assert "DATABASE_URL" in doc
    assert "OPENROUTER_API_KEY" in doc
    assert "TELEGRAM_BOT_TOKEN" in doc
    assert "NEXT_PUBLIC_API_BASE_URL" in doc
    assert "--mocked" in doc
    for out_of_scope in [
        "market data",
        "disclosures",
        "GitHub trends",
        "EC2 deployment",
        "Caddy",
        "OpenTofu",
        "Grafana",
        "Vercel deployment",
        "Rust Ops CLI",
    ]:
        assert out_of_scope in doc
