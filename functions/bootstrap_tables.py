# Create all tables if not exists in the database using sqlalchemy

from macrosurfer.database import Database

if __name__ == "__main__":
    print("Bootstrapping tables...")
    db = Database()
    engine = db.get_engine()
    session = db.get_session()

    # Create all tables if not exists in the database using sqlalchemy
    metadata = db.get_metadata()
    metadata.create_all(engine)
    print("Tables created successfully")
