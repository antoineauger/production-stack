import logging
import sys
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def generate_static_backends(models: dict[str, Any]) -> str:
    static_backends = ""
    for _, details in models.items():
        if "static_backends" in details:
            for endpoint in details["static_backends"]:
                static_backends += f"{endpoint},"
    return static_backends.strip(",")


def generate_static_models(models: dict[str, Any]) -> str:
    static_models = ""
    for name, details in models.items():
        if "static_backends" in details:
            static_models += f"{name}," * len(details["static_backends"])
    return static_models.strip(",")


def generate_static_aliases(aliases: dict[str, Any]) -> str:
    static_aliases = ""
    for alias, model in aliases.items():
        static_aliases += f"{alias}:{model},"
    return static_aliases.strip(",")


def generate_static_model_types(models: dict[str, Any]) -> str:
    static_model_types = ""
    for _, details in models.items():
        if "static_model_type" in details and "static_backends" in details:
            static_model_types += f"{details['static_model_type']}," * len(
                details["static_backends"]
            )
    return static_model_types.strip(",")


def read_and_process_yaml_config_file(config_path: str) -> dict[str, Any]:
    with open(config_path, encoding="utf-8") as f:
        try:
            yaml_config = yaml.safe_load(f)
            models = yaml_config.pop("static_models", None)
            aliases = yaml_config.pop("static_aliases", None)
            if models:
                yaml_config["static_backends"] = generate_static_backends(models)
                yaml_config["static_models"] = generate_static_models(models)
                yaml_config["static_model_types"] = generate_static_model_types(models)
            if aliases:
                yaml_config["static_aliases"] = generate_static_aliases(aliases)
            return yaml_config
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML config file: {e}")
            sys.exit(1)
