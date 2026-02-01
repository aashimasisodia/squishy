# Text-to-Physics Simulation Platform

A web-based platform that generates physics simulations from natural language prompts using PyElastica.

## Project Structure

- `frontend/`: React + Vite + TypeScript application
- `backend/`: FastAPI Python backend
- `vercel.json`: Vercel deployment configuration

## Local Development

### 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```
OPENAI_API_KEY=your_api_key_here
```

Run the backend server:
```bash
uvicorn server:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Frontend Setup

Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
The application will be available at `http://localhost:5173`.

## Vercel Deployment

This project is configured for seamless deployment on Vercel as a monorepo.

### Prerequisites
- A Vercel account
- Your OpenAI API Key

### Deployment Steps

1. **Push to GitHub/GitLab/Bitbucket**: Ensure your code is pushed to a remote repository.

2. **Import Project in Vercel**:
   - Go to your Vercel Dashboard.
   - Click "Add New..." -> "Project".
   - Select your repository.

3. **Configure Project**:
   - **Framework Preset**: Vercel should automatically detect "Vite" or "Other". If not, select "Vite".
   - **Root Directory**: Leave as `./` (the root of the repo).
   - **Build & Output Settings**: The `vercel.json` file handles this automatically.

4. **Environment Variables**:
   - Expand the "Environment Variables" section.
   - Add `OPENAI_API_KEY` with your actual API key.
   - (Optional) `VERCEL=1` is automatically set by the platform, enabling the app to switch to ephemeral `/tmp` storage for simulations.

5. **Deploy**:
   - Click "Deploy".
   - Vercel will build the frontend and set up the Python serverless functions.

### Troubleshooting Vercel Deployment

- **404 Errors on API**: Ensure `vercel.json` rewrites are correctly pointing `/api/(.*)` to `backend/server.py`.
- **Server Errors (500)**: Check Vercel Function logs. Common issues might be missing dependencies in `backend/requirements.txt` or execution timeouts (simulations are computationally intensive).
