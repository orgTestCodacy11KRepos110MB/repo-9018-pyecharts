import os
import urllib.error
from unittest.mock import patch

from nose.tools import assert_equal, raises

from pyecharts.datasets import (
    EXTRA,
    FuzzyDict,
    register_url,
    register_files,
    register_coords,
)


@patch("pyecharts.datasets.urllib.request.urlopen")
def test_register_url(fake):
    current_path = os.path.dirname(__file__)
    fake_registry = os.path.join(current_path, "fixtures", "registry.json")
    file_name = ["shape-with-internal-borders/an1_hui1_an1_qing4", "js"]
    with open(fake_registry, encoding="utf8") as f:
        fake.return_value = f
        register_url("http://register.url/is/used")
        assert_equal(
            EXTRA,
            {
                "http://register.url/is/used/js/": {
                    "安庆": file_name,
                    "English Name": file_name,
                }
            },
        )


def test_register_url_error():
    try:
        register_url("http://127.0.0.1")
    except urllib.error.HTTPError as err:
        assert_equal(type(err), urllib.error.HTTPError)


def test_fuzzy_search_dict():
    fd = FuzzyDict()
    fd.update({"我是北京市": [1, 2]})
    assert_equal(fd["我是北京"], [1, 2])


@raises(KeyError)
def test_fuzzy_search_key_error():
    fd = FuzzyDict()
    fd.cutoff = 0.9
    _ = fd["我是北京"]


def test_register_files():
    register_files(asset_files={"x": 1})


def test_register_coords():
    register_coords(coords={"深圳": [113, 23]})
