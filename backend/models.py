from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field


class Record(SQLModel, table=True):
    """MVP用の記録メタデータモデル."""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    patient_name: str
    patient_id: Optional[str] = None
    visit_date: date

    markdown_path: str  # ローカルMarkdownファイルへのパス

    summary: Optional[str] = None  # AI要約や手入力要約
    tags: Optional[str] = None  # カンマ区切りタグ（簡易実装） 