FROM node:18-alpine AS frontend-build

WORKDIR /app

# Copy package.json and package-lock.json
COPY ./frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the frontend code
COPY ./frontend ./

# Build the React app
RUN CI=false npm run build

# Backend build stage
FROM python:3.10-slim AS backend-build

WORKDIR /app

# Copy requirements
COPY ./backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY ./backend ./

# Production stage
FROM nginx:alpine

# Copy built frontend files from frontend build stage
COPY --from=frontend-build /app/build /usr/share/nginx/html

# Copy custom nginx config
COPY ./frontend/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy backend from backend build stage
COPY --from=backend-build /app /app
COPY --from=backend-build /usr/local/lib/python3.10 /usr/local/lib/python3.10
COPY --from=backend-build /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Set environment variables for backend
ENV PYTHONPATH=/app

# Install supervisor to manage processes
RUN apk add --no-cache supervisor

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 80 8000

# Start supervisor which will start both nginx and backend
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
