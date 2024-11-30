# Use uma imagem base com Python 3.9
FROM python:3.9-slim

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Copie o código para dentro do contêiner
WORKDIR /app
COPY . .

# Instale as dependências do Python
RUN pip install -r requirements.txt

# Execute o backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
