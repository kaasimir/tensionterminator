from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Time, Table
import psycopg2
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from psycopg2 import extensions
from datetime import datetime
import os
from moviepy.editor import VideoFileClip
import pandas as pd

Base = declarative_base()

db_params = {'user': input('Please Enter DB_User [postgres]:'),
             'password': input('Please Enter DB_PW:'),
             'host': 'localhost',
             'port': '5432',
             'database': 'ttdatabase'}

print(f"This script will create a new Database with the name: {db_params['database']}\n")

connection = psycopg2.connect(
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port'],
)
print(f"{connection}\n")

auto_comit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
connection.set_isolation_level(auto_comit)
cursor = connection.cursor()
try:
    cursor.execute(f"CREATE DATABASE {db_params['database']}")
    connection.commit()
    cursor.close()
    connection.close()
except Exception as e:
    cursor.close()
    connection.close()
    print(f"{e}")

db_url = f"postgresql://" \
            f"{db_params['user']}:" \
            f"{db_params['password']}@" \
            f"{db_params['host']}:" \
            f"{db_params['port']}/" \
            f"{db_params['database']}"

engine = create_engine(db_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
print(f"Connected to PostgreSQL, DB: {db_params['database']}")


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surename = Column(String)

    loops = relationship('Loop', back_populates='user')


# Relation Tables for M:M
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

    # M:M
    loop = relationship('Loop', secondary=tools_loop_association, back_populates='tools')


class Bodyside(Base):
    __tablename__ = 'bodyside'

    id = Column(Integer, primary_key=True)
    side = Column(String)
    time_in_use = Column(Time)

    # M:M
    loop = relationship('Loop', secondary=bodyside_loop_association, back_populates='bodysides')


class Loop(Base):
    __tablename__ = 'loop'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    session_length = Column(Integer)  # Seconds
    location = Column(String)
    human_labeled = Column(Boolean)

    # 1:M
    videos = relationship('Video', back_populates='loop')

    # M:1
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='loops')

    # M:M
    tools = relationship('Tools', secondary=tools_loop_association, back_populates='loop')
    bodysides = relationship('Bodyside', secondary=bodyside_loop_association, back_populates='loop')


class Video(Base):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True)
    device = Column(String)
    file_path = Column(String)

    # M:1
    loop_id = Column(Integer, ForeignKey('loop.id'))
    loop = relationship('Loop', back_populates='videos')


Base.metadata.create_all(engine)

'''Creating the current know user'''

users_inputs = [Users(name='unknown', surename='unknown'), Users(name='Christina', surename='Greiderer'),
                Users(name='Christine', surename='Lackinger'), Users(name='Juergen', surename='Zangerl'),
                Users(name='Lukas', surename='Prenner'), Users(name='Martin', surename='Hofer'),
                Users(name='Pirmin', surename='Aster'), Users(name='Robert', surename='Goller'),
                Users(name='Suganthi', surename='Manoharan'), Users(name='Philipp', surename='Egger'),
                Users(name='MartinPO', surename='Feuerstein')]

session.bulk_save_objects(users_inputs)
session.commit()

'''Creating the tool input'''

tools_inputs = [Tools(tool='unknown'),
                Tools(tool='trigger'),
                Tools(tool='small duoballs'),
                Tools(tool='big duoballs')]

session.bulk_save_objects(tools_inputs)
session.commit()

'''Creating the bodyside input'''

bodyside_inputs = [Bodyside(side='unknown'),
                   Bodyside(side='left'),
                   Bodyside(side='middle'),
                   Bodyside(side='right')]

session.bulk_save_objects(bodyside_inputs)
session.commit()

data_doc = pd.read_excel('Session_data.xlsx')


def get_video_duration(file_path):
    try:
        video_clip = VideoFileClip(file_path)
        duration = video_clip.duration
        video_clip.close()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None


def datacollector(source_directory: str, location: str):
    counter = 1

    for root, dirs, files in os.walk(source_directory):

        timestamp_str = '-'.join(os.path.basename(root).split('-')[1:])
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H_%M_%S.%f")
        except ValueError:
            print(f"Skipping invalid timestamp: {timestamp_str}")
            continue

        duration = get_video_duration(os.path.join(root, files[0]))

        if counter > 128:
            user_id = session.query(Tools).filter(Users.id == 1).first()
            tool = session.query(Tools).filter(Tools.id == 1).first()
            bodyside = session.query(Bodyside).filter(Bodyside.id == 1).first()
            human_labeled = False
        else:
            user = session.query(Users.id).filter(Users.name == data_doc['Users'][counter - 1]).first()
            user_id = user[0] if user else session.query(Tools).filter(Users.id == 1).first()
            tool = session.query(Tools).filter(Tools.tool == data_doc['Exercise'][counter - 1]).first()
            bodyside = session.query(Bodyside).filter(Bodyside.side == data_doc['BodySide'][counter - 1]).first()
            human_labeled = True

        new_loop = Loop(timestamp=timestamp,
                        location=location,
                        session_length=duration,
                        human_labeled=human_labeled,
                        user_id=user_id)
        session.add(new_loop)
        session.commit()

        new_loop.tools.append(tool)
        session.commit()

        new_loop.bodysides.append(bodyside)
        session.commit()

        for filename in files:

            if filename.split(".")[-1] != "mp4":
                filepath = os.path.join(root, filename)
                os.remove(filepath)

            if filename.split(".")[-1] == "mp4":
                filepath = os.path.join(os.path.abspath(root), filename)
                filepath = filepath.replace("\\", "/")
                print(filepath)
                device = filename.split(".")[0]
                new_video = Video(file_path=filepath, device=device, loop_id=counter)
                session.add(new_video)
                session.commit()

        counter += 1

    print("Done!")
    print(f"{db_params['database']} created!\n")


filepath = "./tt_video_data"

datacollector(filepath, 'MCI')
