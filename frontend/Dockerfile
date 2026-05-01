FROM node:18-alpine

WORKDIR /app

# Copiar package.json (cuando exista) y luego el resto
COPY package*.json ./
RUN npm install

# Copiar el resto del código (se sobrescribe con volumen)
COPY . .

# Exponer puerto de Vite
EXPOSE 5173

# Comando para desarrollo con hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]