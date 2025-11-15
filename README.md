# OneTeam FSM Demo API

A simple FastAPI backend for maintenance requests.

## Run locally

1. Clone repo
2. Create virtual environment
3. Install dependencies
4. Run server
5. Test endpoints

### Commands

```bash
# Clone repo
git clone YOUR_REPO_URL
cd YOUR_REPO_NAME

# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn server:app --reload
