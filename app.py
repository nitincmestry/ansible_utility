import typer
import yaml

app = typer.Typer()

def load_tasks_yaml():
    with open("tasks.yaml", "r") as file:
        tasks = yaml.safe_load(file)
    return tasks

def get_task_params(task):
    params = {}
    for sub_task in task['tasks']:
        module = sub_task.get('module', 'custom_script')  # Use 'custom_script' as the default module if not provided
        typer.echo(f"\nTask: {task['name']}")
        params[sub_task['name']] = {}
        for param, param_info in sub_task['task_params'].items():
            default_value = param_info.get('default')
            description = param_info.get('description', '')
            prompt = f"Enter value for {param}"
            if default_value is not None:
                prompt += f" (default: {default_value})"
            if description:
                prompt += f" ({description})"
            value = typer.prompt(prompt, default=default_value)
            params[sub_task['name']][param] = value
        params[sub_task['name']]['module'] = module
    return params

def generate_site_yaml(site_yaml):
    playbook = []
    for task_name, task_params in site_yaml.items():
        task = {"name": task_name, "hosts": "localhost", "tasks": []}
        for sub_task_name, sub_task_params in task_params.items():
            sub_task_details = {"action": {"module": sub_task_params.pop("module"), "args": sub_task_params}}
            task["tasks"].append(sub_task_details)
        playbook.append(task)

    with open("site.yaml", "w") as file:
        yaml.dump(playbook, file)

    typer.echo("\nSite.yaml generated successfully.")

@app.command()
def run():
    tasks = load_tasks_yaml()
    site_yaml = {}

    typer.echo("Available tasks:")
    for i, task in enumerate(tasks):
        typer.echo(f"{i+1}. {task['name']}")

    while True:
        task_number = typer.prompt("\nSelect task number to add (or type 'done' to finish): ")
        if task_number.lower() == 'done':
            break
        task_number = int(task_number) - 1
        if task_number < 0 or task_number >= len(tasks):
            typer.echo("Invalid task number. Please select a valid number.")
            continue

        selected_task = tasks[task_number]
        task_params = get_task_params(selected_task)
        site_yaml[selected_task['name']] = task_params

    generate_site_yaml(site_yaml)

if __name__ == "__main__":
    app()
