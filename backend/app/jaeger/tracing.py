from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from app.config import constants

# Configure resource with service name
resource = Resource(attributes={"service.name": constants.JAEGER_FASTAPI_SERVICE})

# Create TracerProvider
tracer_provider = TracerProvider(resource=resource)

# Create OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=constants.JAEGER_SERVICE_DOMAIN, # !!! jaeger server domain
    insecure=True  # Set to False if using HTTPS
)

# Create and add span processor to the tracer provider
class CustomSpanProcessor(BatchSpanProcessor):
    def on_end(self, span):
        for k, v in span.attributes.items():
            if (k=="asgi.event.type" and v in {"http.request", "http.response.body", "http.response.start", "http.disconnect", "websocket.send", "websocket.receive", "websocket.accept", "websocket.connect"}):
                return

        super().on_end(span)
span_processor = CustomSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

trace.set_tracer_provider(tracer_provider)

# Get tracers
fastapi_tracer = trace.get_tracer(constants.JAEGER_FASTAPI_SERVICE)