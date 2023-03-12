FROM python:3.9-alpine
COPY ./ecomm_comp /ecomm_comp
COPY ./crontab /etc/cron.d/crontab
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN chmod a+x ./ecomm_comp/price_gathering_main.py
COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt
RUN crontab /etc/cron.d/crontab
RUN touch /tmp/out.log
CMD ["crond","-f"]