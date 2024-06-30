import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
pytest_plugins = [
    "tests.fixtures.mem_api",
    "tests.fixtures.data",
    "tests",
]
