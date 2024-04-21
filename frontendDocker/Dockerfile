FROM python:3-alpine3.19
WORKDIR /user/src/app
COPY . .
RUN pip install -r requirements.txt
#EXPOSE 5000
CMD python3 ./todolist.py
