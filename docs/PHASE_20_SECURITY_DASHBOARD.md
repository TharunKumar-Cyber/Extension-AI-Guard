# Phase 20 — Security Dashboard

## 1. Phase Overview

Phase 20 introduces the Security Dashboard for Extension AI Guard (EAG).

The dashboard will provide an authenticated web interface for viewing security status, network-request analysis results, alerts, security events, Aegis information, and backend health.

Phase 20 is an integration and presentation phase. It must consume the existing Phase 19 backend contracts and must not silently recreate or replace the Phase 13–19 detection pipeline.

The dashboard must distinguish measured backend data from empty-state or unavailable data. It must not fabricate historical security metrics.

---

## 2. Relationship to the EAG Roadmap

The Phase 20 workflow is:

```text
Phase 13
Feature Contract
     ↓
Phase 14
Classical ML
     ↓
Phase 18
Real-Time Detection
     ↓
Phase 19
Backend API
     ↓
Phase 20
Security Dashboard
     ↓
Phase 21
n8n Automation
     ↓
Phase 22
Telegram Alerting
```

Phase 20 consumes the authentication, Aegis, detection, alert, security-event, and health capabilities established by Phase 19.

---

## 3. Phase 19 Backend Contract

The existing backend exposes:

### General API

- `GET /api/status`
- `GET /api/database-status`
- `POST /api/network-requests`

### Authentication

- `POST /api/auth/register`
- `POST /api/auth/login`

### Aegis

- `GET /api/aegis/welcome`
- `GET /api/aegis/status`
- `POST /api/aegis/onboarding/start`
- `POST /api/aegis/onboarding/step`
- `POST /api/aegis/onboarding/complete`
- `POST /api/aegis/message`
- `GET /api/aegis/knowledge`
- `GET /api/aegis/alerts/explain`

The dashboard must use these contracts as the starting integration boundary.

---

## 4. Dashboard Data Limitation

Phase 19 currently provides a network-request analysis operation but does not provide a dedicated historical dashboard read API.

Therefore Phase 20 must not invent:

- historical alert counts
- historical malicious-request counts
- historical benign-request counts
- historical security-event totals
- time-series metrics
- model-performance statistics

until the backend actually provides those values.

Where historical data is unavailable, the dashboard must show an explicit empty/unavailable state.

---

## 5. Dashboard Objective

The dashboard should answer the following operational questions:

1. Is the EAG backend online?
2. Is the database available?
3. Is the authenticated user session active?
4. Is Aegis onboarding complete?
5. What security information is currently available?
6. What happened in the latest submitted network-request analysis?
7. Are there alerts requiring attention?
8. What security events are currently available?
9. Can Aegis explain a security alert?
10. Is the dashboard receiving valid backend responses?

---

## 6. Frontend Location

The dashboard frontend will be implemented under:

```text
frontend/
```

The frontend implementation now exists under frontend/ as a React + TypeScript + Vite application with Tailwind CSS 4 integration. The repository also contains the Phase 20 backend persistence and dashboard-read boundary.

The frontend must remain separate from the FastAPI backend.

---

## 7. Proposed Frontend Stack

The initial implementation will use:

- React 19.2.8
- TypeScript 6.0.2
- Vite 8.3.x
- Tailwind CSS 4.3.3
- @tailwindcss/vite 4.3.3
- Oxlint 1.81.x

The actual installed versions must be verified during implementation rather than assumed.

The dashboard must be runnable locally through a documented development command.

---

## 8. Application Structure

The proposed frontend structure is:

```text
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── auth.ts
│   │   ├── aegis.ts
│   │   └── security.ts
│   │
│   ├── components/
│   │   ├── layout/
│   │   ├── navigation/
│   │   ├── cards/
│   │   ├── tables/
│   │   ├── alerts/
│   │   └── aegis/
│   │
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── Dashboard.tsx
│   │
│   ├── types/
│   │   ├── auth.ts
│   │   ├── security.ts
│   │   └── aegis.ts
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

The exact structure may be adjusted during implementation if required by the verified toolchain.

---

## 9. Authentication Flow

The dashboard will use the Phase 19 JWT authentication API.

Flow:

```text
Login Form
    ↓
