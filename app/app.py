import falcon
import json


class RunRecSession(object):
    def on_put(self, req, resp, name):
        """Handles PUT requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps({"Nom du bénévole": name})


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
run_rec = RunRecSession()

# things will handle all requests to the '/things' URL path
app.add_route('/run_rec/{name}', run_rec)
