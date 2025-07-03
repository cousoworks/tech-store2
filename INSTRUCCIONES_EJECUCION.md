# Instrucciones para ejecutar el proyecto TechStore

## Opción 1: Usando Docker Compose (recomendado)

### 1A: Entorno de desarrollo (con hot-reload)

Este método es ideal para desarrollo, ya que los cambios en el código se actualizan automáticamente.

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema
2. Abre una terminal en la raíz del proyecto
3. Ejecuta:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```
4. Espera a que los servicios inicien (puede tardar unos minutos la primera vez)
5. Accede a la aplicación en: http://localhost:3000
6. La API estará disponible en: http://localhost:8000/api/v1
7. Los cambios que hagas en el código se actualizarán automáticamente

### 1B: Entorno de producción

Este método simula el entorno de producción completo:

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema
2. Abre una terminal en la raíz del proyecto
3. Ejecuta:
   ```bash
   docker-compose up --build
   ```
4. Espera a que los servicios inicien (puede tardar unos minutos la primera vez)
5. Accede a la aplicación en: http://localhost (puerto 80)
6. La API estará disponible en: http://localhost:8000/api/v1

## Opción 2: Ejecutando backend y frontend por separado

### Backend (Python/FastAPI)

1. Navega a la carpeta backend:
   ```bash
   cd backend
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta el servidor:
   ```bash
   python run.py
   ```
   
5. El backend estará disponible en: http://localhost:8000

### Frontend (React)

1. En otra terminal, navega a la carpeta frontend:
   ```bash
   cd frontend
   ```

2. Instala las dependencias:
   ```bash
   npm install
   ```

3. Inicia el servidor de desarrollo:
   ```bash
   npm start
   ```

4. El frontend estará disponible en: http://localhost:3000

## Notas adicionales

- La API incluye documentación interactiva Swagger en: http://localhost:8000/docs
- Asegúrate de que los puertos 3000 y 8000 estén disponibles
- La base de datos SQLite se encuentra en: backend/app/db/inventario.db
