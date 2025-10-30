## Exercise 4 (Optional, Advanced): Publish Your Server

Goal: Push one of your servers to a container registry (e.g., Docker Hub).

Requirements:
- Create a repository on Docker Hub
- Tag your image as `username/repo:tag`
- `docker push username/repo:tag`

Hints:
- `docker login` first
- Use a minimal `README` on Docker Hub describing your MCP tools
- Follow best practices: pinned base images, small layers

Expected outcome:
- Your image is publicly accessible on Docker Hub and pullable by others


