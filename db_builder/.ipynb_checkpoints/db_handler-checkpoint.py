from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
import db_builder.db_structure as dbs


class DB_Conn():

    def __init__(self, db_params):
        self.user = db_params['user']
        self.password = db_params['password']
        self.host = db_params['host']
        self.port = db_params['port']
        self.database = db_params['database']
        self.db_url = None
        self.engine = None
        self.session = None

    def connect(self):
        try:
            self.db_url = f"postgresql://" \
                          f"{self.user}:" \
                          f"{self.password}@" \
                          f"{self.host}:" \
                          f"{self.port}/" \
                          f"{self.database}"

            self.engine = create_engine(self.db_url, echo=True)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            print(f"Connected to PostgreSQL, DB: {self.database}")

        except SQLAlchemyError as e:
            print(f"Connection Failed: {str(e)}")

    def disconnect(self):
        if self.session:
            self.session.close()
            print(f"Connection to {self.database} closed")

    def get_engine(self):
        return self.engine


    def get_filepath_with_trigger(self):

        loops_with_trigger = self.session.query(dbs.Loop).join(dbs.tools_loop_association).filter(
            dbs.Loop.human_labeled == True,
            dbs.tools_loop_association.c.tool_id == 1  # Modify this condition as needed
        ).all()

        loops_with_trigger_ids = []

        for x in loops_with_trigger:
            loops_with_trigger_ids.append(x.id)

        rgb_data_with_trigger = self.session.query(dbs.Video).join(dbs.Loop, dbs.Video.loop_id == dbs.Loop.id).filter(
            dbs.Video.device == 'rgbCam',
            dbs.Loop.id.in_(loops_with_trigger_ids)
        ).all()

        trigger_file_path_list = []

        for x in rgb_data_with_trigger:
            trigger_file_path_list.append(x.file_path)

        return trigger_file_path_list

    def get_filepath_with_duoballs(self):

        loops_with_buoballs = self.session.query(dbs.Loop).join(dbs.tools_loop_association).filter(
            dbs.Loop.human_labeled == True,
            dbs.tools_loop_association.c.tool_id != 1  # Modify this condition as needed
        ).all()

        loops_with_buoballs_ids = []

        for y in loops_with_buoballs:
            loops_with_buoballs_ids.append(y.id)

        rgb_data_with_buoballs = self.session.query(dbs.Video).join(dbs.Loop, dbs.Video.loop_id == dbs.Loop.id).filter(
            dbs.Video.device == 'rgbCam',
            dbs.Loop.id.in_(loops_with_buoballs_ids)
        ).all()

        buoballs_file_path_list = []

        for x in rgb_data_with_buoballs:
            buoballs_file_path_list.append(x.file_path)

        return buoballs_file_path_list

    def get_filepath_with_rightside(self):

        loops_with_rightside = self.session.query(dbs.Loop).join(dbs.bodyside_loop_association).filter(
            dbs.Loop.human_labeled == True,
            dbs.bodyside_loop_association.c.bodyside_id == 3  # Modify this condition as needed
        ).all()

        loops_with_rightside_ids = []

        for r in loops_with_rightside:
            loops_with_rightside_ids.append(r.id)

        rgb_data_with_rightside = self.session.query(dbs.Video).join(dbs.Loop,dbs.Video.loop_id == dbs.Loop.id).filter(
            dbs.Video.device == 'rgbCam',
            dbs.Loop.id.in_(loops_with_rightside_ids)
        ).all()

        rightside_file_path_list = []

        for x in rgb_data_with_rightside:
            rightside_file_path_list.append(x.file_path)

        return rightside_file_path_list
    
    
    def get_filepath_with_leftside(self):

        loops_with_leftside = self.session.query(dbs.Loop).join(dbs.bodyside_loop_association).filter(
            dbs.Loop.human_labeled == True,
            dbs.bodyside_loop_association.c.bodyside_id == 1  # Modify this condition as needed
        ).all()

        loops_with_leftside_ids = []

        for l in loops_with_leftside:
            loops_with_leftside_ids.append(l.id)

        rgb_data_with_leftside = self.session.query(dbs.Video).join(dbs.Loop,dbs.Video.loop_id == dbs.Loop.id).filter(
            dbs.Video.device == 'rgbCam',
            dbs.Loop.id.in_(loops_with_leftside_ids)
        ).all()

        leftside_file_path_list = []

        for x in rgb_data_with_leftside:
            leftside_file_path_list.append(x.file_path)

        return leftside_file_path_list
    
    def get_filepath_with_middle(self):

        loops_with_middle = self.session.query(dbs.Loop).join(dbs.bodyside_loop_association).filter(
            dbs.Loop.human_labeled == True,
            dbs.bodyside_loop_association.c.bodyside_id == 2  # Modify this condition as needed
        ).all()

        loops_with_middle_ids = []

        for m in loops_with_middle:
            loops_with_middle_ids.append(m.id)

        rgb_data_with_middle = self.session.query(dbs.Video).join(dbs.Loop,dbs.Video.loop_id == dbs.Loop.id).filter(
            dbs.Video.device == 'rgbCam',
            dbs.Loop.id.in_(loops_with_middle_ids)
        ).all()

        middle_file_path_list = []

        for x in rgb_data_with_middle:
            middle_file_path_list.append(x.file_path)

        return middle_file_path_list