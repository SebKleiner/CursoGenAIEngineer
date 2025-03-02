import streamlit as st
import logging
from streamlit.runtime.scriptrunner import get_script_run_ctx

class StreamlitLogger:
    def __init__(self):
        self.logger = self._configure_logger()
    
    def _configure_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    def get_logger(self):
        ctx = get_script_run_ctx()
        if ctx is None:
            return self.logger
        return logging.getLogger(f"{__name__}.{ctx.session_id}")

def demo_logging():
    logger = StreamlitLogger().get_logger()
    
    st.header("Demo de Logging")
    
    if st.button("Generar Log Info"):
        logger.info("Botón de info presionado")
        st.success("Log info generado")
    
    if st.button("Generar Log Error"):
        logger.error("Este es un error de ejemplo")
        st.error("Log error generado")

def main():
    st.set_page_config(page_title="Demo Logging", page_icon="📝")
    demo_logging()

if __name__ == "__main__":
    main() 