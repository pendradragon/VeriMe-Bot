FROM python:3.9

WORKDIR /usr/src/app

# Copy requirements and upgrade dependency tools
COPY requirements.txt . 
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]