import inspect
from typing import Union, get_origin, get_args
import yaml
from abc import ABC


class YamlAttributes(ABC):
    yaml_file_path: str = './yaml-attribute-config.yaml'
    yaml_section: str = 'config'

    @classmethod
    def init(cls, mode='sync', yaml_file_path=None, yaml_section=None):
        cls.__load_config(
            yaml_file_path or cls.yaml_file_path,
            yaml_section or cls.yaml_section,
            mode,
        )

    @classmethod
    def to_dict(cls):
        return {
            k: v
            for k, v in vars(cls).items()
            if not (
                k.startswith('_')
                or inspect.ismethod(k)
            )
        }

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
        req_attributes = [
            k
            for k, v in attributes.items()
            if not cls.__is_optional(v)
        ]

        modes = {
            # The YAML config and the required class attributes have to match
            # exactly while the YAML config can only have entries which are
            # also in the config class
            'sync': lambda: (
                all(k in config for k in req_attributes)
                and all(k in attributes for k in config.keys())
            ),
            # The YAML config has to have at least all class attributes
            # while additional entries are omitted
            'soft_config': lambda: all(k in config for k in req_attributes)
        }

        assert (
            modes[mode]()
        ), 'YAML config and/or class attributes do not fulfill the '\
            'requirements of the "{}" mode'.format(mode)

        for key, attribute_type in attributes.items():
            value = config[key] if key in config.keys() else None
            config_type = type(value)
            attribute_is_union = get_origin(attribute_type) is Union

            if not (
                isinstance(attribute_type, type)
                or attribute_is_union
            ):
                attribute_type = type(attributes[key])

            assert (
                config_type == attribute_type
                or (
                    attribute_is_union
                    and config_type in get_args(attributes[key])
                )
            ), 'Type missmatch between YAML file and config '\
                'class was found for the "{}" attribute.'.format(key)

            setattr(cls, key, value)

    def __is_optional(field):
        return get_origin(field) is Union and type(None) in get_args(field)
