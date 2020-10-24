from tg import expose, TGController, MinimalApplicationConfigurator
from tg.configurator.components.sqlalchemy import SQLAlchemyConfigurationComponent
from tg.util import Bunch
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from wsgiref.simple_server import make_server
from datetime import datetime


class RootController(TGController):
    @expose(content_type='text/plain')
    def index(self):
        logs = DBSession.query(Log).order_by(Log.timestamp.desc()).all()
        return 'Past Greetings\n' + '\n'.join(['%s - %s' % (l.timestamp, l.person) for l in logs])

    @expose('hello.xhtml')
    def hello(self, person=None):
        DBSession.add(Log(person=person or ''))
        DBSession.commit()
        return dict(person=person)


DeclarativeBase = declarative_base()
DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False))


class Log(DeclarativeBase):
    __tablename__ = 'logs'

    uid = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    person = Column(String(50), nullable=False)


def init_model(engine):
    DBSession.configure(bind=engine)
    DeclarativeBase.metadata.create_all(engine)


config = MinimalApplicationConfigurator()
config.register(SQLAlchemyConfigurationComponent)
config.update_blueprint({
    'use_sqlalchemy': True,
    'sqlalchemy.url': 'postgres://postgres:[INSERT POSTGRES PASSWORD HERE]@localhost:5432/postgres',
    'root_controller': RootController(),
    'renderers': ['kajiki'],
    'model': Bunch(
        DBSession=DBSession,
        init_model=init_model
    )
})
application = config.make_wsgi_app()
print("Serving on port 8080!")
httpd = make_server('', 8080, application)
httpd.serve_forever()
