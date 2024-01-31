
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from images_crawler.models import Base, ImageModel

class DatabaseManager:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_image(self, image_data):
        session = self.Session()
        try:
            image = ImageModel(**image_data)
            session.add(image)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def dispose(self):
        self.engine.dispose()