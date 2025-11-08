# Contributing to Discográfica ML Pro

## Code Style
- Use type hints where appropriate
- Follow PEP 8
- Keep functions small and focused

## Security
- Never commit secrets or API keys
- Use `.env` for configuration
- All API endpoints should use HTTPS

## Testing
Run tests with:
```bash
pytest tests/
```

Run full audit with:
```bash
python scripts/audit_viral_marketing_ai.py
```

## Structure
- `core/`: Main system logic
- `ml_engine/`: ML models and inference
- `campaign_manager/`: Campaign orchestration
- `uploaders/`: Platform-specific API clients
- `security/`: Auth and secrets management
- `analytics/`: Dashboards and metrics
- `compliance/`: Legal and copyright checks