POST /api/auth/login
    ↓
Access Token
    ↓
Authenticated Client State
    ↓
Protected Dashboard APIs
```

The frontend must:

- validate required login fields
- send credentials only to the configured backend
- store the access token using a documented client-side strategy
- attach the token to protected API requests
- handle authentication failure
- prevent protected dashboard access without a valid session
- provide logout behavior

The frontend must never display or log the JWT secret.

---

## 10. Registration Flow

Registration will use:

```text
POST /api/auth/register
```

The UI will collect:

- username
- email
- password

The frontend must display backend validation or registration errors without exposing internal implementation details.

---

## 11. Dashboard Layout

The main dashboard will contain:

### Header

- EAG identity
- authenticated user information
- backend/session status
- logout control

### Navigation

Initial navigation:

- Overview
- Detection
- Alerts
- Security Events
- Aegis
- System Status

### Main content

The Overview page will provide the current verified operational state.

---

## 12. Overview Cards

Initial cards:

### Backend Status

Source:

```text
GET /api/status
```

### Database Status

Source:

```text
GET /api/database-status
```

### Aegis Status

Source:

```text
GET /api/aegis/status
```

### Current Security State

This card may summarize currently available detection information, but must not represent unavailable historical data as measured statistics.

---

## 13. Detection Interface

The Detection page will provide a controlled interface for submitting a network request to the existing backend analysis endpoint.

Input fields:

- request ID
- URL
- HTTP method
- domain
- timestamp

Endpoint:

```text
POST /api/network-requests
```

The response must display:

- request information
- malicious/benign classification
- confidence
- threat type
- explanation
- alert when present
- security event

The dashboard must preserve the distinction between the backend's current rule-based Phase 19 analysis and the ML/realtime work completed in earlier phases.

---

## 14. Alert Interface

The Alerts view will display alert information returned by the backend.

Current Phase 19 malicious alert contract includes:

- alert ID
- result ID
- severity
- title
- message
- creation timestamp

A malicious request currently produces a high-severity alert.

Because Phase 19 does not yet expose a historical alert-list endpoint, the dashboard must not claim to show all historical alerts.

---

## 15. Security Events Interface

The Security Events view will display security-event information available from current dashboard operations.

Current event contract includes:

- event ID
- event type
- source
- severity
- description
- timestamp

Until a historical event-list endpoint exists, the UI must use an explicit empty/unavailable state rather than fabricate an event history.

---

## 16. Aegis Interface

The Aegis view will integrate:

- welcome information
- onboarding status
- onboarding progress
- knowledge information
- Aegis messages
- alert explanations

Protected Aegis endpoints must receive the authenticated JWT.

The UI must clearly distinguish:

- onboarding state
- informational responses
- security-alert explanations

---

## 17. System Status

The System Status page will provide:

- backend status
- database status
- authentication/session state
- Aegis state
- frontend/backend connectivity state

Errors must identify the affected service without exposing secrets, stack traces, or sensitive configuration.

---

## 18. API Client Design

The frontend will use a centralized API client.

Responsibilities:

- base backend URL configuration
- JSON request handling
- JWT attachment
- response parsing
- common error handling
- authentication failure handling
- timeout behavior where appropriate

API modules should remain separated by domain:

```text
api/client.ts
api/auth.ts
api/security.ts
api/aegis.ts
```

---

## 19. Environment Configuration

The frontend backend URL must be configurable through an environment variable.

The implementation must not hard-code a production API hostname.

Development configuration may point to the local FastAPI server.

Secrets must not be placed in frontend environment variables unless they are explicitly designed to be public client configuration values.

---

## 20. Security Requirements

The dashboard must implement:

- authenticated access to protected pages
- JWT attachment to protected requests
- no JWT secret exposure
- no password logging
- no sensitive backend configuration display
- safe error messages
- client-side input validation
- backend validation remains authoritative
- controlled rendering of backend response content
- logout/session cleanup
- no unsafe HTML injection

The dashboard is a security product interface, so UI convenience must not weaken the existing backend security boundary.

---

## 21. Empty, Loading, and Error States

Every backend-driven component must define:

### Loading

Show a clear loading state while waiting for the API.

### Empty

If the backend has no data or does not provide historical data, show an explicit empty-state message.

### Error

Show a concise service-specific error and provide a retry path where appropriate.

The UI must never replace unavailable values with invented zeros or synthetic historical values.

---

## 22. Responsive Design

The dashboard must support:

- desktop
- laptop
- tablet
- mobile-width layouts

Security information must remain readable at smaller widths.

Tables should support horizontal scrolling or responsive presentation rather than clipping critical values.

---

## 23. Accessibility

The frontend should provide:

- semantic HTML
- keyboard-accessible controls
- visible focus states
- meaningful labels
- accessible button names
- sufficient text contrast
- status/error messaging understandable without color alone

---

## 24. Testing Strategy

Phase 20 testing will cover:

### Frontend tests

- component rendering
- login validation
- registration validation
- API client behavior
- protected-route behavior
- dashboard loading states
- empty states
- error states
- logout behavior

### Integration tests

- frontend authentication against Phase 19 API
- authenticated Aegis access
- network-request analysis submission
- backend/database status retrieval

### Build verification

The frontend must:

- install successfully
- build successfully
- start successfully in development mode
- contain no TypeScript compilation errors

---

## 25. Dashboard Metrics Policy

Phase 20 must not display fabricated metrics.

The following may be displayed only when backed by an actual API response:

- request counts
- malicious counts
- benign counts
- alert counts
- event counts
- confidence values
- timestamps
- severity distributions
- historical charts

The dashboard may display static explanatory labels or capability descriptions, but these must be clearly distinguishable from measured data.

---

## 26. Phase 20 Backend Extension

Because Phase 19 does not expose historical read endpoints, Phase 20 may add dedicated dashboard read APIs where required.

Potential read endpoints include:

```text
GET /api/dashboard/summary
GET /api/dashboard/detections
GET /api/dashboard/alerts
GET /api/dashboard/security-events
```

These are proposed interfaces, not yet implemented contracts.

Any new endpoint must:

- be documented
- have Pydantic response models
- enforce authentication where appropriate
- use actual persisted data
- include tests
- avoid changing existing Phase 19 contracts unnecessarily

If persistent historical storage is required, the database model and migration/change strategy must be documented before implementation.

---

## 27. Data Ownership

Phase 20 must preserve clear ownership:

```text
Frontend
    ↓ presentation + user interaction

