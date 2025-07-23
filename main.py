from ui.app_ui import iniciar_ui
from database.db_config import inicializar_banco

if __name__ == "__main__":
    inicializar_banco()
    iniciar_ui()