FROM openjdk:8-jdk-slim

RUN apt-get update && \
    apt-get install -y wget python3 python3-pip && \
    apt-get clean

ENV FLUME_VERSION=1.9.0
ENV FLUME_HOME=/opt/flume
ENV PATH=$FLUME_HOME/bin:$PATH

RUN wget https://archive.apache.org/dist/flume/${FLUME_VERSION}/apache-flume-${FLUME_VERSION}-bin.tar.gz && \
    tar -xzf apache-flume-${FLUME_VERSION}-bin.tar.gz && \
    mv apache-flume-${FLUME_VERSION}-bin $FLUME_HOME && \
    rm apache-flume-${FLUME_VERSION}-bin.tar.gz

RUN pip3 install pymongo neo4j

COPY flume.conf $FLUME_HOME/conf/flume.conf
COPY ./app /app
COPY exec-sink/target/exec-sink-1.0.jar $FLUME_HOME/lib/exec-sink.jar

WORKDIR $FLUME_HOME
CMD ["flume-ng", "agent", "--conf", "/opt/flume/conf", "--conf-file", "/opt/flume/conf/flume.conf", "--name", "agent", "-Dflume.root.logger=INFO,console"]
