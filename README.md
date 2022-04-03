# docker-centos7-tg2sip-rpms
A small repository to create, build and install tg2sip package

## Where to start
[Установка и настройка SIP шлюза для Telegram](https://voxlink.ru/kb/asterisk-configuration/ustanovka-i-nastrojka-sip-shljuza-dlja-telegram/)

## How to build
```bash
git clone https://github.com/Nurmukhamed/docker-centos7-tg2sip-rpms
cd docker-centos7-tg2sip-rpms
docker build -t tg2siprpms .
mkdir rpms
docker run -v $(pwd)/rpms:/rpms --env USERID=$(id -u) --env GROUPID=$(id -g) tg2siprpms /usr/local/bin/copyrpms.sh
```
