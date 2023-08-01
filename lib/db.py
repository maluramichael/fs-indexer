import sqlalchemy
from sqlalchemy.orm import Session

from lib.entities import Base, Entry

engine = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=False)

bulk_size = 50
bulk = []
session = Session(engine)


def create_db():
    Base.metadata.create_all(engine)


def flush_bulk():
    session.bulk_save_objects(bulk)
    session.commit()
    session.close()

    bulk.clear()


def bulk_add(entry):
    bulk.append(entry)

    if len(bulk) >= bulk_size:
        flush_bulk()


def get_entry(meta_data):
    return session.query(Entry).filter_by(
        path=meta_data['path'].directory,
        name=meta_data['name']
    ).first()
