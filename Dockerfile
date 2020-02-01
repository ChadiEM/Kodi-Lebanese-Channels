FROM python:3.8-alpine

RUN mkdir -p /opt/lc
WORKDIR /opt/lc
EXPOSE 12589

COPY requirements.txt /opt/lc
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/lc
ENTRYPOINT ["/opt/lc/start.sh"]