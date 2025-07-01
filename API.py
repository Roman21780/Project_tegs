from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

from models import Client, Segment, Tag, AddTagsRequest

app = FastAPI()

# Временное хранилище данных (заменить на базу данных)
# Временные данные для тестирования
clients_db = [
    {"id": 1, "name": "Client A", "segments": [1], "tags": [1]},
    {"id": 2, "name": "Client B", "segments": [2], "tags": [2, 3]},
]

segments_db = [
    {"id": 1, "name": "Segment 1", "tags": [1]},
    {"id": 2, "name": "Segment 2", "tags": [2, 3]},
]

tags_db = [
    {"id": 1, "name": "Tag 1", "color": "#FF0000", "text": "Red tag", "emoji": "🔴"},
    {"id": 2, "name": "Tag 2", "color": "#00FF00", "text": "Green tag", "emoji": "🟢"},
    {"id": 3, "name": "Tag 3", "color": "#0000FF", "text": "Blue tag", "emoji": "🔵"},
]


@app.get("/clients")
async def get_clients(segment_id: Optional[int] = None, tag_id: Optional[int] = None):
    """
    Получить список клиентов с фильтрацией по сегментам и/или тегам.
    """
    filtered_clients = clients_db

    if segment_id:
        # Фильтрация по сегменту
        segment = next((s for s in segments_db if s['id'] == segment_id), None)
        if not segment:
            raise HTTPException(status_code=404, detail="Segment not found")
        filtered_clients = [c for c in filtered_clients if segment_id in c['segments']]

    if tag_id:
        # Фильтрация по тегу
        tag = next((t for t in tags_db if t['id'] == tag_id), None)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        filtered_clients = [c for c in filtered_clients if tag_id in c['tags']]

    return filtered_clients


@app.post("/segments/{segment_id}/add-tags")
async def add_tags_to_segment(segment_id: int, request: AddTagsRequest):
    """
    Добавление тегов к сегменту.
    """
    segment = next((s for s in segments_db if s['id'] == segment_id), None)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

    for tag_id in request.tag_ids:
        if tag_id not in segment['tags']:
            segment['tags'].append(tag_id)

    return {"message": "Tags added successfully"}


@app.post("/segments/{segment_id}/remove-tags")
async def remove_tags_from_segment(segment_id: int, request: AddTagsRequest):
    """
    Удаление тегов из сегмента.
    """
    segment = next((s for s in segments_db if s['id'] == segment_id), None)
    if not segment:
        raise HTTPException(status_code=404, detail="Segment not found")

    for tag_id in request.tag_ids:
        if tag_id in segment['tags']:
            segment['tags'].remove(tag_id)

    return {"message": "Tags removed successfully"}