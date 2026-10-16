#!/usr/bin/env bash

source .venv/Scripts/activate

uvicorn backend.app.main:app --reload &
cd frontend
npm run dev