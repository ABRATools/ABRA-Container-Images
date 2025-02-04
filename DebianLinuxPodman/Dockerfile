FROM debian:latest

RUN apt update && apt upgrade -y

ENV container docker
ENV DEBIAN_FRONTEND=noninteractive

# Install the necessary packages
RUN apt install -y \
    systemd systemd-sysv nano \
    git python3 python3-pip python3-setuptools \
    python3-numpy gcc make nodejs npm wget unzip \
    tar sudo dbus-x11 dbus net-tools gnu-which \
    libwebsockets-dev build-essential cmake git \
    libjson-c-dev xfce4 xfce4-terminal xfce4-goodies xterm \
    tigervnc-standalone-server tigervnc-xorg-extension \
    && apt clean

# setup xstartup for xfce4
RUN mkdir -p /usr/local/vnc
COPY ./xstartup /usr/local/vnc/xstartup
RUN chmod 0755 /usr/local/vnc/xstartup

# copy service files
COPY ./*.service /etc/systemd/system/
RUN chmod 0644 /etc/systemd/system/*.service

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

# install ttyd
RUN wget https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -O /usr/local/bin/ttyd && \
    chmod +x /usr/local/bin/ttyd

# Enable and start the services
RUN systemctl enable dbus && \
    systemctl enable tigervnc@root.service && \
    systemctl enable novnc-websockify@root.service && \
    systemctl enable ttyd@root.service

# port 8888 = novnc, port 7681 = ttyd
EXPOSE 5801 7681

# Start systemd
CMD ["/sbin/init"]