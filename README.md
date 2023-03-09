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

4. Install dependencies with pip:
```
pip install -r requirements.txt
```

## Usage

### Development

5. Start the redis service:
```
docker-compose up -d
```

6. Run the local server:
```
source ./start-app.sh
```

7. In another terminal run the worker:
```
source ./start-worker.sh
```