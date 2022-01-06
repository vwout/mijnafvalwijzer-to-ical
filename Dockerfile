FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY mijnafvalwijzer-to-ical.py .

ENTRYPOINT [ "python", "./mijnafvalwijzer-to-ical.py" ]
