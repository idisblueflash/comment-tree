FROM python:3.8.12
RUN mkdir /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
COPY . /app
WORKDIR /app
ENV FLASK_DEBUG=1
ENV FLASK_APP=comment-tree.py
ENV FLASK_CONFIG=default
RUN cd /app/app
EXPOSE 5000
CMD flask run --host 0.0.0.0
