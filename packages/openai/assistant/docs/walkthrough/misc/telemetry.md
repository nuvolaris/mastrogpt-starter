# Telemetry

Monitoring and understanding the behavior of your microservices is crucial for ensuring their reliability and performance. Dapr, the Distributed Application Runtime, provides built-in support for telemetry, making it easier to gather and analyze data from your microservices. Dapr supports various telemetry exporters, including Zipkin, Jaeger, and Application Insights.

In this walkthrough, we'll explore how to enable and configure telemetry in your microservice using Dapr. We'll focus on the Zipkin exporter as an example, but you can enable other exporters as needed.

In your microservice's YAML configuration, add the telemetry section to enable telemetry and specify the desired exporters (e.g., Zipkin, Jaeger, Application Insights).

```yml
telemetry:
  enable: true
  exporters:
    zipkin: true
```

This will generate a Zipkin container and the required configuration:

```cs
builder.Services.AddOpenTelemetryTracing(builder => builder.SetResourceBuilder(ResourceBuilder.CreateDefault().AddService("Store")).AddAspNetCoreInstrumentation().AddZipkinExporter(x => x.Endpoint = new System.Uri("http://zipkin:9411/api/v2/spans")));
```

Telemetry data includes traces and spans that provide insights into request flow, latency, and individual operations in your microservice. The telemetry data also includes the service name and exporter configuration. Access and analyze telemetry data using the respective tool for your chosen telemetry exporter (e.g., Zipkin, Jaeger, or Application Insights). This allows you to monitor and troubleshoot your microservice's performance and behavior effectively.

Next step: [Advanced Topics in DAL](../dal/advanced-topics-in-dal.md)
