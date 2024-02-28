
from typing import AnyStr
import tomli


from config.config_group import ConfigGroup

class Config:
    def __init__(self, config: AnyStr) -> None:

        with open(config, 'rb') as f:
            cfg = tomli.load(f)
        self.__parse_config(cfg)

    def __parse_config(self, cfg):
        for k, v in cfg.items():
            if isinstance(v, dict):
                setattr(self, k, ConfigGroup(v, f"config.{k}"))
            else:
                setattr(self, k, v)

