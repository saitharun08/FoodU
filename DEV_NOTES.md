Run Redis locally:
# Docker
docker run -p 6379:6379 -d redis:7

Then update .env REDIS_URL=redis://127.0.0.1:6379
