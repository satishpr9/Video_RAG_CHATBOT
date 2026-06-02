This repository  contains a video retrieval-augmented generation (RAG) chatbot.

Backend:- FastAPI
Frontend:- React + VITE 

Setup for backend:-
  1. open a termina in `backend/`
  2. create and activate a python virual environment
       python -m venv .venv
       .venv\Scripts\Activate.ps1
  3. Install Dependencies:
      pip install -r requirement.txt
  4. Run the Backend Server:
     uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
  5 The API will be available at `http://localhost:8000`.
  

Setup for Fronted:-
  1. Open a terminal in `frontend/`
  2. Install npm dependencies:
      npm install
4. Run the frontend dev server:
       npm run dev

The app will typically be available at `http://localhost:5173`.
