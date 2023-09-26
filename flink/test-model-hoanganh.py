import os
import sys
import logging
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings ,TableEnvironment
from pyflink.table.udf import udf
from pyflink.table import DataTypes
import requests

KAFKA_HOST = 'kafka.confluent.svc.cluster.local'
KAFKA_PORT = '9092'
INPUT_TOPIC = 'fraud.transaction'
OUTPUT_TOPIC = 'fraud.model-prediction'

# @udf(result_type=DataTypes.STRING())
# def predict(str):
#     return "1"

@udf(result_type=DataTypes.STRING())
def py_upper(str):
    "This capitalizes the whole string"
    try:
        return str.upper()
    except:
        return 'kocojca'
    
def main():
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    settings = EnvironmentSettings.new_instance() \
        .in_streaming_mode() \
        .build()                                        
    # Create table environment
    t_env = StreamTableEnvironment.create(stream_execution_environment=env,environment_settings=settings)
    t_env.get_config().set_local_timezone("Asia/Ho_Chi_Minh")

    kafka_jar = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flink-sql-connector-kafka-1.17.0.jar')
    t_env.get_config().get_configuration().set_string("pipeline.jars", "file://{}".format(kafka_jar))
    
    # predictfs = udf(predict,DataTypes.STRING(),DataTypes.STRING())
    # t_env.register_function("predict",predictfs)
    # t_env.register_function("predict", udf(predict, DataTypes.BIGINT(),DataTypes.BIGINT()))
    # t_env.create_temporary_function("PREDICT", predict)
    t_env.create_temporary_function("PY_UPPER", py_upper)

    src_ddl_ip = (f"""
    CREATE TABLE input_table (
        USER_ID VARCHAR,
        TRANSACTION_ID VARCHAR,
        AMT VARCHAR,
        TS VARCHAR
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
    t_env.execute_sql(src_ddl_ip)
    input_table = t_env.from_path('input_table')
    input_table.print_schema()
    
    # src_ddl_op = (f"""
    #     CREATE TABLE output_table (
    #         USER_ID VARCHAR,
    #         TRANSACTION_ID VARCHAR,
    #         AMT BIGINT,
    #         TS VARCHAR,
    #         PREDICT VARCHAR
    #               )     
    #     WITH (
    #     'connector' = 'kafka',
    #     'topic' = '{OUTPUT_TOPIC}',
    #     'properties.bootstrap.servers' = '{KAFKA_HOST}:{KAFKA_PORT}',
    #     'properties.group.id' = 'pyflink',
    #     'format' = 'json'
    #     )
    # """)
    # t_env.execute_sql(src_ddl_op)
    # output_table = t_env.from_path('output_table')
    # output_table.print_schema()

        #   cast( predict(1,1)  as string )
    sql= ("""
        select PY_UPPER(USER_ID),TRANSACTION_ID,AMT,TS 
        from input_table
    """)      

    # sql= ("""
    #     SELECT 
    #         A.USER_ID,
    #         A.TRANSACTION_ID, 
    #         A.TS, 
    #         predict(
    #             CONCAT( CAST(A.TRANSACTION_AMT as STRING) , ', ' ,
    #                     CAST(B.NUM_TRANSACTION_15M_WINDOW as STRING), ', ' ,
    #                     CAST(B.CUSTOMER_AVG_AMT_15M_WINDOW as STRING) , ', ' ,
    #                     CAST(C.NUM_TRANSACTION_30M_WINDOW as STRING) , ', ' ,
    #                     CAST(C.CUSTOMER_AVG_AMT_30M_WINDOW as STRING) )
    #             )        
    #     FROM (SELECT USER_ID, TRANSACTION_ID, TS, AMT as TRANSACTION_AMT FROM input_table) A
    #     JOIN (SELECT USER_ID, count(TRANSACTION_ID) over w as NUM_TRANSACTION_15M_WINDOW, avg(AMT) over w as CUSTOMER_AVG_AMT_15M_WINDOW
    #     FROM input_table
    #     WINDOW w AS (partition by USER_ID order by TS_FORMATTED range between INTERVAL '15' MINUTES preceding and current row)
    #     ) B 
    #     ON A.USER_ID = B.USER_ID
    #     JOIN (SELECT USER_ID, count(TRANSACTION_ID) over w as NUM_TRANSACTION_30M_WINDOW, avg(AMT) over w as CUSTOMER_AVG_AMT_30M_WINDOW
    #     FROM input_table
    #     WINDOW w AS (partition by USER_ID order by TS_FORMATTED range between INTERVAL '30' MINUTES preceding and current row)
    #     ) C 
    #     ON A.USER_ID = C.USER_ID
    # """)

    
    revenue_tbl = t_env.sql_query(sql)
    revenue_tbl.execute().print()
    # revenue_tbl.execute_insert('output_table').wait()

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    main()
