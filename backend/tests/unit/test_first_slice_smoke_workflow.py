from pathlib import Path
from subprocess import run

ROOT_DIR = Path(__file__).resolve().parents[3]


def test_first_slice_smoke_script_documents_owner_workflow() -> None:
    script = ROOT_DIR / "scripts" / "first-slice-smoke.sh"

    result = run([script, "--help"], capture_output=True, check=True, text=True)

    assert "DB startup" in result.stdout
    assert "migrations" in result.stdout
    assert "API health" in result.stdout
    assert "GeekNews fetch" in result.stdout
    assert "summary generation" in result.stdout
    assert "AI Cost Dashboard" in result.stdout
    assert "Telegram /geeknews and /cost" in result.stdout


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
