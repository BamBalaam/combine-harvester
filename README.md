# Combine Harvester

CLI tool to log [Harvest](https://www.getharvest.com/) timesheets with FZF

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/combine_harvester) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Requirements

* At least python 3.6 (sorry, I just like f-strings a bit too much)
* [fzf](https://github.com/junegunn/fzf)

## Installation

```
pip install combine-harvester
```

## Environment Variables

Two variables need to be in your environment to authenticate yourself to Harvest's API.

* HARVEST_ACCOUNT_ID
* HARVEST_ACCOUNT_TOKEN

Creating these tokens can be done through [Harvest's Developer Tools](https://id.getharvest.com/developers) page.

## Usage

This [wiki page](https://github.com/BamBalaam/combine-harvester/wiki/Usage) lists all commands and their usage.

```
> harvest

Usage: harvest [OPTIONS] COMMAND [ARGS]...

  Combine Harvester is a Harvest CLI Tool

Options:
  --help  Show this message and exit.

Commands:
  daily  Get notes from previous work day, to be used during daily standup.
  list   Get time entries from today, or optionally another day.
  log    Log time entry for today, using FZF.
```

## Disclaimer

This tool is not an official [Harvest](https://www.getharvest.com/) tool, nor am I affiliated to them.
