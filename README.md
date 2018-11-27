# MySQL Batch

> Run a number of SQL scripts on a MySQL server.

## Usage
Prepare a directory with SQL scripts, named according to the scheme `<no>_<name>.sql`.
Every script is considered a step in an execution sequence.
The leading number controls the order of execution and helps filtering the steps.
The connection to the target server is configured in a configuration file.
See section _Example Configuration_, for an example of `config.ini`.

~~~sh
mysql_batch.py -c config.ini ./sql-scripts my-server
~~~

## Docker Usage
This tool is published as a Docker container as `mastersign/mysql-batch`.
To run `mysql_batch` in a Docker container use the following command.
For the `db-connections.ini` see section _Example Configuration_.

~~~sh
docker run --rm -ti \
    -v $(pwd)/db-connections.ini:/app/config.ini \
    -v $(pwd)/sql-scripts:/app/scripts \
    mastersign/mysql-batch \
    my-server
~~~

## Example Configuration

The configuration contains the connection information for the server
in a section of the INI file.
The server section must be called `database.<name>`.
The name used here is not the actual hostname of the server,
but rather an alias inside the configuration.
There can be more than two server sections in the configuration.

The fields in a server section are:

* `host`: The IP address or hostname, optionally with a port number like `servername:3306`
* `schema`: (_optional_) The default schema on this server
* `user`: (_optional_) The username the login at the MySQL server (default is `root`)
* `password`: (_optional_) The password for the login at the MySQL server (default is empty)

Example for `config.ini`:

~~~ini
[database.my-server]
host = 10.123.45.1:3306
schema = target_db
user = root
password =
~~~

## Help Text

~~~
usage: mysql_batch.py [-h] [-v] [-d] [-n [NO [NO ...]]] [-xn [NO [NO ...]]]
                      [-f NO] [-t NO] [-g PATTERN] [-xg PATTERN] [-r REGEX]
                      [-xr REGEX] [-c CONFIG_FILES] [-o OPTIONS [OPTIONS ...]]
                      source_dir target

Run multiple SQL scripts on a MySQL server.

positional arguments:
  source_dir            A path to the directory with SQL scripts named
                        <no>_<name>.sql.
  target                The name of the target database in the configuration.
                        This is the database to execute the scripts on.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         print the program version and exit
  -d, --dry             do not run the scripts, just print the selected script
                        names
  -n [NO [NO ...]], --include-no [NO [NO ...]]
                        include the listed steps by no
  -xn [NO [NO ...]], --exclude-no [NO [NO ...]]
                        exclude the listed steps by no
  -f NO, --from NO      excludes steps with a number lower
  -t NO, --to NO        exclude steps with a number higher
  -g PATTERN, --include PATTERN
                        include steps, which name matches the given glob
                        pattern
  -xg PATTERN, --exclude PATTERN
                        exclude steps, which name matches the given glob
                        pattern
  -r REGEX, --include-re REGEX
                        include steps, which name matches the given regex
  -xr REGEX, --exclude-re REGEX
                        include steps, which name matches the given regex
  -c CONFIG_FILES, --config-file CONFIG_FILES
                        A path to a configuration file in UTF-8 encoded INI
                        format. This argument can be used multiple times.
  -o OPTIONS [OPTIONS ...], --options OPTIONS [OPTIONS ...]
                        One or more configuration options, given in the format
                        <section>.<option>=<value>.
~~~

## License

This project is published under the BSD-3-Clause license.

Copyright &copy; 2018 Tobias Kiertscher <dev@mastersign.de>.
