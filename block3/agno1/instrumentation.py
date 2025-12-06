import os
############### Instrumentation with OpenTelemetry ###############
#
# pip install openinference-instrumentation-agno
# pip install opentelemetry-exporter-otlp-proto-http 
#
############################################################
from openinference.instrumentation.agno import AgnoInstrumentor

# OpenTelemetry imports for observability
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

ENDPOINT = os.getenv("OPEN_TELEMETRY_ENDPOINT", "http://127.0.0.1:6006/v1/traces")

def instrument(service_name: str, service_version: str, project_name: str):

    # Set up the OpenTelemetry tracer provider
    resource = Resource.create(
        {
            "service.name": service_name,
            "service.version": service_version,
            "openinference.project.name": project_name,
        }
    )
    tracer_provider = TracerProvider(resource=resource)

    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(ENDPOINT)))

    # Optionally, you can also print the spans to the console.
    # tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(tracer_provider=tracer_provider)

    # Start instrumenting agno
    AgnoInstrumentor().instrument()