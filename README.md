# Advanced Censys Client

[![PyPI](https://img.shields.io/pypi/v/censys?color=orange&logo=pypi&logoColor=orange)](https://pypi.org/project/advanced-censys/)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue?logo=python)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-organge.svg?logo=git&logoColor=organge)](http://makeapullrequest.com)
[![License](https://img.shields.io/github/license/censys/censys-python?logo=apache)](https://github.com/Inplex-sys/advanced-censys-client/blob/main/LICENSE)

### Additional Informations
 - This client is more fast than the official
 - You don't limit of api keys **(10 keys -> 100k ips)**

## Getting Started
The library can be installed using `pip3`.

```sh
pip3 install -i https://test.pypi.org/simple/ censys-client
```

To upgraded using `pip`.

```sh
pip3 install -i https://test.pypi.org/simple/ --upgrade censys-client
```

To configure your search credentials run `censys config` or set both `CENSYS_API_ID` and `CENSYS_API_SECRET` environment variables.
```sh
$ censys-client --config
Censys API ID (********************************98d1): CENSYS_API_ID
Censys API Secret (****************************aucc): CENSYS_API_SECRET
Your API ID and API Secret have been successfully saved to ./config.txt

Would you like to add another API ID and API Secret ? (y/n): 
```
