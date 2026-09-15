# Todo API

This is a small REST API for managing a to-do list, built with Python and Flask for the DevOps & Cloud Internship take-home challenge.

It does three things:

* Add a task
* List all tasks
* Mark a task as done

Tasks are kept in memory (just a Python list), so there's no database to set up. That also means the list clears out whenever the app or container restarts, which is expected for something this small.

## Tech Stack

Python 3.12, Flask, Docker, and GitHub Actions for CI.

## Project Structure

```text
todo-api/
├── .github/
│   └── workflows/
│       └── docker-build.yaml   # builds the Docker image on every push
├── app.py                      # the Flask app itself
├── requirements.txt            # pinned dependencies
├── Dockerfile
└── README.md
```

## How to Run It

The easiest way is with Docker.

```bash
docker build -t todo-api .
docker run -d -p 5000:5000 --name todo-api-container todo-api
```

Once that's running, the API is at `http://localhost:5000`. To check it's actually up:

```bash
docker ps
```

and you should see `todo-api-container` with a status of `Up ...`.

When you're done with it:

```bash
docker stop todo-api-container
docker rm todo-api-container
```

If you'd rather skip Docker and just run it locally:

```bash
python3 -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```



## Endpoints

### `POST /tasks` — add a task

Send a JSON body like:

```json
{ "title": "Learn Docker" }
```

and you'll get back:

```json
{ "id": 1, "title": "Learn Docker", "done": false }
```

If `title` is missing, blank, not a string, or the body isn't valid JSON at all, you'll get a `400` back instead, with a message explaining what's wrong, e.g.:

```json
{ "error": "title is required and must be a non-empty string" }
```

I added this validation because the original version just trusted whatever came in — sending an empty body would've quietly created a task with `title: null`, which didn't seem right for an API that's supposed to enforce a schema.

### `GET /tasks` — list tasks

Just returns whatever's in the list:

```json
[
  { "id": 1, "title": "Learn Docker", "done": false }
]
```

or `[]` if nothing's been added yet.

### `PUT /tasks/<id>/done` — mark a task done

Call it with the task's id, e.g. `PUT /tasks/1/done`, and it flips `done` to `true` and returns the updated task. If that id doesn't exist, you get a `404` with `{ "error": "Task not found" }` instead of a silent no-op.

Anything else — a route that doesn't exist, or a method a route doesn't support — also comes back as a JSON error (`404` or `405`) rather than Flask's default HTML error page, just so the API is consistent about always speaking JSON.

## Trying It Out

```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Learn Docker"}'
curl http://localhost:5000/tasks
curl -X PUT http://localhost:5000/tasks/1/done
```

That covers all three operations — create, list, and mark done.

## CI

There's a GitHub Actions workflow at `.github/workflows/docker-build.yaml` that runs on every push. It just checks out the code and runs `docker build -t todo-api .` to make sure the image still builds. It doesn't deploy anything or push the image anywhere — the challenge only asked for a build check, so I kept it at that.

## Reflection

### Trickiest Part

There was no particularly tricky part for me in this task. The implementation was straightforward because I already have hands-on experience with Docker, Git, GitLab, GitHub Actions, Jenkins, and on-premises Kubernetes environments. Because of this background, setting up the API, containerizing the application, and configuring the GitHub Actions workflow was familiar and straightforward.