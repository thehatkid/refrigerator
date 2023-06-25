import json
import math


def get_crontab():
    with open("data/dishtimers.json", "r") as f:
        return json.load(f)


def set_crontab(contents):
    with open("data/dishtimers.json", "w") as f:
        f.write(contents)


def add_job(job_type, job_name, job_details, timestamp):
    timestamp = str(math.floor(timestamp))
    job_name = str(job_name)
    ctab = get_crontab()

    if job_type not in ctab:
        ctab[job_type] = {}

    if timestamp not in ctab[job_type]:
        ctab[job_type][timestamp] = {}

    ctab[job_type][timestamp][job_name] = job_details
    set_crontab(json.dumps(ctab))


def delete_job(timestamp, job_type, job_name):
    timestamp = str(timestamp)
    job_name = str(job_name)
    ctab = get_crontab()

    del ctab[job_type][timestamp][job_name]

    # smh, not checking for empty timestamps. Smells like bloat!
    if not ctab[job_type][timestamp]:
        del ctab[job_type][timestamp]

    set_crontab(json.dumps(ctab))