Backend API
    ↓ validation + authentication + orchestration

Security Services
    ↓ detection + alert/event generation

Database
    ↓ persistence
```

The frontend must not independently implement security-detection rules.

---

## 28. No Duplicate Detection Logic

The dashboard must not recreate the Phase 19 suspicious-domain rules in TypeScript.

The backend remains authoritative for security classification.

The frontend displays backend results.

---

## 29. Performance

Initial performance goals:

- avoid unnecessary API calls
- centralize request handling
- avoid repeated dashboard polling unless explicitly required
- lazy-load nonessential dashboard sections where useful
- keep initial bundle reasonable
- prevent unnecessary component rerenders

Real-time streaming is not part of the Phase 20 baseline unless explicitly introduced as a controlled extension.

---

## 30. Logging

Frontend logs must not contain:

- passwords
- JWT secrets
- authorization headers
- sensitive environment values

Development diagnostics may be enabled locally but must not expose authentication material.

---

## 31. Phase 20 Artifacts

Implemented/expected artifacts:

```text
docs/
└── PHASE_20_SECURITY_DASHBOARD.md

frontend/
├── package.json
├── src/
├── configuration
└── README.md

backend/
├── app/api/dashboard.py
├── app/models/dashboard_records.py
├── app/models/dashboard_schemas.py
└── persisted dashboard records for requests, detections, alerts, and events

.github/
└── workflows/phase20.yml

