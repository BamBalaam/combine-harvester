# Combine Harvester

CLI tool to log Harvest timesheets with FZF

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation

```
pip install combine-harvester
```

## Requirements

* Python 3.6 (f-strings!)
* [fzf](https://github.com/junegunn/fzf)

## Environment Variables

* HARVEST_ACCOUNT_ID
* HARVEST_ACCOUNT_TOKEN

## Usage

```
> harvest

Usage: harvest [OPTIONS] COMMAND [ARGS]...

  Combine Harvester is a Harvest CLI Tool

Options:
  --help  Show this message and exit.

Commands:
  daily  Get time entries from previous day, to be used during daily...
  list   Get time entries from today, or optionally another day.
  log    Log time entry for today, using FZF.
```
