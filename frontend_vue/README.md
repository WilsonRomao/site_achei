# ACHEI — Frontend Vue

Single-page application built with Vue 3 and Vite. It uses Bootstrap for the
interface and Leaflet for the health-unit map.

## Run with Docker Compose

From the repository root:

```bash
docker compose up --build -d
```

The Vue development server is available at <http://localhost:3000> and uses the
Django API at <http://localhost:8000/api>.

## Run locally

```bash
npm ci
npm run dev
```

For local development outside Docker, set `VITE_API_URL` to the Django API base
URL, for example `http://localhost:8000/api`.

## Main components

- `src/App.vue`: application state and main screen composition.
- `src/components/Auth.vue`: registration and login.
- `src/components/Mapa.vue`: map populated from the Django establishments API.
- `src/components/MedicamentoList.vue`: paginated stock search.
- `src/components/AdminPanel.vue`: user and profile-request administration.
- `src/components/Upload.vue`: stock spreadsheet upload.
- `src/services/api.js`: Django REST API client.

The current Docker setup runs Vite in development mode. A production deployment
still needs a production frontend build and a static web server.
