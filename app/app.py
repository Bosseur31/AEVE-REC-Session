import falcon
import json
import subprocess
import rec


class RunRecSession(object):
    def on_put(self, req, resp, name):
        """Handles PUT requests"""
        pid = rec.rec_video(name)
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({"Nom du bénévole": name})


class StopRecSession(object):
    def on_get(self, req, resp):
        """Handles PUT requests"""
        pid = rec.unrec_video()
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({"Pid": pid})


# falcon.API instances are callable WSGI apps
app = falcon.App()

# Resources are represented by long-lived class instances
run_rec = RunRecSession()
stop_rec = StopRecSession()

# things will handle all requests to the '/things' URL path
app.add_route('/run_rec/{name}', run_rec)
app.add_route('/stop_rec', stop_rec)
