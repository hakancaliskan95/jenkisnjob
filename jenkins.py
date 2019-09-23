import requests

class JenkinsApi:

    def __init__(self, baseurl, user=None, password  =None):
        self.baseurl = baseurl
        self.user = user
        self.password = password

    def get_all_jobs(self):
        url = '%s/api/json?tree=jobs[name,url,color]' % self.baseurl
        resp = self.get(url)
        return resp['jobs']

    def get_job_status(self, job):
        url = '%s/lastBuild/api/json' % job['url']
        resp = self.get(url)
        return resp


    def get(self,url):
         response =  requests.get(url, auth=(self.user, self.password))
         if response.status_code != 200:
             raise Exception('Api Error: Http status code is not 200, credentials may be incorrect')
         return response.json()








