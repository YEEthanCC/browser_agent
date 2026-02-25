# configs/tracing.py
"""
Azure AI Foundry tracing setup using OpenTelemetry.

Option A: Console exporter (for local debugging)
Option B: Azure Application Insights (requires APPLICATIONINSIGHTS_CONNECTION_STRING in .env)
"""

import atexit
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from configs.settings import Settings

settings = Settings()

_provider = None


def setup_tracing(use_console: bool = True):
    """
    Configure tracing for the browser agent.
    
    Args:
        use_console: If True, exports traces to console. 
                     If False, requires APPLICATIONINSIGHTS_CONNECTION_STRING for Azure Monitor.
    """
    global _provider
    _provider = TracerProvider()
    
    if use_console:
        # Local debugging - prints traces to console
        processor = SimpleSpanProcessor(ConsoleSpanExporter())
        _provider.add_span_processor(processor)
    else:
        # Azure Monitor - requires Application Insights connection string
        connection_string = settings.APPLICATIONINSIGHTS_CONNECTION_STRING
        print(f"connection: {connection_string}")
        if connection_string:
            from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
            exporter = AzureMonitorTraceExporter(connection_string=connection_string)
            processor = SimpleSpanProcessor(exporter)
            _provider.add_span_processor(processor)
            print("Tracing enabled: Azure Monitor")
        else:
            print("Warning: APPLICATIONINSIGHTS_CONNECTION_STRING not set. Falling back to console.")
            processor = SimpleSpanProcessor(ConsoleSpanExporter())
            _provider.add_span_processor(processor)
    
    trace.set_tracer_provider(_provider)
    
    # Register shutdown handler to flush traces on exit (including Ctrl+C)
    atexit.register(shutdown_tracing)
    
    # Try to instrument OpenAI if available
    try:
        from opentelemetry.instrumentation.openai import OpenAIInstrumentor
        OpenAIInstrumentor().instrument()
        print("OpenAI instrumentation enabled")
    except ImportError:
        print("Warning: opentelemetry-instrumentation-openai not installed")


def shutdown_tracing():
    """Flush and shutdown tracing to ensure all spans are exported."""
    global _provider
    if _provider:
        _provider.force_flush()
        _provider.shutdown()
        print("Tracing shutdown complete")