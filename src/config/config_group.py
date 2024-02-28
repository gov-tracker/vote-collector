
import json

class ConfigGroup:
    def __init__(self, config_group, group_path):
        self.str_to_print = f"{group_path}"
        self.__parse_group(config_group)

    def __str__(self):
        return self.str_to_print

    def __parse_group(self, config_group) -> None:
        for k, v in config_group.items():
            if isinstance(v, dict):
                setattr(self, k, ConfigGroup(v, f"{self.str_to_print}.{k}"))
            else:
                setattr(self, k, v)
