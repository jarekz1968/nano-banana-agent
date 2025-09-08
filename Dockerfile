FROM python:3.10-slim

# ustawiamy katalog roboczy
WORKDIR /app

# kopiujemy i instalujemy zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# kopiujemy całą resztę kodu
COPY . .

# komenda startu aplikacji
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

