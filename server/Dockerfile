FROM python:3.9
# stdder stddin
ENV PYTHONUNBUFFERED=1
# python dont create .pyc
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /backend

RUN pip install --upgrade pip
COPY requirements/base.txt ./
RUN ls
RUN pip install -r base.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . /backend/
