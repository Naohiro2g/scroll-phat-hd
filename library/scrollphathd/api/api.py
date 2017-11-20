from sys import exit
import scrollphathd
from scrollphathd.fonts import font3x5
from queue import Queue
from threading import Thread
from .action import Action

try:
    from flask import Blueprint, render_template, abort, request
except ImportError:
    exit("flask must be installed in order to use the api. Install with pip install flask")

scrollphathd_blueprint = Blueprint('scrollhat', __name__)
api_queue = Queue()

@scrollphathd_blueprint.route('/scroll', methods=["POST"])
def scroll():
    data = request.get_json()
    api_queue.put(Action("scroll", (data["x"], data["y"])))


@scrollphathd_blueprint.route('/show', methods=["POST"])
def show(text):
    data = request.get_json()
    api_queue.put(Action("write", data["text"]))


@scrollphathd_blueprint.route('/clear', methods=["POST"])
def clear():
    api_queue.put(Action("clear", {}))


def run():
    while True:
        action = api_queue.get(block=True)
        if action.action_type == "write":
            scrollphathd.write_string(action.data, font=font3x5)
            scrollphathd.show()

        if action.action_type == "clear":
            scrollphathd.clear()

        if action.action_type == "scroll":
            scrollphathd.scroll(action.data[0], action.data[1])
            scrollphathd.show()

def start_background_thread():
    api_thread = Thread(target=run())
    api_thread.start()
    api_thread.join()