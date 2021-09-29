# YamlAttributes [![Tests Actions Status](https://github.com/gcascio/yaml-attributes/workflows/Tests/badge.svg)](https://github.com/gcascio/yaml-attributes/actions)

YamlAttributes is a utility class to load yaml files and assign the entries to associated class attributes.
This can be used to create a type safe and dynamic configuration class.

## Installation

YamlAttributes can be installed by running `pip install yamlattributes`

## Usage

The abstract `YamlAttributes` class provides the `init` method which loads a YAML file and assigns its values to the corresponding class attributes.
A class which inherits from `YamlAttributes` simply has to list the desired configuration as class attributes and two additional special attributes `yaml_file_path` and `yaml_section`. After calling the `init` method the all class attributes wil be assigned the values of the corresponding fields of the YAML file.

## API

### Attributes

| Attribute        | Default    | Description                                                      |
|------------------|------------|------------------------------------------------------------------|
| `yaml_file_path` | `'./'`     | Sets the path to the YAML file which should be loaded.           |
| `yaml_section`   | `'config'` | Sets YAML section which contains the desired config fields.      |

### init method

| Args           | values                    | Description                                                      |
|----------------|---------------------------|------------------------------------------------------------------|
| `mode`         | `'sync'`, `'soft_config'` | Selects the the mode of how the YAML values should update the config class. The `sync` mode keeps the YAML file and the config class in sync. Each attribute in the config class (except of the two special ones) have to be in the YAML file and vis versa. The `soft_config` mode allows the YAML file to have additional fields which the config class does not have. |



## Example

First create your desired config class and set the destination of the YAML file to be loaded through the special `yaml_file_path` attribute.

```python
# ./config.py

class MyConfig(YamlAttributes):
    yaml_file_path = './configs/my-config.yaml'
    batch_size: int
    num_classes: int
    optimizer: str
```

Make ure the YAML file exists and has all entries the config class `MyConfig` needs.

```yaml
# ./configs/my-config.yaml

config:
    batch_size: 32
    num_classes: 10
    optimizer: 'adam'
```

Finally you can initialize your config class and enjoy accessing config values with autocomplete.

```python
# ./main.py

from config import MyConfig

MyConfig.init()

# Access config values with autocomplete
MyConfig.batch_size
```