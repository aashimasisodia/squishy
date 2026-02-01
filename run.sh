#!/bin/bash
cd backend
source venv/bin/activate
uvicorn server:app --reload

cd frontend
npm run dev