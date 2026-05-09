# Backend Local Setup

TrendBoda backend는 `uv`로 Python 의존성과 명령 실행을 관리한다. Python 프로젝트는
`backend/` 아래에 있고, repo root에서 아래 명령을 실행하는 방식을 표준으로 둔다.

## 1. 기본 구조

```text
.
├── .env
├── backend/
│   ├── .python-version
│   ├── pyproject.toml
│   ├── src/trendboda/
│   └── tests/
└── db/migrations/
```

중요한 점:

- `.env`는 repo root에 둔다.
- Python 프로젝트 설정은 `backend/pyproject.toml`에 둔다.
- 명령은 repo root에서 `uv --directory backend ...` 형태로 실행한다.

## 2. 처음 한 번 실행

```bash
uv --directory backend sync
```

이 명령이 하는 일:

- Python 3.12 환경 준비
- `backend/.venv` 생성
- FastAPI, pytest, ruff, pyright 등 의존성 설치
- `uv.lock` 생성 또는 갱신

VS Code/Antigravity에서 Python interpreter는 아래 경로를 사용한다.

```text
backend/.venv/bin/python
```

## 3. 자주 쓰는 명령

### Unit test

```bash
uv --directory backend run pytest
```

기본 테스트 명령이다. `integration` 테스트는 제외된다.

### Integration test

```bash
uv --directory backend run pytest -m integration
```

Docker가 필요하다. Testcontainers가 Postgres 컨테이너를 띄우고, `dbmate up`으로 migration을
적용한 뒤 테스트한다.

### Ruff lint

```bash
uv --directory backend run ruff check .
```

### Ruff format check

```bash
uv --directory backend run ruff format --check .
```

### Ruff format apply

```bash
uv --directory backend run ruff format .
```

### Pyright type check

```bash
uv --directory backend run pyright
```

## 4. 왜 `uv --directory backend`를 쓰나

다음 두 명령은 비슷한 목적이다.

```bash
cd backend
uv run pytest
```

```bash
uv --directory backend run pytest
```

이 repo에서는 두 번째 방식을 표준으로 둔다.

이유:

- repo root에 `.env`, `db/`, `.vscode/`가 있다.
- backend, DB, 나중의 web app을 root에서 함께 다룬다.
- VS Code task와 터미널 명령을 같은 형태로 유지할 수 있다.

## 5. `.env`

로컬 실제 값은 repo root의 `.env`에 둔다.

예:

```env
DATABASE_URL=postgres://trendboda:trendboda@localhost:5432/trendboda?sslmode=disable
OPENROUTER_API_KEY=
TELEGRAM_BOT_TOKEN=
```

`.env`는 git에 올리지 않는다. 공유용 예시는 `.env.example`에 둔다.

Python 코드는 `pydantic-settings`로 root `.env`를 읽는다.

## 6. dbmate

`dbmate`는 DB migration CLI다. Python 패키지가 아니므로 `uv`로 설치하지 않는다.

macOS 설치:

```bash
brew install dbmate
```

설치 확인:

```bash
which dbmate
dbmate --version
```

현재 migration 적용:

```bash
dbmate --env-file .env --migrations-dir db/migrations up
```

현재 migration 상태 확인:

```bash
dbmate --env-file .env --migrations-dir db/migrations status
```

새 migration 생성:

```bash
dbmate --migrations-dir db/migrations new create_some_table
```

Migration 파일은 `-- migrate:up`, `-- migrate:down` 섹션을 가진 SQL 파일이다.

## 7. Docker와 integration test

Integration test는 Docker Desktop이 켜져 있어야 한다.

확인:

```bash
docker info
```

실행:

```bash
uv --directory backend run pytest -m integration
```

현재 integration test 흐름:

```text
pytest
-> testcontainers가 postgres:16-alpine 시작
-> dbmate up 실행
-> migration 결과 검증
-> 컨테이너 종료
```

Docker가 꺼져 있거나 socket 접근이 막히면 이런 오류가 난다.

```text
Cannot connect to the Docker daemon
```

이 경우 Docker Desktop을 켠 뒤 다시 실행한다.

## 8. VS Code / Antigravity

권장 확장:

- Python
- Pylance
- Ruff
- Prettier

설정 파일:

```text
.vscode/settings.json
.vscode/extensions.json
.vscode/tasks.json
```

Command Palette에서 `Tasks: Run Task` 실행 후 사용할 수 있는 task:

- `backend: sync`
- `backend: test`
- `backend: test integration`
- `backend: lint`
- `backend: format`
- `backend: typecheck`
- `dbmate: up`

## 9. 정상 상태 체크리스트

아래가 모두 통과하면 기본 셋팅은 정상이다.

```bash
uv --directory backend sync
uv --directory backend run pytest
uv --directory backend run ruff check .
uv --directory backend run ruff format --check .
uv --directory backend run pyright
uv --directory backend run pytest -m integration
```

마지막 integration test만 Docker Desktop이 필요하다.
