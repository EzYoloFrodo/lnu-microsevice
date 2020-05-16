FROM node:lts-alpine

EXPOSE 8080

# делаем каталог 'app' текущим рабочим каталогом
WORKDIR /web

# копируем оба 'package.json' и 'package-lock.json' (если есть)
COPY web/package*.json ./

# устанавливаем зависимости проекта
RUN npm install

# копируем файлы и каталоги проекта в текущий рабочий каталог (т.е. в каталог 'app')
COPY web/. .

# собираем приложение для production с минификацией
CMD ["npm", "run", "serve"]
