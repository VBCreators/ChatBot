# Open Source(with exceptions) Tech Stack Summary:

1. **Foundation:** React/Next.js, FastAPI, PostgreSQL, MinIO, Valkey, Keycloak/Authenik, Traefik, Docker, Harbor, GitLab CE, Prometheus/Grafana/Loki, Vault/Infisical.
2. **Cloud-native:** Kubernetes, Helm, ArgoCD, OpenTofu, cert-manager, OpenTelemetry, Alertmanager, Fluent Bit, Velero, Longhorn.
3. **AI platform:** LiteLLM, Qdrant, LangGraph, Langfuse, Ragas, OpenSearch, RabbitMQ or Kafka/Redpanda (choose based on your needs), Guardrails, Whisper/PaddleOCR if your application uses speech or documents.
4. **Enterprise hardening:** APISIX, OpenAppSec, Falco, Trivy, Semgrep, OWASP ZAP, Uptime Kuma, Renovate, Playwright, k6, PostHog, Unleash, Chatwoot, Vaultwarden.



# 1. Frontend

| Purpose       | Tool                    |
| ------------- | ----------------------- |
| Frontend      | React                   |
| Framework     | Next.js                 |
| UI Components | shadcn/ui               |
| Styling       | Tailwind CSS            |
| Forms         | React Hook Form         |
| Validation    | Zod                     |
| State         | Zustand / Redux Toolkit |
| Data Fetching | TanStack Query          |
| Charts        | Apache ECharts          |

---

# 2. Backend

| Purpose            | Tool              |
| ------------------ | ----------------- |
| API                | FastAPI           |
| Validation         | Pydantic          |
| ORM                | SQLAlchemy        |
| Database Migration | Alembic           |
| Background Jobs    | Celery / Dramatiq |
| Scheduling         | APScheduler       |

---

# 3. Databases

| Purpose        | Tool       |
| -------------- | ---------- |
| SQL            | PostgreSQL |
| Vector DB      | Qdrant     |
| Search         | OpenSearch |
| Cache          | Valkey     |
| Object Storage | MinIO      |

---

# 4. Authentication

| Purpose           | Tool                 |
| ----------------- | -------------------- |
| Identity Provider | Keycloak / Authentik |
| MFA               | Built into Keycloak  |
| OAuth Provider    | Keycloak             |
| SSO               | Keycloak             |
| Passkeys          | Keycloak             |

---

# 5. AI Stack

| Purpose           | Tool                            |
| ----------------- | ------------------------------- |
| AI Gateway        | LiteLLM                         |
| Model Router      | LiteLLM                         |
| Embeddings        | sentence-transformers           |
| LLM Framework     | LangChain / LlamaIndex          |
| Agent Framework   | LangGraph                       |
| Reranker          | BGE Reranker                    |
| OCR               | Tesseract / PaddleOCR           |
| Speech-to-Text    | Whisper                         |
| Text-to-Speech    | Piper                           |
| Guardrails        | Guardrails AI / NeMo Guardrails |
| Prompt Management | Langfuse                        |
| Evaluation        | Ragas                           |
| AI Monitoring     | Langfuse                        |
| AI Tracing        | Langfuse                        |

---

# 6. Message Systems

| Purpose         | Tool             |
| --------------- | ---------------- |
| Queue           | RabbitMQ         |
| Event Streaming | Kafka / Redpanda |
| Event Bus       | NATS             |

Many companies use **NATS** for lightweight microservice communication and Kafka only for event streaming.

---

# 7. API Layer

| Purpose            | Tool    |
| ------------------ | ------- |
| Reverse Proxy      | Traefik |
| API Gateway        | APISIX  |
| GraphQL (optional) | Hasura  |
| gRPC               | Native  |

---

# 8. Security

| Purpose               | Tool                  |
| --------------------- | --------------------- |
| Secrets               | Vault OSS / Infisical |
| WAF                   | OpenAppSec            |
| IDS                   | Suricata              |
| IPS                   | Suricata              |
| Runtime Security      | Falco                 |
| Vulnerability Scanner | Trivy                 |
| Image Scanner         | Trivy                 |
| Dependency Scanner    | Grype                 |
| Malware Scanner       | ClamAV                |
| Certificate Manager   | cert-manager          |
| PKI                   | Smallstep Step-CA     |
| Rate Limiting         | APISIX                |
| DDoS Protection       | Cloudflare (free)     |
| CSP                   | Next.js headers       |
| SAST                  | Semgrep               |
| DAST                  | OWASP ZAP             |

---

# 9. Observability

| Purpose              | Tool                          |
| -------------------- | ----------------------------- |
| Metrics              | Prometheus                    |
| Dashboards           | Grafana                       |
| Logs                 | Loki                          |
| Log Shipping         | Alloy / Fluent Bit            |
| Tracing              | Jaeger                        |
| OpenTelemetry        | OpenTelemetry Collector       |
| Alerting             | Alertmanager                  |
| Uptime               | Uptime Kuma                   |
| Synthetic Monitoring | Checkmate / Blackbox Exporter |

