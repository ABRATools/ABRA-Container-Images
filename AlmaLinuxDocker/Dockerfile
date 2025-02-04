FROM almalinux:latest

# Install the necessary packages
RUN dnf install -y epel-release && \
    dnf install -y \
    git \
    python3 \
    python3-pip \
    python3-devel \
    python3-setuptools \
    python3-numpy \
    gcc \
    make \
    nodejs \
    npm \
    wget \
    unzip \
    xz \
    bzip2 \
    tar \
    sudo \
    dbus-x11 \
    dbus \
    net-tools \
    dnf-plugins-core \
    which \
    && dnf clean all

# Enable CRB repository
RUN dnf config-manager --set-enabled crb

# Install libwebsockets
RUN dnf install -y libwebsockets-devel --enablerepo=epel-testing && \
    dnf clean all

# Install XFCE4
RUN dnf groupinstall -y "Xfce" && \
    dnf install -y xfce4-terminal && \
    dnf clean all

# Install TigerVNC
RUN dnf install -y tigervnc-server tigervnc-server-module && \
    dnf clean all

# setup xstartup for xfce4
RUN mkdir -p /usr/local/vnc
COPY ./xstartup /usr/local/vnc/xstartup

# copy service files
COPY ./*.service /etc/systemd/system/

# install novnc
RUN wget https://github.com/novnc/noVNC/archive/refs/tags/v1.5.0.tar.gz -O /tmp/novnc.tar.gz && \
    tar -xvf /tmp/novnc.tar.gz -C /usr/local/bin && \
    mv /usr/local/bin/noVNC-1.5.0 /usr/local/bin/novnc && \
    rm -f /tmp/novnc.tar.gz

# install websockify
RUN wget https://github.com/novnc/websockify/archive/refs/tags/v0.12.0.tar.gz -O /tmp/websockify.tar.gz && \
    tar -xvf /tmp/websockify.tar.gz -C /usr/local/bin && \
    mv /usr/local/bin/websockify-0.12.0 /usr/local/bin/websockify-install && \
    rm -f /tmp/websockify.tar.gz && \
    cd /usr/local/bin/websockify-install && \
    python3 setup.py install

# port 8888 = novnc
EXPOSE 8888
# port 7681 = ttyd
EXPOSE 7681