from src.config.config_manager import get_config, combine_configs, config
import pytest
import os, tempfile


class TestFileContent:
    def __init__(self, content):
        self.file = tempfile.NamedTemporaryFile(mode="w", delete=False)

        with self.file as f:
            f.write(content)

    @property
    def filename(self):
        return self.file.name

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        os.unlink(self.filename)


@pytest.fixture(autouse=True, scope="session")
def temp_yaml_1():
    file_content = (
        """version: 42\nfoo_data:\n  location: some/directory/data.csv\n  type: csv"""
    )
    yield TestFileContent(file_content)


@pytest.fixture(autouse=True, scope="session")
def temp_yaml_2():
    file_content = """version: 1\ndriver_paths:\n  CHROME_DRIVER_PATH: some/directory/chromedriver.exe"""
    yield TestFileContent(file_content)


def test_get_config(temp_yaml_1):
    actual = get_config(temp_yaml_1.filename)

    expected = {
        "version": 42,
        "foo_data": {
            "location": "some/directory/data.csv",
            "type": "csv",
        },
    }

    assert actual == expected


def test_combine_configs(temp_yaml_1, temp_yaml_2):
    config_entries = (
        ["foo", temp_yaml_1.filename],
        ["bar", temp_yaml_2.filename],
    )

    actual = combine_configs(*config_entries)

    expected = {
        "foo": {
            "version": 42,
            "foo_data": {
                "location": "some/directory/data.csv",
                "type": "csv",
            },
        },
        "bar": {
            "version": 1,
            "driver_paths": {
                "CHROME_DRIVER_PATH": "some/directory/chromedriver.exe",
            },
        },
    }

    assert actual == expected
