from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            if task.completed_at:
                tasks_response.append({
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : True
            })
            else:
                tasks_response.append({
                "id" : task.task_id,
                "title" : task.title,
                "description" : task.description,
                "is_complete" : False
            })
   
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"],
            is_complete = request_body["is_complete"]
        )
        db.session.add(new_task)
        db.session.commit()

        return make_response(f"{new_task.name} has successfully been added to your task list", 201)

@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if request.method == "GET":
        return {"task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True

        }}