backend/results/
└── phase20_metadata.json
```

The exact artifact set will follow the implementation actually completed.

---

## 32. Phase 20 Experiments and Verification

### Experiment A — Frontend Build

Verify that the dashboard installs and builds successfully.

### Experiment B — Authentication

Verify registration, login, protected requests, and logout.

### Experiment C — System Status

Verify backend and database status display.

### Experiment D — Detection

Submit controlled network requests and verify that the dashboard displays the backend detection result.

### Experiment E — Alert Handling

Submit a controlled suspicious-domain request and verify that the returned high-severity alert is displayed.

### Experiment F — Aegis

Verify authenticated Aegis status, onboarding, knowledge, messaging, and alert explanation.

### Experiment G — Error/Empty States

Verify unavailable historical data is presented honestly without fabricated metrics.

---

## 33. Reproducibility Metadata

Phase 20 metadata must record:

- phase
- experiment ID
- timestamp
- frontend framework/version
- Node version
- npm version
- backend version
- API contract version
- browser/test environment
- build result
- test result
- dashboard capabilities implemented
- backend endpoints added
- known limitations

---

## 34. Completion Criteria

Phase 20 is complete only when:

- [ ] Phase 20 documentation is committed.
- [ ] Frontend toolchain is verified.
- [ ] Dashboard structure is implemented.
- [ ] Authentication UI is implemented.
- [ ] JWT session handling is implemented.
- [ ] Dashboard overview is implemented.
- [ ] Backend/database status is displayed.
- [ ] Detection interface is implemented.
- [ ] Alert interface is implemented.
- [ ] Security-event interface is implemented.
- [ ] Aegis integration is implemented.
- [ ] Loading states are implemented.
- [ ] Empty states are implemented.
- [ ] Error states are implemented.
- [x] Required backend read APIs are implemented.
- [ ] Required backend read APIs are locally/CI verified.
- [ ] Frontend lint passes.
- [ ] Backend tests pass.
- [ ] Production build succeeds.
- [x] Phase 20 metadata is generated.
- [x] Results and limitations are documented.
- [ ] Phase 21 handoff is documented.
- [ ] Git working tree is clean.
- [ ] Phase 20 changes are committed and pushed.

---

## 35. Phase 21 Handoff

Phase 20 will provide a web-based security interface that can consume authenticated EAG backend services.

Phase 21 will build on this foundation by integrating n8n automation workflows.

The dashboard should therefore expose stable API boundaries without coupling the UI directly to future automation implementation details.

---

## 36. Research and Engineering Conclusion

Phase 20 establishes the Security Dashboard as the presentation and operational interface for Extension AI Guard.

The dashboard will integrate the verified Phase 19 authentication, Aegis, network-request analysis, detection, alert, security-event, and health contracts.

Where Phase 19 does not provide historical read data, Phase 20 will add authenticated, tested read/aggregation APIs rather than fabricating dashboard metrics.

The phase therefore maintains the EAG principle of traceable, reproducible, and evidence-based security results while providing the user-facing interface required for subsequent automation and alerting phases.


## 37. Implementation Status — 2026-09-29

The Phase 20 repository implementation has been carried out through the connected GitHub repository.

Implemented:

- React + TypeScript + Vite frontend under frontend/.
- Tailwind CSS 4 using the official Vite plugin integration.
- Centralized frontend API client with JWT attachment and authentication failure cleanup.
- Login and registration UI.
- Responsive dashboard navigation for Overview, Detection, Alerts, Security Events, Aegis, and System Status.
- Loading, empty, and service-error states.
- Phase 19 network-request analysis integration.
- Persistent SQLite records for dashboard requests, detections, alerts, and security events.
- Authenticated dashboard read APIs for summary, detections, alerts, and security events.
- Local development CORS configuration for the Vite frontend.
- GitHub Actions workflow covering backend compilation/API registration and frontend lint/build.

Verification limitation:

The connected GitHub tooling can create and inspect repository files, but it does not provide a local Windows process for executing the user's exact EAG environment. The Phase 20 implementation is therefore not marked fully complete until the repository's actual environment verifies the frontend build/lint and backend test suite. The workflow file has been added for automated verification, but no successful workflow run was available from the connected GitHub tooling at the time of documentation.

This status deliberately avoids claiming a successful build or test result that has not been observed.
