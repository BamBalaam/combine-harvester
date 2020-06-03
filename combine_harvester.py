from datetime import date
from itertools import islice, count
import json
import os

import jq
from pyfzf.pyfzf import FzfPrompt
import requests


def iter_range(start, stop, step=1.0):
    length = int(abs(stop - start) / step)
    return islice(count(start, step), length)


def main():
    fzf = FzfPrompt()
    harvest_id = os.getenv("HARVEST_ACCOUNT_ID")
    harvest_token = os.getenv("HARVEST_ACCOUNT_TOKEN")
    headers = {
        "Harvest-Account-ID": harvest_id,
        "Authorization": f"Bearer {harvest_token}",
    }
    api_url = "https://api.harvestapp.com/api/v2"

    response = requests.get(
        api_url+"/users/me/project_assignments/",
        headers=headers
    )

    projects_raw = jq.compile(
        """.project_assignments | {
            projects: map_values(
                {
                    id: .project.id,
                    name: .project.name,
                    tasks: .task_assignments
                }
            )
        }
        """
    ).input(response.json()).text()

    projects = json.loads(projects_raw)['projects']

    final_dict = {}

    for item in projects:
        project_name = item['name']
        final_dict[project_name] = {}
        final_dict[project_name]['id'] = item['id']
        tasks = {}
        for task in item['tasks']:
            tasks[task['task']['name']] = task['task']['id']
        final_dict[project_name]['tasks'] = tasks

    projects_prompt = final_dict.keys()

    project_choice = fzf.prompt(
        projects_prompt, "--prompt 'Choose Harvest Project:  ' --reverse"
    )[0]

    tasks_prompt = final_dict[project_choice]['tasks'].keys()

    task_choice = fzf.prompt(
        tasks_prompt, "--prompt 'Choose Project Task:  ' --reverse"
    )[0]

    project_id = final_dict[project_choice]['id']
    task_id = final_dict[project_choice]['tasks'][task_choice]

    time_choice = fzf.prompt(
        list(iter_range(0.5, 8.5, 0.5)),
        "--prompt 'Amount of Hours to log?:  ' --reverse"
    )[0]

    notes = input("(Optional) Add task notes? Press enter to leave blank: ")

    log_url = (
        f"{api_url}/time_entries"
        f"?project_id={project_id}&task_id={task_id}"
        f"&spent_date={date.today().isoformat()}&hours={time_choice}"
    )

    if notes != '':
        log_url += f"&notes={notes}"

    response = requests.post(log_url, headers=headers)


if __name__ == "__main__":
    main()
