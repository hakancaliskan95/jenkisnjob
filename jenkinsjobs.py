import os
import datetime
from jenkins import JenkinsApi
from jenkinsdb import Database


def get_database(dbName):

    exists = os.path.exists(dbName)
    database = Database(dbName)
    cursor = database.query("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'").fetchall()
    count = len(cursor)

    if count < 1:
        jobs = {'id': 'integer NOT NULL PRIMARY KEY AUTOINCREMENT', 'name': 'varchar(254) NOT NULL',
                'url': 'text',  'status': 'varchar(20) NOT NULL', 'date': 'datetime NOT NULL', 'build_url': 'text', 'build_id':'integer NOT NULL'}
        database.createTable('jobs', jobs)
    return database


def main():
    database = get_database('jobs.db')

    api = JenkinsApi('http://localhost:8080','admin','admin')
    jobs = api.get_all_jobs()
    print('\nJobs:\n\n')
    for job in jobs:
        last_build = api.get_job_status(job)
        date = datetime.datetime.fromtimestamp(last_build['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        jobdb = database.query("SELECT count(),build_id FROM jobs WHERE name=?", (job['name'],)).fetchone()
        status = 0
        if jobdb[0] < 1:
            sql = database.execute("INSERT INTO jobs(name, url, status, date, build_url, build_id) VALUES (?,?,?,?,?,?)",
                                    (job['name'], job['url'],  last_build['result'], last_build['url'], last_build['id'], date))
            status = 1
        else:
            if jobdb[1] != int(last_build['id']):
                sql = database.execute("UPDATE jobs SET  status = ?, date = ?, build_url = ?, build_id = ?", (last_build['result'], date, last_build['url'], last_build['id']))
                status = 2


        status_texts = [
            'no changed',
            'inserted',
            'updated'
        ]
        print('Job: {0} , satus: {1} - url: {2} date: {3} -> {4}'.format(job['name'], last_build['result'], last_build['url'], date, status_texts[status]))

    database.close()
if __name__ == "__main__":
    main()
