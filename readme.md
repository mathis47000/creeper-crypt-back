# Requirements:
- Python 3.6

# Installation:
- pip install -r requirements.txt

# Usage:
- python app.py

# Description:
- Chat websocket server

# Technologies:
- Python
- Flask
- Flask-SocketIO

# Features:
- Chat with multiple users
- Multiple chat rooms

# Docker:

- Build image:
```bash
docker build -t socketpy .
```

- Run container:
```bash
docker run -p <port_you_want>:5000 socketpy
```

# Or use docker-compose:

- Run container:
```bash
docker-compose up
```