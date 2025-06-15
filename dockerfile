# Usa uma imagem base oficial do Python
FROM python:3.11-slim

# Define variáveis de ambiente para o Python
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
# Usamos COPY . . para copiar todos os arquivos do projeto para o WORKDIR
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . /app/

# Executa as migrações do banco de dados e coleta arquivos estáticos
# Note: Para SQLite, o db.sqlite3 será criado no volume mapeado
# Para produção, você pode precisar de um script de entrada que rode isso
# antes de iniciar o servidor web
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Expõe a porta em que a aplicação Django será executada (Gunicorn padrão é 8000)
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
# Substitua 'url_shortener_project.wsgi:application' pelo caminho correto do seu arquivo wsgi.py
CMD ["gunicorn", "url_shortener_project.wsgi:application", "--bind", "0.0.0.0:8000"]
