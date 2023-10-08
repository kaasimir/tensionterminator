from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Time, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surename = Column(String)

    loops = relationship('Loop', back_populates='user')

#Relation Tables for M:M
tools_loop_association = Table(
    'tools_loop_association',
    Base.metadata,
    Column('tool_id', Integer, ForeignKey('tools.id')),
    Column('loop_id', Integer, ForeignKey('loop.id'))
)

bodyside_loop_association = Table(
    'bodyside_loop_association',
    Base.metadata,
    Column('bodyside_id', Integer, ForeignKey('bodyside.id')),
    Column('loop_id', Integer, ForeignKey('loop.id'))
)

class Tools(Base):
    __tablename__ = 'tools'

    id = Column(Integer, primary_key=True)
    tool = Column(String)
    time_in_use = Column(Time)

    #M:M
    loop = relationship('Loop', secondary=tools_loop_association, back_populates='tools')

class Bodyside(Base):
    __tablename__ = 'bodyside'

    id = Column(Integer, primary_key=True)
    side = Column(String)
    time_in_use = Column(Time)

    #M:M
    loop = relationship('Loop', secondary=bodyside_loop_association, back_populates='bodysides')


class Loop(Base):
    __tablename__ = 'loop'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    session_length = Column(Integer) #Seconds
    location = Column(String)
    human_labeled = Column(Boolean)

    #1:M
    videos = relationship('Video', back_populates='loop')

    #M:1
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='loops')

    #M:M
    tools = relationship('Tools', secondary=tools_loop_association, back_populates='loop')
    bodysides = relationship('Bodyside', secondary=bodyside_loop_association, back_populates='loop')


class Video(Base):
    __tablename__= 'video'

    id = Column(Integer, primary_key=True)
    device = Column(String)
    file_path = Column(String)

    #M:1
    loop_id = Column(Integer, ForeignKey('loop.id'))
    loop = relationship('Loop', back_populates='videos')