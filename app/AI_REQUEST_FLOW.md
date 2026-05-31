Client Request
↓
Validation Layer
↓
Authentication
↓
Prompt Builder
↓
LLM Service
↓
Response Formatter
↓
Logging
↓
Final Response

## Operational Recommendations

- **Failures by layer:** Client (network, malformed requests); Edge/Gateway (TLS, DDoS, rate-limit); Transport (timeouts, latency); Auth (expired tokens, provider outage); API/Middleware (schema/deserialization errors); Validation (injection, oversized payloads); Business Logic (domain errors, race conditions); Storage (db timeouts, permission errors); Model Invocation (quota, partial responses); Model Output (hallucinations, unsafe content); Observability (missing traces).

- **Logging (structured):** correlation id, span ids, latency, endpoint, user/tenant id (hashed), model name/version, token usage, status codes, validation errors, auth failures, rate-limit events, error types + stack traces. Sample full prompts/responses only to secure audit logs (low %), always redact secrets/PII.

- **Never send to the model:** API keys, private keys, raw auth tokens/JWTs, full SSNs, full credit card numbers, unredacted PHI, internal-only secrets, unapproved proprietary source code. Replace with deterministic placeholders or hashed identifiers.

- **Rate limiting (defense-in-depth):** enforce at Edge/API Gateway (global & per-IP), Middleware (per-tenant/api-key), Application (per-user/session, fairness), and at Model Invocation (per-model token/concurrency limits, circuit-breaker). Return `Retry-After` headers and use token-bucket/leaky-bucket with jitter + exponential backoff on clients.

See configuration and policy details in [app/config/ai_policy.yaml](app/config/ai_policy.yaml).
