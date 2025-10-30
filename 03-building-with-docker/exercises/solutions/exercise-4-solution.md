## Solution: Exercise 4 (Publish Your Server)

1) Log in and tag the image
```bash
docker login
docker tag practical-mcp-server:latest yourname/practical-mcp-server:latest
```

2) Push
```bash
docker push yourname/practical-mcp-server:latest
```

3) Test pull on another machine
```bash
docker pull yourname/practical-mcp-server:latest
```


