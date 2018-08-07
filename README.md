# aws-docker-dynamic-dns
A docker container to setup dynamic dns at home. Run this on any computer you want to route to. Obviously, you'll have to make sure your router has a DMZ or a port mapping to the host with both 500 + 4500 open. This container will tell your Route53 entry within AWS what your IP Address is at home so that you can route to it if it changes.

```
Problem: I have a domain that I want connected to my dynamic IP.

Solution: If you are using AWS for your domain, you can run this docker container with two variables!
```

### Reason Behind the Tool

The reason I made this was becuase I didn't want to use DynDNS or some other service. I knew it was easy enough to track my dynamic ip at home, and hopefully this is all I need.

### Run the Tool

To run:

`docker run -it --rm -e DOMAIN_NAME='mydomain.something.com' -e HOSTED_ZONE='something.com' -v ~/.aws:/root/.aws:ro ktruckenmiller/aws-docker-dynamic-dns`
