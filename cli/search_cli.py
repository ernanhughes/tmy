# File: cli/search_cli.py

import click
from db.search import search_transcripts_by_embedding
from utils.embedding import get_embedding

@click.command()
@click.argument("markdown_file", type=click.Path(exists=True))
@click.option("--top_k", default=10, help="Number of top results to return.")
def search(markdown_file, top_k):
    """
    Search stored transcripts for content relevant to a Markdown session file.
    """
    with open(markdown_file, "r") as f:
        session_text = f.read()

    embedding = get_embedding(session_text)
    if not embedding:
        click.echo("Failed to generate embedding for session text.")
        return

    results = search_transcripts_by_embedding(embedding, top_k=top_k)

    if not results:
        click.echo("No matches found.")
        return

    click.echo("\nTop Matches:\n")
    for i, result in enumerate(results, 1):
        video_id, start_time, text_segment, score = result
        click.echo(f"{i}. Video: {video_id} | Time: {start_time}")
        click.echo(f"   Score: {score:.2f}")
        click.echo(f"   Segment: {text_segment}\n")

if __name__ == "__main__":
    search()
