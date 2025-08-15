# MLX Whisper API

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/duytechie/mlx-api.git
cd mlx-api
```

### 2. Install `uv` (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Install necessary packages

```bash
uv sync
```

### 4. Run the server

```bash
uv run main.py
```

### 5. Usage

API Enpoints:

- `POST /v1/audio/transcriptions`: Upload audio file for transcription
- `GET /v1/models`: List all models

Check the `docs` on `localhost:8000/docs`
