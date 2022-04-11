# Vehicle builder

## Launch

- set .env
  - db_url
- build docker image: `docker build -t vehicle_builder`
- run docker container: `docker run -p 8000:8000 --name vehicle_builder --env_file.env vehicle_builder`

## Development

- `pip install -r packages.dev.txt`
- `pre-commit install`
- export envs
  - db_url
  - test_db_url
- `python app/main.py`

## Structure

- app - contains all the source code
- app/api - contains code for HTTP API
- app/service - contains business logics
- app/tests - contains tests, respective to the app structure

## Known issues

- lack of logs
- no api specification
