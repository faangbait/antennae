FROM python:3-slim-bullseye
LABEL MAINTAINER="S Smith <@faangbait>"

EXPOSE 8000
STOPSIGNAL SIGTERM

RUN apt-get update && \
    apt-get install nginx git vim -y --no-install-recommends && \
    apt-get clean -y && \
    mkdir -p /opt/app/{src,pip_cache} && \
    pip install --upgrade --cache-dir /opt/app/pip_cache pip

COPY bin/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

COPY src/ /opt/app/src/
COPY requirements.txt /opt/app/src/
COPY bin/container-launch.sh /opt/app/src/

WORKDIR /opt/app/src/

RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache && \
    ./manage.py collectstatic --no-input && \
    chown -R www-data:www-data /opt/app

USER www-data

CMD [ "/opt/app/src/container-launch.sh" ]
