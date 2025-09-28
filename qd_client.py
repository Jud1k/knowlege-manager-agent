import asyncio
from typing import Any, Dict, List
import uuid
from fastembed import TextEmbedding
from pydantic import BaseModel, Field
from qdrant_client.async_qdrant_client import AsyncQdrantClient
from qdrant_client.async_client_base import AsyncQdrantBase
from qdrant_client.models import VectorParams, Distance, PointStruct


class DocumentChunck(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SearchResult(BaseModel):
    id: str
    content: str
    score: float
    metadata: Dict[str, Any]


class CustomQdrantClient:
    def __init__(self, client: AsyncQdrantBase):
        self.client = client
        self.embedding_model = TextEmbedding()

    async def create_collection(self, collection_name: str):
        if not await self.client.collection_exists(collection_name):
            await self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

    async def add_document_chunks(
        self, chunks: List[DocumentChunck], collection_name: str = "documents"
    ):
        try:
            contents = [chunk.content for chunk in chunks]
            embeddings = list(self.embedding_model.embed(contents))

            points = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point_id = str(uuid.uuid4())

                point = PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={"content": chunk.content, "chunk_id": i, **chunk.metadata},
                )
                points.append(point)
            return await self.client.upsert(
                collection_name=collection_name, points=points
            )
        except Exception as e:
            pass


async def main():
    client = AsyncQdrantClient(location="http://localhost:6333/")
    qd_client = CustomQdrantClient(client=client)
    docs = [
        DocumentChunck(
            content="Для более глубокого контроля над поведением моделей рекомендуется использовать специализированные пакеты:",
            metadata={"source": "doc1"},
        ),
        DocumentChunck(
            content="Пришло время превратить теоретические знания в мощный практический инструментарий для создания по-настоящему умных AI-агентов!",
            metadata={"source": "doc2"},
        ),
    ]

    await qd_client.create_collection("documents")
    a = await qd_client.add_document_chunks(docs)
    print(a)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(e)
