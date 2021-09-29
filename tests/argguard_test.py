import pytest

from yamlattributes import YamlAttributes


def test_config_loads_successfully_in_sync_mode():
    """
    Description
    """
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
    """
    Description
    """
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
    """
    Description
    """
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
    """
    Description
    """
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
    """
    Description
    """
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
    """
    Description
    """
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
