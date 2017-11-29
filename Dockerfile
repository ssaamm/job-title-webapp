FROM continuumio/miniconda3:latest
MAINTAINER Samuel Taylor "docker@samueltaylor.org"

RUN apt-get update && apt-get install -y supervisor
RUN conda install -y gunicorn

#ADD config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN conda install -y scikit-learn scipy pandas
RUN pip install gspread oauth2client

ADD src/ /app
WORKDIR /app
RUN python create_model.py clf.pkl vect.pkl

CMD ["/bin/bash"]
