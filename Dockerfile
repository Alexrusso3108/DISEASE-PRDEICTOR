FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PREDICTIONS_DB_PATH=/data/predictions.db

RUN useradd -m -u 1000 user

WORKDIR /home/user/app

COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

RUN mkdir -p /data \
    && chown -R user:user /data /home/user/app

USER user

EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
