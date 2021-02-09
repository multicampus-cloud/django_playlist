FROM elasticsearch:7.10.1

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app

RUN yum install -y gcc openssl-devel bzip2-devel libffi-devel wget make && \
    wget https://www.python.org/ftp/python/3.8.5/Python-3.8.5.tgz && \
    tar xzf Python-3.8.5.tgz && \
    Python-3.8.5/configure --enable-optimizations && \
    make altinstall Python-3.8.5 && \
    ln -s /usr/local/bin/python3.8 /bin/python3.8 && \
    yum install -y python3-devel mysql-devel && \
    pip3.8 install --upgrade pip && \
    pip3.8 install -r requirements.txt && \
    wget https://raw.githubusercontent.com/q3aql/ffmpeg-install/master/ffmpeg-install && \
    chmod a+x ffmpeg-install && \
    ./ffmpeg-install --install release

# COPY . /usr/src/app
CMD ["python3.8", "manage.py", "runserver", "0:8000"]
