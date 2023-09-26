import sys, os, logging
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.udf import udf
from pyflink.table import DataTypes
from sklearn.ensemble import RandomForestClassifier
import numpy as np
# import pickle


KAFKA_HOST = 'kafka.confluent.svc.cluster.local'
KAFKA_PORT = '9092'
INPUT_TOPIC = 'fraud.transaction'
OUTPUT_TOPIC = 'fraud.model-prediction'


# model_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'rf_fraud.pkl')
# model = pickle.load(open(model_path, "rb"))


def predict(nb_tx_last_15m: int, nb_tx_last_30m: int):
    return np.random.choice([0, 1])

def main():

    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    # create table environment
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)
    t_env.get_config().set_local_timezone("Asia/Ho_Chi_Minh")
    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flink-sql-connector-kafka-1.16.1.jar')
    t_env.get_config().get_configuration().set_string("pipeline.jars", "file://{}".format(kafka_jar))

    t_env.register_function("predict", udf(predict, DataTypes.BIGINT(),DataTypes.BIGINT()))
    t_env.execute_sql(f"""

    CREATE TABLE input_table (
        user_id VARCHAR,
        amount DOUBLE,
        ts BIGINT,
        ts_formatted AS TO_TIMESTAMP(FROM_UNIXTIME(ts)),
        WATERMARK FOR ts_formatted AS ts_formatted - INTERVAL '0' SECOND
    )
    WITH (
        'connector' = 'kafka',
        'topic' = '{INPUT_TOPIC}',
        'properties.bootstrap.servers' = '{KAFKA_HOST}:{KAFKA_PORT}',
        'properties.group.id' = 'pyflink',
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
    """)
    print("Done input table")
    t_env.execute_sql(f"""
        CREATE TABLE output_table (user_id VARCHAR, ts BIGINT, prediction BIGINT)    
        WITH (
        'connector' = 'kafka',
        'topic' = '{OUTPUT_TOPIC}',
        'properties.bootstrap.servers' = '{KAFKA_HOST}:{KAFKA_PORT}',
        'format' = 'json'
        )
    """)
    print("Done output table")
    t_env.execute_sql("""
        INSERT INTO output_table
        SELECT A.user_id, A.ts, predict(A.nb_tx_last_15m, B.nb_tx_last_30m)
        FROM (
        SELECT user_id, ts, count(user_id) over w as nb_tx_last_30m
        FROM input_table
        WINDOW w AS (partition by user_id order by ts_formatted range between INTERVAL '30' MINUTES preceding and current row)
        ) B JOIN (SELECT user_id, ts
        , count(user_id) over w as nb_tx_last_15m
        FROM input_table
        WINDOW w AS (partition by user_id order by ts_formatted range between INTERVAL '15' MINUTES preceding and current row)
        ) A ON A.user_id = B.user_id
    """).wait()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    main()

   

 