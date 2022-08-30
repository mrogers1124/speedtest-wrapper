# Load results from raw directory into sqlite DB
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import datapath, rawpath, processedpath, errorpath
from models import Base, Interface, Server, Result


# Database path and engine
dbpath = os.path.join(datapath, 'results.sqlite3')
engine = create_engine(f'sqlite:///{dbpath}', echo=True)
Session = sessionmaker(bind=engine)

# Create DB tables if needed
Base.metadata.create_all(engine)


# Get or create model object
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


# Load the result into the DB
def load_result_to_db(result_str: str, session):
    result = json.loads(result_str)

    interface: Interface = get_or_create(session, Interface, **result['interface'])
    server: Server = get_or_create(session, Server, **result['server'])

    kwargs = {
        'timestamp': result['timestamp'],
        'ping_jitter': result['ping']['jitter'],
        'ping_latency': result['ping']['latency'],
        'ping_low': result['ping']['low'],
        'ping_high': result['ping']['high'],
        'download_bandwidth': result['download']['bandwidth'],
        'download_bytes': result['download']['bytes'],
        'download_elapsed': result['download']['elapsed'],
        'download_latency_iqm': result['download']['latency']['iqm'],
        'download_latency_low': result['download']['latency']['low'],
        'download_latency_high': result['download']['latency']['high'],
        'download_latency_jitter': result['download']['latency']['jitter'],
        'upload_bandwidth': result['upload']['bandwidth'],
        'upload_bytes': result['upload']['bytes'],
        'upload_elapsed': result['upload']['elapsed'],
        'upload_latency_iqm': result['upload']['latency']['iqm'],
        'upload_latency_low': result['upload']['latency']['low'],
        'upload_latency_high': result['upload']['latency']['high'],
        'upload_latency_jitter': result['upload']['latency']['jitter'],
        'packetLoss': result['packetLoss'] if 'packetLoss' in result else None,
        'isp': result['isp'],
        'interface_uid': interface.interface_uid,
        'server_uid': server.server_uid,
        'result_id': result['result']['id'],
        'result_url': result['result']['url'],
        'result_persisted': result['result']['persisted']
    }

    new_result = Result(**kwargs)
    session.add(new_result)
    session.commit()


if __name__ == '__main__':
    # Open a DB session
    with Session() as session:

        # Iterate through files in raw data directory
        for fn in sorted(os.listdir(rawpath)):
            fp = os.path.join(rawpath, fn)
            with open(fp, 'r') as file:
                result_str = file.read()

            try:
                # Load the result into the DB
                load_result_to_db(result_str, session)

                # Move the raw file into the processed folder
                fp_processed = os.path.join(processedpath, fn)
                os.rename(fp, fp_processed)

            except KeyError:
                # Move the raw file into the error folder
                fp_error = os.path.join(errorpath, fn)
                os.rename(fp, fp_error)
