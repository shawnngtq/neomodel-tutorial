# Neomodel Tutorial

- [Neomodel Tutorial](#neomodel-tutorial)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Reference](#reference)

This tutorial is to test neo4j [neomodel](https://neomodel.readthedocs.io/en/latest/index.html).

[Neomodel GitHub](https://github.com/neo4j-contrib/neomodel)

## Requirements

- Neo4j
- Python
- Neomodel

You can refer to [environment.yml](environment.yml) or [install_packages.sh](install_packages.sh) for the specific libraries.

## Installation

```bash
# install from environment.yml
conda env create -f environment.yml
conda activate neomodel-tutorial

# create database models and constraints
neomodel_install_labels --db bolt://<database_name>:<database_password>@localhost:7687 models.py

# execute script
python app.py
```

## Reference

- <https://github.com/a759116/teamskill>
- <https://rudrapanda.medium.com/tutorial-neo4j-neomodel-python-bf26022921f0>
