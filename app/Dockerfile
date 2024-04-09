FROM python:3.12.2
ARG DB_PASSWORD
ENV DB_PASSWORD=
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y python3
COPY . /app
EXPOSE 5000
CMD ["streamlit", "run", "Home.py"]
