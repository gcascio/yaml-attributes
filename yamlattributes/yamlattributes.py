import inspect
import yaml
from abc import ABC


class YamlAttributes(ABC):
    yaml_file_path: str = './yaml-attribute-config.yaml'
    yaml_section: str = 'config'

    @classmethod
    def init(cls, mode='sync'):
        cls.__load_config(cls.yaml_file_path, cls.yaml_section, mode)

    @classmethod
    def __load_config(cls, yam_file_path: str, yaml_section, mode):
        attributes = cls.__get_attributes()

        with open(yam_file_path, "r") as stream:
            config = yaml.safe_load(stream)

            if yaml_section:
                config = config[yaml_section]

            cls.__set_attributes(config, attributes, mode)

    @classmethod
    def __get_attributes(cls):
        self_members = dict(inspect.getmembers(YamlAttributes))
        members = dict(inspect.getmembers(cls))

        members = {
            **members,
            **members['__annotations__'],
        }

        filtered_members = {
            key: value
            for (key, value) in members.items()
            if not (
                key.startswith('_')
                or inspect.ismethod(value)
                or key in self_members.keys()
            )
        }

        return filtered_members

    @classmethod
    def __set_attributes(cls, config: dict, attributes: dict, mode):
        req_attributes = attributes.keys()

        modes = {
            # The YAML config and the required class attributes have to match
            # exactly
            'sync': lambda: set(config.keys()) == set(req_attributes),
            # The YAML config has to have at least all class attributes
            # while additional entries are omitted
            'soft_config': lambda: all(k in config for k in req_attributes)
        }

        assert (
            modes[mode]()
        ), 'YAML config and/or class attributes do not fulfill the '\
            'requirements of the "{}" mode'.format(mode)

        for key, value in config.items():
            if key not in req_attributes:
                return

            config_type = type(value)
            attribute_type = attributes[key]

            if not isinstance(attribute_type, type):
                attribute_type = type(attributes[key])

            assert (
                config_type == attribute_type
            ), 'Type missmatch between YAML file and config '\
                'class was found for the "{}" attribute'.format(key)

            setattr(cls, key, value)
