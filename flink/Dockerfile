FROM flink:1.17.1-scala_2.12-java11

RUN apt-get update -y && \
apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libffi-dev liblzma-dev && \
wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz && \
tar -xvf Python-3.7.9.tgz && \
cd Python-3.7.9 && \
./configure --without-tests --enable-shared && \
make -j6 && \
make install && \
ldconfig /usr/local/lib && \
cd .. && rm -f Python-3.7.9.tgz && rm -rf Python-3.7.9 && \
ln -s /usr/local/bin/python3 /usr/local/bin/python && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

RUN cp  /opt/flink/opt/flink-python-1.17.1.jar /opt/flink/lib

COPY requirement.txt .
 
# install PyFlink
RUN pip3 install -r requirement.txt
 
# add python script

USER flink

RUN mkdir /opt/flink/usrlib
ADD test-model.py /opt/flink/usrlib/test-model.py
ADD test-model-hoanganh.py /opt/flink/usrlib/test-model-hoanganh.py
ADD test-model-dzung.py /opt/flink/usrlib/test-model-dzung.py

COPY flink-sql-connector-kafka-1.16.1.jar /opt/flink/usrlib
COPY flink-sql-connector-kafka_2.11-1.13.0.jar /opt/flink/usrlib
COPY flink-sql-connector-kafka-1.17.0.jar /opt/flink/usrlib


