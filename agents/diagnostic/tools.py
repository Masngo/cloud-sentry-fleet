def query_cloud_logging(service_name: str) -> str:
    return f"LOGS: Error traces found for '{service_name}'."
def query_cloud_monitoring(service_name: str) -> str:
    return f"METRICS: RAM spiked to 99% for '{service_name}'."
