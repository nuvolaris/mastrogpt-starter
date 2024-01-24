FROM ubuntu:22.04
RUN \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN \
    export TZ=Europe/London ; ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
    apt-get update && apt-get -y upgrade &&\
    apt-get -y install curl wget gpg zip unzip software-properties-common apt-utils unzip vim silversearcher-ag
RUN \
    apt-get update &&\
    apt-get -y install \
    sudo socat telnet \
    inetutils-ping \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    build-essential gettext-base \
    git gnupg curl wget jq kafkacat \
    zlib1g-dev libbz2-dev libncurses5-dev \
    libgdbm-dev libnss3-dev libssl-dev \
    libreadline-dev libffi-dev libsqlite3-dev liblzma-dev
RUN \ 
    sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/bin
RUN \
    BUILD="3.0.1-beta.2401121536" ;\
    ARCH="$(dpkg --print-architecture)" ;\
    FILE="nuv_$(echo $BUILD)_$ARCH.deb" ;\
    URL="https://github.com/nuvolaris/nuv/releases/download/$BUILD/$FILE" ;\
    rm -Rvf /tmp/nuv-installer ;\
    mkdir /tmp/nuv-installer ;\
    wget $URL -O "/tmp/nuv-installer/$FILE" ;\
    dpkg -i "/tmp/nuv-installer/$FILE"
ENV TZ=Europe/London
RUN useradd -m nuvolaris -s /bin/bash &&\
    echo "nuvolaris ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
USER nuvolaris
WORKDIR /home/nuvolaris
ADD setup.source /home/nuvolaris/.setup.source
ADD init.sh /usr/sbin/init.sh
RUN cat .setup.source .aliases >.bashrc ;\
    /bin/bash -c 'source /home/nuvolaris/.bashrc'
# proxy to docker and keep alive
ENTRYPOINT ["/bin/bash", "/usr/sbin/init.sh"]