import json
import uuid
import os 
import glob
import pandas as pd
import logging



def get_columns(ds):
    schema_file_path = os.environ.setdefault('SCHEMAS_FILE_PATH', 'data/retail_db/schemas.json')
    with open(schema_file_path) as fp:
        schemas = json.load(fp)
    try:
        schema = schemas.get(ds)
        if not schema:
            raise KeyError
        cols = sorted(schema, key=lambda s: s['column_position'])
        columns = [col['column_name'] for col in cols]
        return columns 
    except KeyError as ke:
        logging.error(f'Schema not found for {ds}')
        raise


def process_file(src_base_dir, ds, tgt_base_dir):
    for file in glob.glob(f'{src_base_dir}/{ds}/part*'):
        try:
            df = pd.read_csv(file, names=get_columns(ds))
            os.makedirs(f'{tgt_base_dir}/{ds}', exist_ok=True)
            df.to_json(
                f'{tgt_base_dir}/{ds}/part-{str(uuid.uuid1())}.json',
                orient='records',
                lines=True
            )
            logging.info(f'Number of records processed for {os.path.split(file)[1]} is {ds} is {df.shape[0]}')
        except KeyError:
            raise

def main():
    log_file_path = os.environ['LOG_FILE_PATH']
    src_base_dir = os.environ['SRC_BASE_DIR']
    tgt_base_dir = os.environ['TGT_BASE_DIR']
    logging.basicConfig(
        level=logging.INFO,
        filename=log_file_path,
        format='%(levelname)s %(asctime)s %(message)s'
    )

    datasets = os.environ.get('DATASETS')
    logging.info('File format conversion: Successful')
    if not datasets:
        for path in glob.glob(f'{src_base_dir}/*'):
            if os.path.isdir(path):
                process_file(src_base_dir, os.path.split(path)[1], tgt_base_dir)
    else:
        dirs = datasets.split(',')
        for ds in dirs:
            try:
                process_file(src_base_dir, ds, tgt_base_dir)    
            except Exception as e:
                logging.error(f'File format conversion for {ds} is not successful')
    logging.info('File format conversion: Successful')

if __name__ == "__main__":
    main()
