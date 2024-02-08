FROM python:latest

# Установка обновления pip
RUN pip install --upgrade pip

# Копируем requirement в контейнер
COPY ./requirement.txt ./

# Установка всех зависимостей
RUN pip install -r requirement.txt

# Копируем корневые директории в контейнер
COPY ./ ./app

# Объявление рвбочей директории
WORKDIR /app

# Запуск программы
RUN uvicorn main:app --reload

