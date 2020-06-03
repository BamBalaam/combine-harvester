from itertools import islice, count


def iter_range(start, stop, step=1.0):
    length = int(abs(stop - start) / step)
    return islice(count(start, step), length)


def parse_project_assignments(rest_response):
    parsed_data = {}
    projects = []
    for item in rest_response["project_assignments"]:
        project_instance = {
            "id": item["project"]["id"],
            "name": item["project"]["name"],
            "tasks": item["task_assignments"],
        }
        projects.append(project_instance)

    for item in projects:
        project_name = item["name"]
        parsed_data[project_name] = {}
        parsed_data[project_name]["id"] = item["id"]
        tasks = {}
        for task in item["tasks"]:
            tasks[task["task"]["name"]] = task["task"]["id"]
        parsed_data[project_name]["tasks"] = tasks

    return parsed_data
