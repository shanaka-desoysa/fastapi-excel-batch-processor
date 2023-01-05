# Excel Batch Processor

This is a simple batch processing service that accepts an Excel file, reads it into a Pandas DataFrame, adds a new column to the DataFrame, and returns the modified DataFrame as an Excel file.

## Development

To develop the app, clone the repository and create a virtual environment:

```bash
git clone https://github.com/myuser/excel-batch-processor.git
cd excel-batch-processor
python -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the app using the ASGI server:

```bash
uvicorn app:app --reload
```

## Deployment

To deploy the app using Docker, build the image and start the container:

```bash
docker-compose build
docker-compose up
```
