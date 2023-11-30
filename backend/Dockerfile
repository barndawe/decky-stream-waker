FROM ghcr.io/steamdeckhomebrew/holo-base:latest

RUN mkdir /pacman && pacman -Sydd --noconfirm --dbpath /var/lib/pacman python-pip

RUN pip3 install wakeonlan --target=/wakeonlan
RUN pip3 install protobuf==3.19.0 --target=/protobuf

ENTRYPOINT [ "/backend/entrypoint.sh" ]
