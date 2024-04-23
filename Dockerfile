FROM python:3.11

ADD app.py .
ADD requirements.txt .
RUN python -m venv .venv
COPY . .
RUN . .venv/bin/activate

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]



