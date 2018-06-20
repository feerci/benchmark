FROM continuumio/miniconda3

WORKDIR /usr/src/app
RUN conda update -n base conda && conda config --set show_channel_urls True
RUN conda create --name bob_py3 --override-channels \
  -c https://www.idiap.ch/software/bob/conda -c defaults \
  python=3 bob && \
   conda config --env --add channels defaults && \
   conda config --env --add channels https://www.idiap.ch/software/bob/conda && \
   conda install bob.measure
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
RUN pip install Cython
ADD requirements.txt /usr/src/app
RUN pip install -r requirements.txt
ADD . /usr/src/app
VOLUME /usr/src/app
CMD bash ./benchmark_run.sh

