# Girl Math VIP

A playful mobile-friendly Streamlit app for the Girl Math Hair Salon VIP pass experience.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501`.

## Deploy options

### Streamlit Community Cloud
1. Push this repo to GitHub.
2. Create a new app in Streamlit Community Cloud.
3. Set the entrypoint to `app.py`.

### Docker

```bash
docker build -t girl-math .
docker run -p 8501:8501 girl-math
```

## What changed
- Better mobile spacing and responsive styling
- Cleaner card-based layout
- Safer name-tag preview rendering
- Deployment files for Streamlit and Docker
