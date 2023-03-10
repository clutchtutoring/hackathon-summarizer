# Summarizer Backend

This is a transcriber/summarizer application built for the P+ hackathon.

## Installation

### Development

1. Install ffmpeg:

Use `apt`, `dnf`, `brew` (or any other package manager) to install ffmpeg, then check the version:

```bash
$ ffmpeg
ffmpeg version 4.2.4-1ubuntu0.1 Copyright (c) 2000-2020 the FFmpeg developers
  built with gcc 9 (Ubuntu 9.3.0-10ubuntu2)
```

2. This project requires python >= `3.10`, so you will need to install python first using `pyenv` or the official installer.

3. Create a virtual environment:
```
python3 -m venv .venv
```

4. Enter the virtual environment:
```
source .venv/bin/activate
```

5. Install dependencies with pip:
```
pip install openai-whisper rq "fastapi[all]" farm-haystack pySmartDL ffmpeg-python
```

6. Download ML models:
```
python3 download_models.py
```

## Usage

### Development

1. Start the redis service:

* If you already have a local redis server you can skip this step. 

```
docker-compose up -d
```

2. Run the local server:
```
source ./start-app.sh
```

3. In another terminal run the worker:
```
source ./start-worker.sh
```
4. Go to the openapi specification:
```
http://localhost:8000/docs
```