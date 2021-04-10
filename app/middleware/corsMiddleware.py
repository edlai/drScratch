class corsMiddleware(object):
    def process_response(self, req, resp):
        resp['Access-Control-Allow-Origin'] = '*'
        resp['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT'
        #response['Content-Type'] = 'application/json'
        #resp['Accept'] = 'application/x.scratch.sb3'
        return resp

