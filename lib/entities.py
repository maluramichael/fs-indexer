import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Directory(Base):
    __tablename__ = 'directories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.String, unique=True)
    mtime = sqlalchemy.Column(sqlalchemy.DateTime)
    files = relationship('Entry', backref='directory')


class Entry(Base):
    __tablename__ = 'entries'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    path = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('directories.id'))
    name = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.Enum('dir', 'file', 'image', 'video', name='type'))

    # os.stat
    mtime = sqlalchemy.Column(sqlalchemy.DateTime)
    size = sqlalchemy.Column(sqlalchemy.Integer)

    __table_args__ = (
        sqlalchemy.UniqueConstraint('path', 'name'),
    )
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'file'
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r})"


class Image(Entry):
    __tablename__ = 'images'

    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('entries.id'), primary_key=True)
    width = sqlalchemy.Column(sqlalchemy.Integer)
    height = sqlalchemy.Column(sqlalchemy.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }


class Video(Entry):
    __tablename__ = 'videos'

    id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('entries.id'), primary_key=True)
    width = sqlalchemy.Column(sqlalchemy.Integer)
    height = sqlalchemy.Column(sqlalchemy.Integer)
    duration_in_seconds = sqlalchemy.Column(sqlalchemy.Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }


class System(Base):
    __tablename__ = 'system'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    value = sqlalchemy.Column(sqlalchemy.String)
