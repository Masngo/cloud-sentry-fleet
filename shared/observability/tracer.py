import logging
logging.basicConfig(level=logging.INFO)
def log_reasoning_step(agent, step):
    logging.info(f"[AGENT_TRACE] [{agent}] -> {step}")
