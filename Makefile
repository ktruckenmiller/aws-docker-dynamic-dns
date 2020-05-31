
develop: build
	docker run -it --rm \
		-v ${PWD}:/app \
		-w /app \
		-e IAM_ROLE \
		ktruckenmiller/aws-docker-dynamic-dns bash

build:
	docker build -t ktruckenmiller/aws-docker-dynamic-dns .

build-test:
	docker build -t ktruckenmiller/aws-docker-dynamic-dns:test .

test:
	docker run -it --rm \
	-v ${PWD}:/app \
	-w /app \
	-e IAM_ROLE \
	ktruckenmiller/aws-docker-dynamic-dns:test
