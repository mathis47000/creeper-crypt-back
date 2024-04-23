FROM python:3.8-slim

ADD app.py .
ADD requirements.txt .
RUN python -m venv .venv
COPY . .
RUN . .venv/bin/activate

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]



