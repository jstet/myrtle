FROM debian:bookworm-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3-pip default-jdk curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir /app
COPY ./myrtle /app/myrtle/
COPY pyproject.toml /app
COPY ./data/processed/processed_quotes.csv /app/data/processed/processed_quotes.csv
COPY README.md /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry install --only main
RUN export PRODUCTION=True

CMD ["/root/.local/bin/poetry", "run", "start"]