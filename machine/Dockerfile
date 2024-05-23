FROM  python:3.9

WORKDIR /machine 
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    zlib1g-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h 
RUN python -m pip install --upgrade pip

COPY . /machine
RUN pip3 install  setuptools wheel
RUN pip3 install Cython==0.29.36
RUN pip3 install --no-binary=h5py h5py
RUN pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v461 tensorflow
RUN pip3 install -Ur ./requirements.txt --verbose

CMD [ "python3", "/machine/main.py" ]