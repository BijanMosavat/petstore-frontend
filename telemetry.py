import os
import uuid
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from comprehend_telemetry import ComprehendSDK

resource = Resource.create({
    "service.name": "my-python-service",
    "service.namespace": "production",
    "deployment.environment": "prod",
    "service.instance.id": str(uuid.uuid4()),
})

comprehend = ComprehendSDK(
    organization='comprehend',
    token=os.getenv("COMPREHEND_SDK_TOKEN"),
    # debug=True  # Optional: enable debug logging
)

tracer_provider = TracerProvider(
    resource=resource,
    active_span_processor=comprehend.get_span_processor(),
)
trace.set_tracer_provider(tracer_provider)

meter_provider = MeterProvider(
    resource=resource,
    metric_readers=[
        PeriodicExportingMetricReader(
            comprehend.get_metrics_exporter(),
            export_interval_millis=15000,
        )
    ],
)