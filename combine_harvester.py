from datetime import date, datetime, timedelta
import os

import click
import iso8601
from pyfzf.pyfzf import FzfPrompt
import requests

from utils import iter_range, parse_project_assignments


@click.group()
@click.pass_context
def main(ctx):
    """Combine Harvester is a Harvest CLI Tool"""
    fzf = FzfPrompt()
    harvest_id = os.getenv("HARVEST_ACCOUNT_ID")
    harvest_token = os.getenv("HARVEST_ACCOUNT_TOKEN")
    headers = {
        "Harvest-Account-ID": harvest_id,
        "Authorization": f"Bearer {harvest_token}",
    }
    api_url = "https://api.harvestapp.com/api/v2"
    ctx.obj = {"fzf": fzf, "headers": headers, "api_url": api_url}


@main.command()
@click.pass_context
def daily(ctx):
    """Get notes from previous work day, to be used during daily standup.

    Will return time entries from the day before, except on Monday, which will
    return entries from last Friday.
    """
    api_url, headers = ctx.obj["api_url"], ctx.obj["headers"]
    yesterday = datetime.strftime(datetime.now() - timedelta(1), "%Y-%m-%d")
    friday = datetime.strftime(datetime.now() - timedelta(3), "%Y-%m-%d")
    if date.today().weekday() == 0:
        daily_url = api_url + f"/time_entries?from={friday}&to={friday}"
    else:
        daily_url = api_url + f"/time_entries?from={yesterday}&to={yesterday}"

    response = requests.get(daily_url, headers=headers)
    for entry in response.json()["time_entries"][::-1]:
        if entry["notes"] != "":
            print(f"- {entry['notes']}")


@main.command()
@click.option('--day', type=str, help="Day in ISO format: YYYY-MM-DD.")
@click.pass_context
def list(ctx, day):
    """Get time entries from today, or optionally another day."""
    api_url, headers = ctx.obj["api_url"], ctx.obj["headers"]
    if day is None:
        today = date.today().isoformat()
        list_url = api_url + f"/time_entries?from={today}&to={today}"
    else:
        try:
            iso8601.parse_date(day)
        except iso8601.iso8601.ParseError:
            print("Invalid ISO format string")
            ctx.exit(1)
        list_url = api_url + f"/time_entries?from={day}&to={day}"

    response = requests.get(list_url, headers=headers)
    for entry in response.json()["time_entries"][::-1]:
        project = entry['project']['name']
        time = entry['hours']
        task = entry['task']['name']
        note = ""
        print(f"({time} hours) - {project}")
        if entry["notes"] != "":
            note = entry['notes']
        print(f"{task} {'- ' + note if note != '' else ''}\n")


@main.command()
@click.pass_context
def log(ctx):
    """Log time entry for today, using FZF.

    Uses FZF to list projects, tasks, hours and others to add a time entry.
    """
    api_url, headers, fzf = (
        ctx.obj["api_url"],
        ctx.obj["headers"],
        ctx.obj["fzf"],
    )
    response = requests.get(
        api_url + "/users/me/project_assignments/", headers=headers
    )

    harvest_data = parse_project_assignments(response.json())

    projects_prompt = harvest_data.keys()

    project_choice = fzf.prompt(
        projects_prompt, "--prompt 'Choose Harvest Project:  ' --reverse"
    )[0]

    tasks_prompt = harvest_data[project_choice]["tasks"].keys()

    task_choice = fzf.prompt(
        tasks_prompt, "--prompt 'Choose Project Task:  ' --reverse"
    )[0]

    project_id = harvest_data[project_choice]["id"]
    task_id = harvest_data[project_choice]["tasks"][task_choice]

    time_choice = fzf.prompt(
        iter_range(0.5, 8.5, 0.5),
        "--prompt 'Amount of Hours to log?:  ' --reverse",
    )[0]

    notes = input("(Optional) Add task notes? Press enter to leave blank: ")

    log_url = (
        f"{api_url}/time_entries"
        f"?project_id={project_id}&task_id={task_id}"
        f"&spent_date={date.today().isoformat()}&hours={time_choice}"
    )

    if notes != "":
        log_url += f"&notes={notes}"

    response = requests.post(log_url, headers=headers)


if __name__ == "__main__":
    main(obj={})
