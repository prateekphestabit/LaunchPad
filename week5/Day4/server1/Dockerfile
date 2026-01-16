FROM node:18-alpine
WORKDIR /app
COPY ./ ./
RUN npm install --production
EXPOSE 8000
CMD ["node", "server.js"]