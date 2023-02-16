from sqlalchemy import create_engine, text


def create_a_connection():
    # create a engine using sqlite in memery, it doesn't require anything to configure neither create files
    # to save data
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

    with engine.connect() as conn:
        result = conn.execute(text("select 'hi'"))
        print(result.all())