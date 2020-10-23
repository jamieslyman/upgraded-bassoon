from tg import expose, TGController, MinimalApplicationConfigurator
from wsgiref.simple_server import make_server

class RootController(TGController):
    @expose()
    def index(self):
        return 'Hello World!'
    @expose('hello.xhtml')
    def hello(self, person=None):
        return dict(person=person)
config = MinimalApplicationConfigurator()
config.update_blueprint({
    'root_controller': RootController(),
    'renderers': ['kajiki']
})
application = config.make_wsgi_app()
print("Serving on port 8080!")
httpd = make_server('', 8080, application)
httpd.serve_forever()