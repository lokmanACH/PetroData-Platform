import tempfile
from pathlib import Path

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import File

from pipeline import run_pipeline

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello FastAPI"}


@app.post("/pipeline")
async def run_it(file: UploadFile = File(...)):
    if not file.filename or Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(status_code=400, detail="Upload a CSV file")

    uploaded_path = None
    try:
        file_contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as uploaded_file:
            uploaded_file.write(file_contents)
            uploaded_path = Path(uploaded_file.name)

        output_name = f"{Path(file.filename).stem}_processed.csv"
        output_path = Path(__file__).resolve().parent / "data" / "processed" / output_name
        data, output_path = run_pipeline(uploaded_path, output_path)
        return {
            "message": "success",
            "csv_path": str(output_path),
            "data": data,
        }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        if uploaded_path and uploaded_path.exists():
            uploaded_path.unlink()