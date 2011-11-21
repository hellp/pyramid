import os
import sys

from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config
import transaction

from ..models import DBSession
from ..models import MyModel
from ..models import Base

def usage(argv):
    print('usage: %s <Pyramid ini filename>' % os.path.basename(argv[0]))
    sys.exit(1)

def main(argv=sys.argv):
    try:
        config_filename = argv[1]
    except IndexError:
        usage(argv)
    settings = appconfig('config:' + os.path.abspath(config_filename))
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        model = MyModel(name=u'first', value=55)
        DBSession.add(model)
