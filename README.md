# Petstore Frontend

## Telemetry setup

This service uses the Comprehend OpenTelemetry SDK for tracing and metrics.

### Required environment variable

Set the following environment variable before running the service:

```powershell
$env:COMPREHEND_SDK_TOKEN="<your-comprehend-token>"
```

If the variable is not present, the telemetry module will raise an error so secrets are not silently omitted.

### Local run

```powershell
cd D:\Projects\petstore\petstore-frontend
python -m http.server 8000
```

For container deployments, pass the token through the container environment instead of committing it to source control.
