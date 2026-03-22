import logging
import logging.config
import logging.handlers

from pathlib import Path
import yaml

from app.core import settings


class LoggerUtils:
    @staticmethod
    def vk_logs_path() -> str:
        return "logs/vk_logs"

    @staticmethod
    def tg_logs_path() -> str:
        return "logs/tg_logs"

    @staticmethod
    def __disable_logger__(baseFilename: str):
        root_logger = logging.getLogger()

        handler = next(
            (
                h
                for h in root_logger.handlers
                if isinstance(h, logging.handlers.TimedRotatingFileHandler)
                and baseFilename in h.baseFilename
            ),
            None,
        )
        if handler:
            root_logger.removeHandler(handler)

    @staticmethod
    def disable_vk_logger():
        LoggerUtils.__disable_logger__("vk_logs")

    @staticmethod
    def disable_tg_logger():
        LoggerUtils.__disable_logger__("tg_logs")

    @staticmethod
    def setup_logger():
        """
        Настройка логирования на основе log_conf.yaml и параметров из .env.
        """
        # Получаем параметры из настроек
        environment = settings.common_app.ENVIRONMENT
        # Создаём директорию для логов, если её нет
        if environment == "development":
            Path(f"{LoggerUtils.tg_logs_path()}/dev").mkdir(parents=True, exist_ok=True)
            Path(f"{LoggerUtils.vk_logs_path()}/dev").mkdir(parents=True, exist_ok=True)
        if environment == "production":
            Path(f"{LoggerUtils.tg_logs_path()}/prod").mkdir(
                parents=True, exist_ok=True
            )
            Path(f"{LoggerUtils.vk_logs_path()}/prod").mkdir(
                parents=True, exist_ok=True
            )

        # Загружаем конфигурацию из YAML
        config_path = Path(
            f"log_conf.{environment.lower()}.yaml"
        )  # или укажите полный путь
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

            # Применяем конфигурацию
            logging.config.dictConfig(config)

            # 4. Отдельная настройка уровней для сторонних библиотек
            logging.getLogger("apscheduler").setLevel(logging.WARNING)
            logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

            if not settings.vk_app.VK_RUN:
                # запуск vk бота отключен. отключаем логгер
                LoggerUtils.disable_vk_logger()
            if not settings.tg_app.TG_RUN:
                # запуск tg бота отключен. отключаем логгер
                LoggerUtils.disable_tg_logger()
