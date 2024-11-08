from prometheus_client import Counter, Histogram, start_http_server

# Start Prometheus metrics server
start_http_server(8001)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    "fastapi_request_count",
    "Total number of HTTP requests",
    ["example_app", "method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "fastapi_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["example_app", "endpoint"]
)

# Middleware to collect metrics
def metrics_middleware(app, app_name):
    @app.middleware("http")
    async def add_metrics(request, call_next):
        import time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(request.method)

        # Update Prometheus metrics
        REQUEST_COUNT.labels(app_name, request.method, request.url.path, response.status_code).inc()
        REQUEST_LATENCY.labels(app_name, request.url.path).observe(process_time)
        
        return response

    return app