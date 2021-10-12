from typing import Optional
import pytest

from yamlattributes import YamlAttributes


def test_config_loads_successfully_in_sync_mode():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act
    TestConfig.init()

    # Assert
    assert (
        TestConfig.test_attribute_a == 'config_test_value_a'
        and TestConfig.test_attribute_b == 'config_test_value_b'
        and TestConfig.test_attribute_c == 42
    ), 'Config values are not correctly assigned to config class'


def test_config_fails_with_incomplete_yaml_in_sync_mode():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/incomplete_test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act

    # Assert
    with pytest.raises(
        AssertionError,
        match=r".*\"sync\" mode.*",
    ):
        TestConfig.init()


def test_config_fails_with_overloaded_yaml_in_sync_mode():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/overloaded_test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act

    # Assert
    with pytest.raises(
        AssertionError,
        match=r".*\"sync\" mode.*",
    ):
        TestConfig.init()


def test_config_loads_successfully_in_soft_config_mode():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act
    TestConfig.init(mode='soft_config')

    # Assert
    assert (
        TestConfig.test_attribute_a == 'config_test_value_a'
        and TestConfig.test_attribute_b == 'config_test_value_b'
        and TestConfig.test_attribute_c == 42
    ), 'Config values are not correctly assigned to config class'


def test_config_loads_successfully_overloaded_config_in_soft_config_mode():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/overloaded_test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act
    TestConfig.init(mode='soft_config')

    # Assert
    assert (
        TestConfig.test_attribute_a == 'config_test_value_a'
        and TestConfig.test_attribute_b == 'config_test_value_b'
        and TestConfig.test_attribute_c == 42
        and not hasattr(TestConfig, 'test_attribute_d')
    ), 'Config values are not correctly assigned to config class'


def test_config_fails_with_incomplete_yaml_in_soft_config_mode():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/incomplete_test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act

    # Assert
    with pytest.raises(
        AssertionError,
        match=r".*\"soft_config\" mode.*",
    ):
        TestConfig.init(mode='soft_config')


def test_config_fails_with_type_mismatch():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/test_config.yaml'
        # create type mismatch between config class and YAML file
        # by changing str to int
        test_attribute_a: int
        test_attribute_b = 'test_value_b'
        test_attribute_c: int

    # Act

    # Assert
    with pytest.raises(
        AssertionError,
        match=r".*missmatch.*\"test_attribute_a\" attribute.*",
    ):
        TestConfig.init()


def test_config_loads_successfully_with_union_type():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: int
        optional_attribute: Optional[int]

    # Act
    TestConfig.init()

    # Assert
    assert (
        TestConfig.test_attribute_a == 'config_test_value_a'
        and TestConfig.test_attribute_b == 'config_test_value_b'
        and TestConfig.test_attribute_c == 42
        and hasattr(TestConfig, 'optional_attribute')
        and not TestConfig.optional_attribute
    ), 'Config values are not correctly assigned to config class'


def test_config_successfully_assighns_optional_values():
    YamlAttributes.__abstractmethods__ = set()

    # Arrange
    class TestConfig(YamlAttributes):
        yaml_file_path = './tests/test_config.yaml'
        test_attribute_a: str
        test_attribute_b = 'test_value_b'
        test_attribute_c: Optional[int]

    # Act
    TestConfig.init()

    # Assert
    assert (
        TestConfig.test_attribute_a == 'config_test_value_a'
        and TestConfig.test_attribute_b == 'config_test_value_b'
        and TestConfig.test_attribute_c == 42
    ), 'Config values are not correctly assigned to config class'
