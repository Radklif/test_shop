from python:alpine

ENV WD /app
ENV AD ./app 

EXPOSE 8000
WORKDIR ${WD}
COPY requirements.txt . ${WD} 
RUN pip install -r requirements.txt

COPY ${AD} ${WD}
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
