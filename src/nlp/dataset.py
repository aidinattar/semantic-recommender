import os
import time
import tqdm
import zipfile
import typer
import threading
from pathlib import Path
from config import (
    KAGGLE_DATASET,
    DATA_DIR,
    RAW_FILE_NAME,
    RAW_DATA_DIR,
    PROCESSED_FILE_NAME,
    PROCESSED_DATA_DIR,
)
ZIP_PATH = DATA_DIR / "arxiv.zip"

app = typer.Typer(help="Download and extract the arXiv metadata dataset from Kaggle.")


@app.command()
def download():
    """Download the arXiv metadata dataset from Kaggle."""
    def spinner(stop_event: threading.Event):
        """
        A generator that yields a spinner for the download process.
        
        Args:
            stop_event (threading.Event): An event to signal when to stop the spinner.
        """
        while not stop_event.is_set():
            for frame in "|/-\\":
                print(f"\r{frame} Downloading...", end="", flush=True)
                time.sleep(0.1)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    typer.echo("\nDownloading arXiv metadata dataset from Kaggle...")
    stop_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_event,))
    spinner_thread.start()
    exit_code = os.system(f"kaggle datasets download -d {KAGGLE_DATASET} -p {DATA_DIR}")
    stop_event.set()
    spinner_thread.join()

    if exit_code != 0:
        typer.echo("\n❌ Failed to download the dataset. Please check your Kaggle API credentials.", err=True)
        raise typer.Exit(code=1)

    typer.echo("\nDownload complete.")


@app.command()
def extract():
    """Extract the downloaded zip file."""
    if not ZIP_PATH.exists():
        typer.echo("\n❌ The zip file does not exist. Please download the dataset first.", err=True)
        raise typer.Exit(code=1)

    typer.echo("\nExtracting the zip file...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(DATA_DIR)

    typer.echo("\nExtraction complete.")
    # Optionally, remove the zip file after extraction
    # Uncomment the following line if you want to delete the zip file after extraction
    typer.echo(f"Removing {ZIP_PATH}...")
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()


@app.command()
def process():
    """Extract id, title, abstract, authors, categories and update_date and save it in csv and json format."""
    import json
    import csv

    json_file_path = RAW_DATA_DIR / RAW_FILE_NAME
    if not json_file_path.exists():
        typer.echo("\n❌ The JSON file does not exist. Please download and extract the dataset first.", err=True)
        raise typer.Exit(code=1)
    
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    typer.echo("\nProcessing the JSON file...")

    columns = [
        "id",
        "title",
        "abstract",
        "authors",
        "categories",
        "update_date",
    ]

    with open(RAW_DATA_DIR / RAW_FILE_NAME, "r") as json_file, open(
        PROCESSED_DATA_DIR / PROCESSED_FILE_NAME, "w", newline=""
    ) as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
        csv_writer.writeheader()
        iterator = tqdm.tqdm(
            json_file,
            total=sum(1 for _ in open(RAW_DATA_DIR / RAW_FILE_NAME, "r")),
            desc="Processing",
            unit="record",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {postfix}",
            ncols=125,
            ascii=True,
            colour="green",
            unit_scale=True,
            unit_divisor=1024,
        )
        for line in iterator:
            try:
                data = json.loads(line)
                title = data.get("title", "")
                abstract = data.get("abstract", "")
                authors = data.get("authors", [])
                categories = data.get("categories", "")
                update_date = data.get("update_date", "")
                id = data.get("id", "")

                if not title or not abstract:
                    continue

                record = {
                    "id": id,
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "categories": categories,
                    "update_date": update_date,
                }
                csv_writer.writerow(record)
                postfix = f"{categories}"[:30].ljust(30)
                iterator.set_postfix_str(postfix)
            except json.JSONDecodeError:
                continue

    typer.echo(f"\nProcessing complete. Saved file to {PROCESSED_DATA_DIR / PROCESSED_FILE_NAME}.")
    # Optionally, remove the JSON file after processing
    # Uncomment the following line if you want to delete the JSON file after processing
    # json_file_path.unlink()


@app.command()
def full():
    """Download and extract the arXiv metadata dataset from Kaggle.
    This command combines the download and extract commands."""
    download()
    extract()
    process()


if __name__ == "__main__":
    app()