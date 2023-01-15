
ecr-login:
	aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 601394826940.dkr.ecr.us-west-2.amazonaws.com

build:
	docker build -t 601394826940.dkr.ecr.us-west-2.amazonaws.com/dynamic-dns --platform  .

push: ecr-login build
	docker push 601394826940.dkr.ecr.us-west-2.amazonaws.com/dynamic-dns

develop: build
	docker run -it --rm \
		-v ${PWD}:/app \
		-v ${HOME}/.aws:/root/.aws:ro \
		-w /app \
		--entrypoint /bin/sh \
		-e HOSTED_ZONE=kloudcover.com \
		-e DOMAIN_NAME=home.kloudcover.com \
		601394826940.dkr.ecr.us-west-2.amazonaws.com/dynamic-dns


test: build
	docker run -it --rm \
	-v ${HOME}/.aws:/root/.aws:ro \
	-e HOSTED_ZONE=kloudcover.com \
	-e DOMAIN_NAME=home.kloudcover.com \
	601394826940.dkr.ecr.us-west-2.amazonaws.com/dynamic-dns