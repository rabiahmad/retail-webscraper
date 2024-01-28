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
def temp_yaml():
    file_content = (
        """version: 42\nfoo_data:\n  location: some/directory/data.csv\n  type: csv"""
    )
    yield TestFileContent(file_content)


def test_get_config(temp_yaml):
    actual = get_config(temp_yaml.filename)

    expected = {
        "version": 42,
        "foo_data": {
            "location": "some/directory/data.csv",
            "type": "csv",
        },
    }

    assert actual == expected
