# aws-docker-dynamic-dns
A docker container to setup dynamic dns at home. Run this on any computer you want to route to. Obviously, you'll have to make sure your router has a DMZ or a port mapping to the host with both 500 + 4500 open.


To run:

`docker run -it --rm -e DOMAIN_NAME='mydomain.something.com' -e HOSTED_ZONE='something.com' -v ~/.aws:/root/.aws:ro refresh`
