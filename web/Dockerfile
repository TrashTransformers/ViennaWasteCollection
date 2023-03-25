FROM node:18.15.0 as node
WORKDIR /app
VOLUME /app-volume
COPY . .
RUN npm install
RUN npm run build --prod
# Stage 2
FROM nginx:alpine
COPY --from=node /app/dist/web-app /usr/share/nginx/html