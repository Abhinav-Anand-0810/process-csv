# Process CSV Job

Google Cloud Run Jobs triggered by Cloud Function. It validates the menu item present in the `.csv` file and inserts them into existing restaurants, publishing the final results to Pub/Sub.

## Expected Item Details in CSV File

The CSV file must include at least these columns for each Menu Item:

- `restaurant_id`: ID of the restaurant.
- `name`: Name of the Menu Item.
- `rate`: Rate of the Item.
- `quantity`: Available Quantity of the Item.

## Project Structure

- `main.py`: Cloud Job entrypoint orchestrating validation, insertion, and results reporting.
- `settings.py`: Environment and application configuration.
- `enums.py`: Service-level enumerations and constants.
- `exceptions.py`: Custom exception classes for validation and processing failures.
- `schemas/dto.py`: Schemas used in the project.
- `utils/storage.py`: Utility file for Google Cloud Storage.
- `utils/pub_sub.py`: Utility file for Google Cloud Pub/Sub.
- `src/repository.py`: Repository for communication with DB.
- `src/service.py`: Service for the Business Logic.

## Local Setup & Deployment Prep

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment variables from the template

```bash
cp .env.template .env
```

#### Populate .env with the required configuration values

### 3. Update the Cloud Function on GCP

```bash
gcloud run jobs deploy process-csv --source . --region asia-south2 --env-vars-file=.env
```
