import os
import fastapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# OpenTelemetry imports for observability
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

ENDPOINT = os.getenv("OPEN_TELEMETRY_ENDPOINT", "http://127.0.0.1:6006/v1/traces")

# Set up the OpenTelemetry tracer provider
resource = Resource.create(
    {
        "service.name": "my_service_name",
        "service.version": "0.0.1",
        "openinference.project.name": "my_project_name",
    }
)
tracer_provider = TracerProvider(resource=resource)

tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(ENDPOINT)))

app = fastapi.FastAPI()

@app.get("/foobar")
async def foobar():
    return {"message": "hello world"}

FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)