# RevInsight

## Install Requirements.txt using pip
```bash
pip install -r requirements.txt
```

## Generate Fake Data using *scripts/generate_data.py*
```bash
python scripts/generate_data.py
```

- Please use `Makefile` and go through all the commands.
- If you don't have make installed, you can run the commands from the `Makefile` directly.

## Build Container
- `make build` or `docker build -t revinsight:v1 .`

## Run Container
- `make run` or `docker run --rm --name rev-insight -v ./data/:/app/data -it rev-insight:v1 python3 main.py data/orders.csv data/report.xlsx`

## Run Tests
- `make test` or `docker run -it --rm --name rev-insight-test $(IMAGE_NAME) python3 -m pytest -v tests`

## Get Coverage Report
- `make cov` or `docker run -it --rm --name rev-insight-cov $(IMAGE_NAME) python3 -m pytest --cov=app tests/`