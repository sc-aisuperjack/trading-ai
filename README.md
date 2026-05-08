# Simple Cognizant Trading AI Assistant

Tiny, clean Streamlit version.

This is deliberately small so it can be demoed quickly.

## Run on Windows

Double-click:

```text
run.bat
```

## Run on Mac/Linux

```bash
chmod +x run.sh
./run.sh
```

## Optional OpenAI

The app works without OpenAI.

To enable OpenAI:

1. Open `.env`.
2. Set:

```bash
USE_OPENAI=true
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

3. Restart the app.

## Demo path

1. Dashboard.
2. Monday brief.
3. Teams chat question: Why did dresses underperform this week?
4. Teams chat question: What will revenue be next week?
5. Show citation guard.
6. Show architecture.
