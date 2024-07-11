FROM python:3.11-bullseye as spark-base

ARG SPARK_VERSION=3.4.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        curl \
        vim \
        unzip \
        rsync \
        openjdk-11-jdk \
        build-essential \
        software-properties-common \
        ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=/opt/spark \
    HADOOP_HOME=/opt/hadoop \
    PATH=/opt/spark/sbin:/opt/spark/bin:$PATH \
    SPARK_MASTER=spark://spark-master:7077 \
    SPARK_MASTER_HOST=spark-master \
    SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    PYSPARK_PYTHON=python3 \
    PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

RUN mkdir -p ${HADOOP_HOME} ${SPARK_HOME} && \
    curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory ${SPARK_HOME} --strip-components=1 && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /tmp/spark-events

COPY spark-defaults.conf $SPARK_HOME/conf/
COPY entrypoint.sh .
RUN chmod u+x /opt/spark/sbin/* /opt/spark/bin/* ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
