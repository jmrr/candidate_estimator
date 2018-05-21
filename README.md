## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pserve candidate_estimator.ini
```

Application is served at http://localhost:6543

REST endpoints (you can find `.http` files in scripts directory):

```
POST /candidates
GET /candidates/{candidate_id}
```