I would strongly recommend adding **OpenTelemetry Collector**.

---

# 10. CI/CD

| Purpose     | Tool                |
| ----------- | ------------------- |
| Git         | GitLab CE / Gitea   |
| CI/CD       | GitLab CI / Jenkins |
| GitOps      | ArgoCD              |
| Image Build | BuildKit            |
| Deployment  | ArgoCD              |
| Rollbacks   | Argo Rollouts       |

I recommend **GitOps** using **ArgoCD** instead of traditional deployment scripts.

---

# 11. Kubernetes

| Purpose         | Tool               |
| --------------- | ------------------ |
| Runtime         | containerd         |
| Containers      | Docker             |
| Orchestration   | Kubernetes         |
| Package Manager | Helm               |
| Kustomization   | Kustomize          |
| Autoscaler      | KEDA               |
| Node Autoscaler | Cluster Autoscaler |
| Service Mesh    | Istio              |
| Gateway API     | Envoy Gateway      |

---

# 12. Storage

| Purpose        | Tool     |
| -------------- | -------- |
| Object Storage | MinIO    |
| Block Storage  | Longhorn |
| Shared Storage | NFS      |
| CSI            | Longhorn |

Longhorn is excellent for homelabs.

---

# 13. Backup

Many people forget this.

| Purpose             | Tool                       |
| ------------------- | -------------------------- |
| Kubernetes Backup   | Velero                     |
| PostgreSQL Backup   | pgBackRest                 |
| MinIO Backup        | MinIO Replication / Restic |
| File Backup         | Restic                     |
| Snapshot Management | Velero                     |

---

# 14. Artifact Management

| Purpose            | Tool   |
| ------------------ | ------ |
| Container Registry | Harbor |
| Helm Registry      | Harbor |
| OCI Registry       | Harbor |

---

# 15. Infrastructure

| Purpose           | Tool        |
| ----------------- | ----------- |
| IaC               | OpenTofu    |
| Configuration     | Ansible     |
| Secrets Injection | Vault Agent |

---

# 16. Workflow Automation

| Purpose    | Tool    |
| ---------- | ------- |
| Automation | n8n     |
| BPM        | Camunda |

---

# 17. Feature Management

| Purpose       | Tool       |
| ------------- | ---------- |
| Feature Flags | Unleash    |
| Experiments   | GrowthBook |

---

# 18. Product Analytics

| Purpose           | Tool    |
| ----------------- | ------- |
| Product Analytics | PostHog |
| Session Replay    | PostHog |
| Heatmaps          | PostHog |

---

# 19. Email

You'll need this.

| Purpose             | Tool     |
| ------------------- | -------- |
| SMTP                | Postal   |
| Transactional Email | Listmonk |
| Marketing           | Listmonk |

---

# 20. Notifications

| Purpose  | Tool             |
| -------- | ---------------- |
| Push     | ntfy             |
| SMS      | Twilio (not OSS) |
| Web Push | VAPID            |

---

# 21. Billing

Usually not open source.

| Purpose      | Tool          |
| ------------ | ------------- |
| Billing      | Stripe        |
| Invoices     | Invoice Ninja |
| Subscription | Stripe        |

---

# 22. Documentation

| Purpose        | Tool            |
| -------------- | --------------- |
| Docs           | MkDocs Material |
| API Docs       | FastAPI Swagger |
| Knowledge Base | BookStack       |

---

# 23. Developer Platform

| Purpose            | Tool           |
| ------------------ | -------------- |
| Internal Portal    | Backstage      |
| Dependency Updates | Renovate       |
| Dev Containers     | Dev Containers |
| Pre-commit Hooks   | pre-commit     |

---

# 24. Testing

| Purpose         | Tool                  |
| --------------- | --------------------- |
| Backend Tests   | pytest                |
| Frontend Tests  | Vitest                |
| Component Tests | React Testing Library |
| E2E             | Playwright            |
| API Tests       | Bruno                 |
| Load Testing    | k6                    |
| Chaos Testing   | LitmusChaos           |

---

# 25. Business Operations

| Purpose          | Tool                  |
| ---------------- | --------------------- |
| CRM              | Twenty CRM            |
| Helpdesk         | Zammad                |
| Chat Support     | Chatwoot              |
| Status Page      | Uptime Kuma           |
| Password Manager | Bitwarden/Vaultwarden |

---

# Tools I would definitely add to your current stack

These are the ones I think are missing and worth adopting:

* ArgoCD (GitOps deployments)
* Helm
* Kustomize
* cert-manager
* OpenTelemetry Collector
* Alertmanager
* Fluent Bit or Grafana Alloy
* Uptime Kuma
* Trivy
* Falco
* Suricata
* Semgrep
* OWASP ZAP
* Velero
* pgBackRest
* Restic
* Longhorn
* Ansible
* Renovate
* Playwright
* k6
* MkDocs Material
* BookStack
* Langfuse
* Ragas
* Guardrails AI or NeMo Guardrails
* LangGraph
* NATS
* GrowthBook
* Chatwoot
* Twenty CRM
* Vaultwarden
* Smallstep Step-CA




