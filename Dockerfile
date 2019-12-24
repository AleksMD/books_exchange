FROM python:3.7
COPY . app/books_sharing
WORKDIR app/books_sharing
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python3 -m manage runserver
