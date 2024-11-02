FROM python:3-alpine AS build

# Create a virtual environment
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk add --update alpine-sdk

RUN pip uninstall urllib3 && \
    pip install urllib3==1.26.7 && \
    pip install --no-cache-dir -r requirements.txt


FROM python:3-alpine

# Copy the virtual environment from the first stage.
COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH

COPY mijnafvalwijzer-to-ical.py .

ENTRYPOINT [ "python", "./mijnafvalwijzer-to-ical.py" ]
