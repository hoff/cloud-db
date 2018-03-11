import webapp2, json
from google.appengine.ext import ndb


class Document(ndb.Model):
    json = ndb.JsonProperty()

class HomeEndpoint(webapp2.RequestHandler):
    def get(self):
        return self.response.out.write('up and running')

class DocumentEndpoint(webapp2.RequestHandler):
    
    def get(self, document_id):
        allow_cors(self)
        document = Document.get_by_id(int(document_id))
        if document:
            return_json(self, {'id': document.key.id(), 'document': document.json})
        else:
            self.error(404)

    def put(self, document_id):
        allow_cors(self)
        data = json.loads(self.request.body)
        document_key = Document(json = data).put()
        document = document_key.get()
        response = {'id': document.key.id(), 'document': document.json}
        return_json(self, response)

    def post(self, document_id):
        allow_cors(self)
        document = Document.get_by_id(int(document_id))
        data = json.loads(self.request.body)
        document.json = data
        document.put()
        return_json(self, {'id': document.key.id(), 'document': document.json})

    def delete(self, document_id):
        # todo
        pass

    def options(self, document_id):
        allow_cors(self)

def allow_cors(request):
    """
    set the appropriate response headers for cross-origin requests
    """
    request.response.headers['Access-Control-Allow-Credentials'] = 'true'
    request.response.headers['Access-Control-Allow-Origin'] = '*'
    request.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    request.response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE'


def return_json(handler, data):
    """
    returns JSON from an object to a given request handler
    """
    handler.response.headers['Content-Type'] = 'application/json; charset=utf-8'
    handler.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication(
    [
        ('/api/documents/(\d+)', DocumentEndpoint),
        ('/', HomeEndpoint),
        # for put only
        #('/api/documents', DocumentEndpoint),
    ],
    debug=True
)