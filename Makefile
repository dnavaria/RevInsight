IMAGE_NAME=rev-insight:v1

all: build

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm --name rev-insight -v $(PWD)/data:/app/data -it $(IMAGE_NAME) python3 main.py data/orders.csv data/report.xlsx

test:
	docker run -it --rm --name rev-insight-test $(IMAGE_NAME) python3 -m pytest -v tests

cov:
	docker run -it --rm --name rev-insight-cov $(IMAGE_NAME) python3 -m pytest --cov=app tests/

clean-test:
	docker stop rev-insight-test

clean:
	docker stop rev-insight
	docker rm rev-insight

clean-image:
	docker rmi $(IMAGE_NAME)

logs:
	docker logs rev-insight

.PHONY: all build run test cov clean-test clean clean-image logs
