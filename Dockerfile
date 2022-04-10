FROM python:3.8-alpine

EXPOSE 8000

COPY ./packages.txt .
RUN pip install -r ./packages.txt

COPY ./app .

CMD python -m aiohttp.web -H localhost -P 8000 main:init_app