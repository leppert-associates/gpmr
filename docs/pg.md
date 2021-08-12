# Postgres Setup Guide

## Installation

Instal Postgress from [postgresql.org](https://www.postgresql.org/download/). This installation should include a GUI called pgAdmin, but if not, download from [pgadmin.org](https://www.pgadmin.org/download).

### Environmental Variables

If command line tools are not recognized, the installation did not add to the path environmental variable.

- On your machine, go to settings
- Search for 'Environmental Variables' (or find the system properties, advanced tab)
- Click 'Environmental Variables...'
- Click on path, then edit
- Click New and add bin and lib paths (Note: lib must be after bin)
  - `C:\Program Files\PostgreSQL\13\bin`
  - `C:\Program Files\PostgreSQL\13\lib`

## The Shell

Run the SQL Shell app, or run command `psql` in the terminal.

If you are being prompted for a password prior to setting one type `psql -U postgres` in the command line.

To connect to a local db, accept default prompts

Type `help` to see commands, or `\?` for all commands

```shell
General
  \copyright             show PostgreSQL usage and distribution terms
  \crosstabview [COLUMNS] execute query and display results in crosstab
  \errverbose            show most recent error message at maximum verbosity
  \g [(OPTIONS)] [FILE]  execute query (and send results to file or |pipe);
                         \g with no arguments is equivalent to a semicolon
  \gdesc                 describe result of query, without executing it
  \gexec                 execute query, then execute each value in its result
  \gset [PREFIX]         execute query and store results in psql variables
  \gx [(OPTIONS)] [FILE] as \g, but forces expanded output mode
  \q                     quit psql
  \watch [SEC]           execute query every SEC seconds

Help
  \? [commands]          show help on backslash commands
  \? options             show help on psql command-line options
  \? variables           show help on special variables
  \h [NAME]              help on syntax of SQL commands, * for all commands

Query Buffer
  \e [FILE] [LINE]       edit the query buffer (or file) with external editor
  \ef [FUNCNAME [LINE]]  edit function definition with external editor
  \ev [VIEWNAME [LINE]]  edit view definition with external editor
  \p                     show the contents of the query buffer
  \r                     reset (clear) the query buffer
  \w FILE                write query buffer to file

Input/Output
  \copy ...              perform SQL COPY with data stream to the client host
-- More  --
```

To quit psql use the `\q` command or `Ctr + C`

## Getting Started

To create your first database, type `CREATE DATABASE mydb;`

## Connect to NAS?

Go to `C:\Program Files\PostgreSQL\13\data\pg_hba.conf` and

- Change: `host all all <your_ip/mask> ident`
- To: `host all all <your_ip/mask> md5`
  host all all 192.168.3.184/32 md5

Drobo IP: 192.168.3.184

Unable to connect to server:

could not connect to server: Connection timed out
Is the server running on host and accepting
TCP/IP connections on port?
