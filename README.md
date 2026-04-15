# 11402 Data Analytics Project

Visualizes sentiment, platform, emotion, topic, and engagement distributions from a social media AI trends dataset.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Install dependencies:

```bash
uv sync
```

## Run

```bash
uv run main.py
```

Charts are saved to the `result/` folder.
