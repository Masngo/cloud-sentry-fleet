MEMORY_BANK = []
def record_remediation_event(service_name, rca, action):
    MEMORY_BANK.append({"service": service_name, "rca": rca, "action": action})
