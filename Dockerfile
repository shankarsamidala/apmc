FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# ✅ Start Django using `python manage.py runserver`
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]