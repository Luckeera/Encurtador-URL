# Encurtador de URL Django

Um projeto simples de encurtador de URL construído com Django.

## Visão Geral

Este projeto implementa um serviço básico para encurtar URLs longas, gerar códigos curtos únicos e redirecionar usuários para a URL original.

## Funcionalidades

- Encurtar URLs longas.
- Gerar códigos curtos únicos.
- Redirecionar do código curto para a URL original.
- Páginas para links expirados ou não encontrados.
- Interface administrativa básica do Django.

## Pré-requisitos

Para executar este projeto, você precisa ter o Docker e o Docker Compose instalados em sua máquina.

- [Instalar Docker](https://docs.docker.com/get-docker/)
- [Instalar Docker Compose](https://docs.docker.com/compose/install/)

## Configuração e Execução com Docker Compose

Siga os passos abaixo para configurar e executar o projeto usando Docker Compose:

1.  **Clone o Repositório** (Se aplicável, caso contrário, navegue até a pasta do projeto).

2.  **Crie o arquivo `requirements.txt`**:
    Certifique-se de que o arquivo `requirements.txt` na raiz do projeto liste todas as dependências Python necessárias. Um exemplo básico está incluído na documentação.

3.  **Construa a Imagem Docker**:
    Abra o terminal na raiz do projeto (onde estão o `Dockerfile` e `docker-compose.yml`) e execute:
