# Chapter 34: API Design (FastAPI + SQLite)

> The backend that stores project metadata and serves pipeline results
> to the frontend via REST endpoints and a SQLite database.

---

## 1. What is it?

The **API** is Layer 3 of the platform (Ch 33). Built with **FastAPI**
(Python) and **SQLAlchemy** (ORM) against a **SQLite** database, it
exposes REST endpoints that the React UI (Ch 35) calls.

Entities modeled: **Projects**, **Samples**, **Runs**, and **Results**.

---

## 2. Why do we need it?

- The UI needs a structured way to query results.
- Metadata (which samples, which run, which condition) must be stored
  persistently.
- A clean API decouples the frontend from the pipeline internals.
- FastAPI auto-generates interactive API docs (`/docs`).

---

## 3. Where does it fit?

```
Pipeline results (Layer 1/2) -> API (reads into DB) -> UI (Ch 35)
```

The API is the single source of truth served to the frontend.

---

## 4. Input

- Pipeline output files (parsed into the database).
- HTTP requests from the UI.

---

## 5. Output

- REST responses (JSON) and a populated SQLite database.

---

## 6. How it works

### 6.1 Technology stack

| Component | Tool |
|-----------|------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite |
| Migrations | Alembic |
| Validation | Pydantic v2 |

### 6.2 Entities (schema)

- **Project**: a study (e.g., GSE52778).
- **Sample**: one biological sample (C1, T1, ...).
- **Run**: one pipeline execution.
- **Result**: outputs (QC metric, DE table row, plot reference).

### 6.3 Example endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/projects` | List projects |
| GET | `/projects/{id}` | Project detail |
| GET | `/projects/{id}/samples` | Samples in project |
| GET | `/results/de` | Differential expression results |
| GET | `/results/qc` | QC metrics for charts |

### 6.4 Database via SQLAlchemy

SQLAlchemy maps Python classes to SQLite tables; Alembic manages schema
migrations so the DB can evolve safely.

---

## 7. Biology behind it

- The API serves **biological results** (DE tables, pathway
  enrichments, QC plots) to scientists.
- Storing run metadata enables reproducibility (which versions, which
  samples).

---

## 8. Command

```bash
# create migrations / run server
cd api
alembic upgrade head
uvicorn app.main:app --reload
# docs at http://localhost:8000/docs
```

---

## 9. Example

`GET /projects` returns:

```json
{
  "id": 1,
  "accession": "GSE52778",
  "title": "Dexamethasone in airway smooth muscle",
  "organism": "Homo sapiens",
  "design": "control vs treatment"
}
```

---

## 10. How to read the output

- **2xx** = success; **4xx** = client error; **5xx** = server error.
- **`/docs`** (Swagger UI) lets you test endpoints interactively.
- JSON responses map directly to frontend components.

---

## 11. Common errors

| Error | Fix |
|-------|-----|
| 404 NotFound | Endpoint/row doesn't exist |
| 422 ValidationError | Payload fails Pydantic schema |
| 500 Internal | Server/DB error; check logs |
| CORS blocked | Configure allowed origins for UI |

---

## 12. Limitations

- SQLite is file-based, single-writer; production scales to Postgres.
- FastAPI is async; keep DB access patterns clean.
- API only serves stored results; triggering runs is deferred.

---

## 13. How our project uses it

- **Future / Phase 3**: `api/` with FastAPI + SQLAlchemy + SQLite.
- Serves DE/QC/pathway results to the UI.
- Documented in the stack decisions (FastAPI, SQLAlchemy 2.0, Alembic,
  SQLite, Uvicorn, Pydantic v2).

---

## 14. Official documentation

- **FastAPI**:
  https://fastapi.tiangolo.com/
- **SQLAlchemy**:
  https://docs.sqlalchemy.org/
- **Alembic**:
  https://alembic.sqlalchemy.org/

---

## 15. Mini exercise

1. Name the database/ORM/framework used and one role of each.
2. List the 4 core entities modeled.
3. What does the `/docs` endpoint provide?
4. What does a 422 response mean?
5. Why is Alembic used for schema migrations?

---

> **Next**: [Chapter 35: Frontend Design](frontend.md)
