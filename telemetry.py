import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from comprehend_telemetry import ComprehendDevSpanProcessor

token = os.getenv("COMPREHEND_SDK_TOKEN")
if not token:
    raise RuntimeError("COMPREHEND_SDK_TOKEN must be set in the environment before importing telemetry")

resource = Resource.create({
    "service.name": "petstore-frontend",
    "deployment.environment": os.getenv("OTEL_ENVIRONMENT", "prod"),
})

span_processor = ComprehendDevSpanProcessor(
    organization="bijan-sandbox",
    token=token,
    debug=False,
)

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(span_processor)

current_tracer_provider = trace.get_tracer_provider()
if current_tracer_provider.__class__.__name__ == "ProxyTracerProvider":
    trace.set_tracer_provider(tracer_provider)
else:
    if hasattr(current_tracer_provider, "add_span_processor"):
        current_tracer_provider.add_span_processor(span_processor)