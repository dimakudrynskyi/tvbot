FROM python:3.8.0-buster

WORKDIR /tvBot_Project

COPY requirements.txt . 
RUN python3.8 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "TvBotProject.py"]
