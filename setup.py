import re

import setuptools

with open("src/defi_services/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="defi-state-querier",
    version=version,
    author="Viet-Bang Pham",
    author_email="phamvietbang2965@gmail.com",
    description="Calculate apy, apr, and wallet information,... in decentralized applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Centic-io/defi-state-querier",
    project_urls={"Bug Tracker": "https://github.com/Centic-io/defi-state-querier", },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # web3.py doesn't work on 3.5.2 and less (https://github.com/ethereum/web3.py/issues/1012)
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.6',
    install_requires=[
        "web3==5.31.1",
        "QueryStateLib==1.1.4",
        "pycoingecko==2.2.0",
        "python-dotenv==0.21.0",
        "pymongo==4.3.3"
    ],
)
