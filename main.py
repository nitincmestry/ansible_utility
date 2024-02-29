from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate", response_class=HTMLResponse)
async def generate_playbook(request: Request, task: str = Form(...), variable: str = Form(...)):
    playbook = generate_playbook_from_task(task, variable)
    return templates.TemplateResponse("result.html", {"request": request, "playbook": playbook})


def generate_playbook_from_task(task: str, variable: str) -> str:
    playbook = f"""
    - name: My Playbook
      hosts: all
      tasks:
        - name: {task}
          # Add your dynamic variable handling here
          # dynamic_variable: {variable}
    """
    return playbook


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
