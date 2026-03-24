# AI Drift Detect Pipeline

This project detects Terraform drift, analyzes it with AI, takes human-approved action, and stores audit logs in MongoDB Atlas.

## What This Project Achieves

- Detects infrastructure drift using native Terraform plan output.
- Uses Claude API to classify drift and suggest KEEP/REVERT.
- Requires human decision before final action.
- Executes Terraform action only when decision requires it.
- Stores full pipeline audit data in MongoDB Atlas.
- Runs end-to-end with a single command.

## End-to-End Flow

1. **Stage 2 - Drift Detection**
   - Runs `terraform plan -out=tfplan` inside `terraform/`
   - Runs `terraform show -json tfplan`
   - Saves output to `logs/drift.json`

2. **Stage 3 - AI Analysis**
   - Reads `logs/drift.json`
   - Calls Claude API via REST
   - Saves response to `logs/ai_response.json`

3. **Stage 4 - Decision + Approval CLI**
   - Shows AI decision and reason
   - Prompts user for `KEEP` or `REVERT`
   - If `KEEP`, asks approval (`yes/no`)

4. **Stage 5 - Execute + Atlas Logging**
   - If `REVERT`, runs `terraform apply -auto-approve`
   - If `KEEP`, skips Terraform change
   - Logs one document to MongoDB Atlas:
     - `drift`
     - `ai_response`
     - `decision`
     - `timestamp`

5. **Stage 6 - Orchestrator**
   - Runs stages in order from one entrypoint.

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
- MongoDB Atlas cluster + user
- Anthropic API key

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create local env file from template:

```bash
cp .env.example .env
```

3. Fill `.env` with real values.

## Environment Variables

Use these keys in `.env`:

- `CLAUDE_API_KEY`
- `MONGO_URI`
- `MONGO_DB_NAME`
- `MONGO_COLLECTION_NAME`

## Run The Full Pipeline

From project root (`AI/Drift-Detect`):

```bash
python -m backend.main
```

## Expected Outputs

- `logs/drift.json` generated from Terraform plan
- `logs/ai_response.json` generated from Claude analysis
- CLI asks final action (`KEEP/REVERT`)
- MongoDB Atlas gets one pipeline audit document

## Security Notes

- Never commit `.env` with real secrets.
- Rotate API keys/passwords if they are exposed.
- Keep MongoDB user least-privilege for this project.
