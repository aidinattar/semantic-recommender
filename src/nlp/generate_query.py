import torch
import typer
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import warnings
warnings.simplefilter("ignore", category=FutureWarning)

app = typer.Typer(help="Generate embeddings for a text query and save them to disk.")

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OUTPUT_PATH = Path("embeddings/queries/query.csv")

@app.command()
def generate(
    query: str = typer.Option(
        ...,
        help="The text query to generate embeddings for.",
    ),
    model_name: str = typer.Option(
        default=DEFAULT_MODEL_NAME,
        help="The name of the SentenceTransformer model to use.",
    ),
    output_path: Path = typer.Option(
        default=Path(OUTPUT_PATH),
        help="The path to save the generated embeddings.",
    ),
):
    """
    Generate embeddings for a text query using a specified SentenceTransformer model.
    The generated embeddings are saved to a CSV file.

    Args:
        query (str): The text query to generate embeddings for.
        model_name (str): The name of the SentenceTransformer model to use.
        output_path (str): The path to save the generated embeddings.
    """
    typer.echo(f"Loading model {model_name}...")
    model = SentenceTransformer(model_name)
    
    typer.echo(f"Generating embeddings for query: {query}")
    embedding = model.encode([query], show_progress_bar=True, device="cuda" if torch.cuda.is_available() else "cpu")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(output_path, embedding, delimiter=",")
    typer.echo(f"Embeddings saved to {output_path}")

@app.command()
def new_command_name():
    pass

if __name__ == "__main__":
    app()