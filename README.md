# AI Drift Detect Pipeline

An end-to-end Python workflow that detects Terraform drift, asks AI for risk-aware guidance, requires human approval, executes the final infrastructure action, and stores an audit record in MongoDB Atlas.

## Why This Project Exists

Terraform drift is common in real cloud environments because manual console changes, provider-side defaults, and lifecycle updates can move infrastructure away from IaC state.

This project adds a practical control loop:

- detect drift with native Terraform output
- analyze drift with AI for fast context
- keep a human in control of final action
- apply or skip changes safely
- store every run as an auditable record

## Architecture Flow

```mermaid
flowchart TD
    A[Stage 2: Terraform Plan] --> B[logs/drift.json]
    B --> C[Stage 3: Claude AI Analysis]
    C --> D[logs/ai_response.json]
    D --> E[Stage 4: User Decision CLI]
    E -->|KEEP| F[Skip Terraform Apply]
    E -->|REVERT| G[terraform apply -auto-approve]
    F --> H[Stage 5: MongoDB Atlas Logging]
    G --> H
    H --> I[Stage 6: Single Orchestrator Entry]
```

## What Each Stage Does

### Stage 2 - Drift Detection (`backend/plan/planner.py`)

- Runs `terraform plan -out=tfplan` in `terraform/`
- Runs `terraform show -json tfplan`
- Saves machine-readable drift data to `logs/drift.json`

### Stage 3 - AI Analysis (`backend/ai/claude_client.py`)

- Reads `logs/drift.json`
- Sends drift payload to Claude via REST API
- Receives structured recommendation (`KEEP`/`REVERT` + reasoning)
- Saves response in `logs/ai_response.json`

### Stage 4 - Decision + Approval (`backend/decision/decision_engine.py`)

- Displays AI decision and reason in CLI
- Prompts operator for final choice: `KEEP` or `REVERT`
- If `KEEP`, asks approval (`yes`/`no`)
- Returns normalized decision object

### Stage 5 - Execution + Atlas Logging (`backend/executor/terraform_executor.py`)

- Reads drift and AI outputs
- Uses Stage 4 decision
- If action is `revert`: runs `terraform apply -auto-approve`
- If action is `keep`: prints `Keeping current infrastructure`
- Inserts one audit document in MongoDB Atlas:
  - `drift`
  - `ai_response`
  - `decision`
  - `timestamp`

### Stage 6 - Orchestrator (`backend/main.py`)

- Runs Stages 2 -> 3 -> 5 (Stage 4 is called by Stage 5)
- Provides a single-command pipeline run

## Project Structure

```text
AI/Drift-Detect/
├── backend/
│   ├── ai/
│   │   └── claude_client.py
│   ├── decision/
│   │   └── decision_engine.py
│   ├── db/
│   │   ├── mongo_client.py
│   │   └── logger.py
│   ├── executor/
│   │   └── terraform_executor.py
│   ├── plan/
│   │   └── planner.py
│   ├── config.py
│   └── main.py
├── logs/
├── terraform/
├── .env
├── .env.example
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- Terraform installed and available in PATH
- MongoDB Atlas cluster and DB user
- Anthropic API key

## Setup

1) Install dependencies:

```bash
pip install -r requirements.txt
```

2) Create local environment file from template:

```bash
cp .env.example .env
```

3) Fill `.env` values.

## Environment Variables

Configure these keys in `.env`:

- `CLAUDE_API_KEY`
- `MONGO_URI`
- `MONGO_DB_NAME`
- `MONGO_COLLECTION_NAME`

Example (do not commit real values):

```env
CLAUDE_API_KEY=your_claude_api_key
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=srikanth
MONGO_COLLECTION_NAME=pipeline_logs
```

## How to Run

From project root (`AI/Drift-Detect`):

```bash
python -m backend.main
```

The pipeline will:

1. generate drift output
2. generate AI analysis
3. ask for your decision
4. execute Terraform action based on decision
5. store run data in MongoDB Atlas

## Expected Outputs

- `logs/drift.json`
- `logs/ai_response.json`
- CLI decision result (`KEEP`/`REVERT`)
- MongoDB Atlas document in configured collection

## Sample Audit Document

```json
{
  "drift": { "format_version": "1.2" },
  "ai_response": { "id": "msg_xxx" },
  "decision": { "action": "keep", "approved": true },
  "timestamp": "2026-03-24T10:20:30.000000+00:00"
}
```

## Troubleshooting Quick Guide

- `CLAUDE_API_KEY is not set`:
  - fix `.env` format (`KEY=value`, no spaces)
- Claude `404 model not found`:
  - use a model available for your Anthropic account
- Claude `429`:
  - wait and retry; reduce payload frequency
- Mongo `authentication failed`:
  - verify URI username/password and Atlas network access
- CLI appears frozen:
  - use PowerShell (interactive prompts are more reliable on Windows)

## Security Notes

- Never commit `.env` with real secrets.
- Rotate keys immediately if exposed.
- Use least-privilege MongoDB users for production.
