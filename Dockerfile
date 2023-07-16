FROM huggingface/transformers-pytorch-cpu
RUN apt update && \
    apt install -y gcc musl-dev python3-dev gfortran g++ gcc libxslt-dev 
RUN mkdir /app
COPY ./myrtle /app/myrtle/
COPY pyproject.toml /app
COPY ./data/processed/processed_quotes.csv /app/data/processed/processed_quotes.csv
COPY README.md /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# Run dagster gRPC server on port 4000

EXPOSE 8000

CMD ["poetry", "run", "start"]