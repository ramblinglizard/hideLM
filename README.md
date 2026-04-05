# hideLM

**Deterministic PII anonymization proxy for LLM APIs — no ML models, regex + math only. GDPR-ready, self-hosted, locale-aware.**

hideLM sits between your application and any external LLM API (OpenAI, Anthropic, Google, etc.). It automatically detects and replaces sensitive data before the request leaves your network, then restores the original values in the response — transparently, with zero changes to your existing code.

```
Your App  →  hideLM (localhost:8080)  →  OpenAI / Anthropic / ...
              ↑ masks PII                ↓ restores PII
```

---

## Why hideLM?

- **100% deterministic** — no ML models, no GPU, no inference. PII detection uses regex + mathematical validation (Luhn, mod-97, ISO checksums).
- **Zero false positives on structured data** — a credit card number is verified with the Luhn algorithm before being masked. An IBAN is verified with mod-97. No guessing.
- **Drop-in replacement** — change one line: your API endpoint from `https://api.openai.com` to `http://localhost:8080`. Nothing else changes.
- **Self-hosted** — your data never leaves your infrastructure unmasked.
- **Locale-aware** — activate national ID detectors (SSN, Codice Fiscale, NINO, etc.) per country with a single env variable.
- **GDPR · CCPA · HIPAA · LGPD · PIPEDA** ready.

---

## Quickstart

```bash
git clone https://github.com/ramblinglizard/hideLM.git
cd hideLM
cp .env.example .env          # add your API key and configure locales
docker-compose up -d
```

Point your application at `http://localhost:8080` instead of `https://api.openai.com`. Done.

---

## Configuration

Edit `.env`:

```env
TARGET_API_URL=https://api.openai.com
TARGET_API_KEY=sk-your-key-here

# In-memory vault (recommended) — data never touches disk
VAULT_DB_PATH=
VAULT_TTL_SECONDS=3600

# Activate national ID detectors for one or more countries
LOCALES=us,gb

# Toggle individual universal detectors
DETECT_EMAIL=true
DETECT_IBAN=true
DETECT_CREDIT_CARD=true
DETECT_PHONE=true
DETECT_IP=true
DETECT_URL_CREDENTIALS=true
DETECT_NAMES=true
```

---

## Detectors

### Universal (always active)

| Type | Standard | Validation |
|---|---|---|
| Email | RFC 5322 | Regex |
| Credit card | ISO/IEC 7812 | Regex + Luhn algorithm |
| IBAN | ISO 13616 | Regex + mod-97 (86 countries) |
| IPv4 / IPv6 | RFC 791 / 2460 | Regex + octet range check |
| URL with credentials | RFC 3986 | Regex (`scheme://user:pass@host`) |
| Phone number | E.164 + national | Google libphonenumber (all countries) |

### Locale plugins (`LOCALES=xx,yy`)

| Locale | Detectors |
|---|---|
| `it` | Codice Fiscale (+ official checksum), Partita IVA |
| `us` | SSN, EIN |
| `de` | Steueridentifikationsnummer (ISO 7064 Mod 11,10) |
| `fr` | Numéro de Sécurité Sociale (NIR) |
| `gb` | National Insurance Number (NINO) |

Each locale also ships a `names.txt` dictionary used for full-name detection.

---

## How tokens work

A masked request looks like:

```
User: "Please process the payment for [EMAIL_1], card [CREDIT_CARD_1]."
```

The original values are stored in an in-memory vault keyed by session ID and restored in the response before it reaches your application. The same value always gets the same token within a session.

---

## Security

hideLM has **no built-in authentication**. By default it binds to `localhost:8080` and is only reachable from the same machine — that is the recommended setup.

If you expose hideLM on a network interface (e.g. via Docker with `-p 0.0.0.0:8080:8080` or behind a reverse proxy), you are responsible for adding authentication (API gateway, mTLS, firewall rules). An unauthenticated hideLM instance would let any caller relay requests through your API key.

---

## Running tests

```bash
pip install -r requirements.txt
pytest
```

---

## Adding a new locale

1. Create `detector/locales/xx/` (replace `xx` with the ISO country code)
2. Add detector classes extending `BaseDetector`
3. Add a `names.txt` with first names and surnames (one per line)
4. Export a `get_detectors() -> list[BaseDetector]` function in `__init__.py`
5. Open a PR — new locales are always welcome

---

## License

MIT
