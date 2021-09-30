from setuptools import find_packages, setup

about = {}
with open("ip_pool/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(
    name="ip-pool",
    version=about["__version__"],
    description=about["__summary__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zachary Cutlip",
    author_email="uid000@gmail.com",
    url="https://github.com/zcutlip/ip-address-pool",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["ip-pool=ip_pool.cli:ip_pool_main"],
    },
    python_requires=">=3.7",
    install_requires=[],
    package_data={"ip_pool": ["config/*"]},
)
