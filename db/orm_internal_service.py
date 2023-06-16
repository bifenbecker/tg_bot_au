import os
import logging
import settings
from db.orm import Base
from glob import glob
from importlib import import_module

logger = logging.getLogger(__name__)


class OrmInternalService:
    # This class imports models
    # thus it adds them to Base.metadata

    TARGET_FOLDER = "models"
    METADATA_NOT_CHECKED_MESSAGE = "is not checked for metadata (migrations)"
    MODELS_NOT_CHECKED_MESSAGE = "is not checked for models (admin panel)"
    NOT_CHECKED_MESSAGE = "is not checked for items"

    @classmethod
    def _get_module_items(cls, module_name) -> list[dict]:
        """
        import classes / methods / variables module in specific app
        and get __all__ variable to get these items in output format:
        [{"name": item_name, "value": exact_class_or_method}]
        """
        module_name = os.path.relpath(module_name, settings.BASE_DIR)
        module_name = module_name.replace("/", ".")
        package_name = module_name.split(".")[0]
        module_name = module_name.replace(package_name, "")
        target_module = import_module(module_name, package=package_name)
        module_items = [{"name": item_name, "value": getattr(target_module, item_name)}
                        for item_name in target_module.__all__]
        return module_items

    @classmethod
    def _get_modules_with_items(cls) -> list[str]:
        """
        Scan all "target_subfolders" folders in TARGET_FOLDER recursively
        """

        module_paths = [module_path for module_path in
                        glob(f"{settings.BASE_DIR}/db/{cls.TARGET_FOLDER}/", recursive=True)]
        return module_paths

    @classmethod
    def get_items(cls, not_checked_message=None) -> list[dict]:
        """
        Main method of the class that returns the list of dicts of imported items
        in format [{"name": item_name, "value": exact_class_or_method}]
        """
        items = []
        modules_with_items = cls._get_modules_with_items()
        not_checked_message = not_checked_message or cls.NOT_CHECKED_MESSAGE

        for module_path in modules_with_items:
            try:
                items += cls._get_module_items(module_path)
            except Exception as e:
                logger.exception(e)
                logger.info(f"App {module_path} {not_checked_message}")
        return items

    @classmethod
    def get_models_metadata(cls):
        # get all metadata in the project
        # to make auto migrations work
        metadata = cls.get_items(
            not_checked_message=cls.METADATA_NOT_CHECKED_MESSAGE
        )

        metadata = [metadata_item['value'].metadata for metadata_item in metadata]
        return Base.metadata

    @classmethod
    def get_models(cls):
        # Get all models in the project

        models = cls.get_items(
            not_checked_message=cls.MODELS_NOT_CHECKED_MESSAGE
        )

        return [model['value'] for model in models]
