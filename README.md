# BOT de Coleta de Cotações NASDAQ100

O bot alimenta um cache com validade de 5 minutos com as 5 ações com maiores altas no momento relacionadas no NASDAQ100.

## Como utilizar

O bot utiliza-se um == python virtual env ==, as bibliotecas utilizadas constam no arquivo requirements.txt e devem seguir o processo de instalação de ambientes pip:
python -m venv venv
venv\Scripts\Active.ps1
pip install requirements.txt

## Docker

Para boa execução do código é == necessário a execução de dois containers docker == (Redis + Standalone Chrome):

docker run --name redis -e ALLOW_EMPTY_PASSWORD=yes -p 6379:6379 bitnami/redis:latest

docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome