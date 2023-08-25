from celery_tasks import app


def run():
    app.send_task("tasks.manage_execute", ("64a947ec4948b52a1aca476d",))
    worker = app.Worker()
    worker.start()


if __name__ == "__main__":
    run()
