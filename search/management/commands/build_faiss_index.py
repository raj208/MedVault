# search/management/commands/build_faiss_index.py
from django.core.management.base import BaseCommand
from search.faiss_store import rebuild_index, load_index
from search.embedding import get_dim

class Command(BaseCommand):
    help = "Rebuild the FAISS index from active doctors in Postgres."

    def handle(self, *args, **options):
        dim = get_dim()
        self.stdout.write(self.style.NOTICE(f"Embedding dimension: {dim}"))
        index = rebuild_index()
        n = index.ntotal
        self.stdout.write(self.style.SUCCESS(f"FAISS index rebuilt. Vectors: {n}"))
