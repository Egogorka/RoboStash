# RoboStash
Robotniks' project for 2025 Hackathon from DD MIPT
https://github.com/Egogorka/RoboStash

## Packages used

- PyYAML — for parsing configs of databases
- PySide6 — for GUI in Qt
- user_agents — for parsing UA strings
- psycopg2 — PostgreSQL Python interface
- pandas — for data storage in-between app components 

## Installation

Currently the application should be run via Python interpreter with
necessary packages installed, and necessary databases set up as well.

For quick installation of Python packages use `[name_of_script]`.

For PostgreSQL follow the steps described in https://www.postgresql.org/download/

## How to use

Before launching `main.py`, config file `config.yaml` should be provided. 
If no config file is provided, then default one is used `example_config.yaml`, with "DatabasePlug" and CLI interface

While database part of config is mandatory and is set up like so:
```yaml
database:
  type: plug
  host: localhost
  port: 5432
  username: user
  password: pass
  database: logs
```
selection of view interface can be done via arguments
```shell
python main.py 
```

- Install packages with script `init.py`
- Setup supported database (PostgreSQL)
- Configure database connection parameters (host, password, etc.) in `config.yaml`
- Start the application from `main.py`