FROM python:3.5-slim

WORKDIR /machine 
#RUN apt update && apt install -y libhdf5-dev

RUN python -m pip install --upgrade pip

COPY . /machine
RUN pip3 install  setuptools wheel
RUN pip install --no-binary h5py h5py
RUN pip3 install -r ./requirements.txt --verbose

CMD [ "python3", "/machine/main.py" ]