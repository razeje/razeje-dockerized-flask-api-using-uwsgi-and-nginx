
FROM python:3

WORKDIR ./loginapi
COPY .  /loginapi
RUN pip install -r /loginapi/requirements.txt
RUN chmod +x /loginapi/entrypoint.sh


#CMD ["uwsgi","--ini", "app.ini"]
#ENTRYPOINT["entrypoint.sh"]




