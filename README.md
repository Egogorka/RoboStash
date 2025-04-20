# RoboStash
Robotniks' project for 2025 Hackathon from DD MIPT
https://github.com/Egogorka/RoboStash

Contributors:

- https://github.com/anastasiiade
- https://github.com/Andreiv573
- https://github.com/AserDees
- https://github.com/KochetovSergey
- https://github.com/OsokinIlya
- https://github.com/Egogorka/
=======

## Packages used

- PyYAML — for parsing configs of databases
- PySide6 — for GUI in Qt
- user_agents — for parsing UA strings
- psycopg2 — PostgreSQL Python interface
- pandas — for data storage in-between app components

## Installation and configuration

Currently the application should be run via Python interpreter with
necessary packages installed, and necessary databases set up as well.

For quick installation of Python packages run `pip install -r requirements.txt`.

For PostgreSQL follow the steps described in https://www.postgresql.org/download/

Then enter in `config.yaml` information about connection to database



## How to use

Before launching `main.py`, config file `config.yaml` should be provided. 
If no config file is provided, then default one is used `example_config.yaml`, with "DatabasePlug" and CLI interface

While database part of config is mandatory and is set up like so:
```yaml
databases:
  plug:
    type: plug
  postgreSQL:
    type: postgreSQL
    host: localhost
    port: 5432
    username: user
    password: pass
    database: logs
```

Then launch the script:
```shell
python main.py
```
=======
- PySide6 — for GUI
- user_agents - for parsing UA strings
- psycopg2 - PostgreSQL Python interface

## How to use

Currently the application should be run via Python interpreter with
necessary packages installed, and necessary databases set up as well:
```shell

```

- Install packages with script `init.py`
- Setup supported database (PostgreSQL)
- Configure database connection parameters (host, password, etc.) in `config.yaml`
- Start the application from `main.py`
