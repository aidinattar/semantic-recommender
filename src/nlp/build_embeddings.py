import os
import tqdm
import typer
import numpy as np
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer
from config import (
    PROCESSED_DATA_DIR,
    PROCESSED_FILE_NAME
)

app = typer.Typer(help="Build embeddings for the arXiv metadata dataset.")


# Default paths
INPUT_PATH = PROCESSED_DATA_DIR / PROCESSED_FILE_NAME
EMBEDDINGS_DIR = Path("embeddings")
VECTORS_PATH = EMBEDDINGS_DIR / "vectors.npy"
INDEX_PATH = EMBEDDINGS_DIR / "index.csv"


@app.command()
def build(
    model_name: typer.Option(
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="The name of the SentenceTransformer model to use.",
    ),
    batch_size: typer.Option(
        default=32,
        help="The batch size for embedding generation.",
    ),
    input_path: typer.Option(
        default=PROCESSED_DATA_DIR / PROCESSED_FILE_NAME,
        help="The path to the input file containing the text data.",
    ),
    max_length: typer.Option(
        default=512,
        help="The maximum length of the input text.",
    ),
):
    """
    Build embeddings for the arXiv metadata dataset and save them to disk.
    This function uses the SentenceTransformer model to generate embeddings
    for the text data in the input file. The embeddings are saved as a numpy
    array and the metadata is saved as a CSV file.
    The embeddings are generated in batches to optimize memory usage and
    processing time.
    The input file should contain a column named 'text' with the text data
    to be embedded. The output files will be saved in the 'embeddings' directory.

    Args:
        model_name (str): The name of the SentenceTransformer model to use.
        batch_size (int): The batch size for embedding generation.
        input_path (str): The path to the input file containing the text data.
        max_length (int): The maximum length of the input text.
    """
    typer.echo(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    df.dropna(subset=["title", "abstract"], inplace=True)
    df["text"] = df["title"] + ". " + df["abstract"]
    
    # Create the embeddings directory if it doesn't exist
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Loading model {model_name}...")
    model = SentenceTransformer(model_name)
    model.max_seq_length = max_length

    # Generate embeddings in batches
    embeddings = []
    for i in tqdm.tqdm(range(0, len(df), batch_size), desc="Generating embeddings"):
        batch = df.iloc[i : i + batch_size]
        texts = batch["text"].tolist()
        batch_embeddings = model.encode(texts, show_progress_bar=False)
        embeddings.append(batch_embeddings)
    embeddings = np.vstack(embeddings)

    np.save(VECTORS_PATH, embeddings)
    df[["id", "title", "categories", "update_date", "authors"]].to_csv(INDEX_PATH, index=False)

    typer.echo(
        f"Embeddings saved to {VECTORS_PATH} and metadata saved to {INDEX_PATH}."
    )
    # Clean up
    del df
    del model
    del embeddings

if __name__ == "__main__":
    app()