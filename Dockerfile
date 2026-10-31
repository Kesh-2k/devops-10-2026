FROM python:3.12-slim

WORKDIR /srv

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Mesma imagem para os dois serviços: APP=app.api:APP (tarefas, 8001)
# ou APP=app.notificacoes:NOTIFICACAO (notificações, 8002).
ENV APP=app.api:APP \
    PORT=8001
EXPOSE 8001 8002

CMD ["sh", "-c", "exec uvicorn \"$APP\" --host 0.0.0.0 --port \"$PORT\""]
