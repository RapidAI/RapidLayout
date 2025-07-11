# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import sys
from pathlib import Path
from typing import List, Union

from get_pypi_latest_version import GetPyPiLatestVersion
from setuptools import find_packages, setup


def read_txt(txt_path: Union[Path, str]) -> List[str]:
    with open(txt_path, "r", encoding="utf-8") as f:
        data = [v.rstrip("\n") for v in f]
    return data


def get_readme():
    root_dir = Path(__file__).resolve().parent
    readme_path = str(root_dir / "docs" / "doc_whl_rapid_layout.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()
    return readme


MODULE_NAME = "rapid_layout"
obtainer = GetPyPiLatestVersion()
latest_version = obtainer(MODULE_NAME)
VERSION_NUM = obtainer.version_add_one(latest_version, add_patch=True)

if len(sys.argv) > 2:
    match_str = " ".join(sys.argv[2:])
    matched_versions = obtainer.extract_version(match_str)
    if matched_versions:
        VERSION_NUM = matched_versions
sys.argv = sys.argv[:2]

setup(
    name=MODULE_NAME,
    version=VERSION_NUM,
    platforms="Any",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    description="Tools for document layout analysis based ONNXRuntime.",
    author="SWHL",
    author_email="liekkaskono@163.com",
    url="https://github.com/RapidAI/RapidLayout",
    license="Apache-2.0",
    include_package_data=True,
    install_requires=read_txt("requirements.txt"),
    packages=find_packages(),
    package_data={"": ["*.onnx", "*.yaml"]},
    keywords=["ppstructure,layout,rapidocr,rapid_layout"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": [f"{MODULE_NAME}={MODULE_NAME}.main:main"]},
)
