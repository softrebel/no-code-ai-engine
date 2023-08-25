# no-code-ai-engine
No Code AI Engine



- Run Celery:

```bash
celery -A celery_tasks.app worker -l INFO
```

- Run Celery Beat:

```bash
celery -A celery_tasks.app beat -S redbeat.RedBeatScheduler -l INFO
```
