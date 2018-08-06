#!/bin/sh
docker build -t refresh .
docker run -it --rm -v $(pwd):/work -v ~/.aws:/root/.aws:ro refresh
