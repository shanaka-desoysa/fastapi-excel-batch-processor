import io
import tempfile

from fastapi import FastAPI, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI()


def predict(feature_1, feature_2, feature_3):
    # Simple model: predict 1 if feature_1 + feature_2 + feature_3 > 3, else predict 0
    return 1 if feature_1 + feature_2 + feature_3 > 3 else 0


@app.post("/predict_batch/")
async def predict_batch(file: bytes = File(...)):
    """
    Expects an excel file with columns: feature_1, feature_2, feature_3.
    <a href="/static/example_input.xlsx">Example Input</a>.<br>
    Returns a modified excel file with columns: feature_1, feature_2, feature_3, prediction
    <a href="/static/example_output.xlsx">Example Output</a>
    """
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(io.BytesIO(file))

    # Make predictions using the predict function and the apply method
    df['prediction'] = df[['feature_1', 'feature_2', 'feature_3']].apply(
        lambda row: predict(row['feature_1'], row['feature_2'], row['feature_3']), axis=1)

    # Write the modified DataFrame to a temporary file and return it as an Excel file response
    stream = io.BytesIO()
    df.to_excel(stream, index=False)
    stream.seek(0)
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".xlsx", delete=False) as FOUT:
        FOUT.write(stream.read())
        return FileResponse(
            FOUT.name,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=predictions.xlsx",
                "Access-Control-Expose-Headers": "Content-Disposition",
            }
        )
