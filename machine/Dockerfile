FROM python:3.9-slim

WORKDIR /machine 
#RUN apt-get update && apt-get install -y libhdf5-dev

RUN python -m pip install --upgrade pip

COPY . /machine
RUN pip3 install  setuptools wheel
RUN pip3 install -r ./requirements.txt --verbose

CMD [ "python3", "/machine/main.py" ]