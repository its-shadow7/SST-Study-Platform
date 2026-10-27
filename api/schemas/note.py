import re
from typing import List, Optional, Literal, Union, Dict, Any
from pydantic import BaseModel, Field, model_validator


def extract_term_number(term: str) -> int:
    """Helper to extract integer term number from string like 'Term 5' or 'term-3'."""
    if not term:
        return 1
    match = re.search(r'(\d+)', str(term))
    return int(match.group(1)) if match else 1


class NoteSection(BaseModel):
    section_id: str = Field(..., description="Unique slug for section within the note")
    heading: str = Field(..., description="Section title")
    body: str = Field(..., description="Markdown and LaTeX formatted body content")
    citations: List[str] = Field(default_factory=list, description="Academic citations and references")


class QuizOption(BaseModel):
    id: str = Field(..., description="Option identifier e.g. 'A', 'B', 'C'")
    text: str = Field(..., description="Option text")


class QuizQuestion(BaseModel):
    question_id: str = Field(..., description="Unique question identifier")
    question: str = Field(..., description="Question prompt text with LaTeX math support")
    options: List[QuizOption] = Field(default_factory=list, description="List of options")
    correct_answer: List[str] = Field(default_factory=list, description="List of correct option IDs")
    explanation: str = Field("", description="Detailed explanation for the solution")
    multi_select: bool = Field(False, description="Whether multiple options can be selected")


class NoteDocument(BaseModel):
    schema_version: int = Field(1, description="Schema version number")
    note_id: str = Field(..., pattern=r'^[a-z0-9-]+$', description="Kebab-case unique note identifier")
    term: str = Field(..., description="Curriculum term label e.g. 'Term 5'")
    term_number: int = Field(0, description="Integer term number e.g. 5")
    subject_code: str = Field(..., description="Course code e.g. 'CML', 'CN'")
    topic_title: str = Field(..., description="Full lecture title")
    tags: List[str] = Field(default_factory=list, description="Searchable tags")
    learning_objectives: List[str] = Field(default_factory=list, description="Key learning objectives")
    summary: str = Field(..., description="Short introductory summary")
    key_takeaways: List[str] = Field(default_factory=list, description="Bullet takeaways")
    sections: List[NoteSection] = Field(default_factory=list, description="Lecture sections")
    quiz: Optional[Union[Dict[str, Any], List[Any]]] = Field(default=None, description="Interactive comprehension quiz questions or object")
    last_updated: str = Field(..., description="ISO 8601 update timestamp")
    approval_status: Literal["draft", "approved"] = Field("approved", description="Publication status")

    @model_validator(mode="before")
    @classmethod
    def populate_term_number(cls, data):
        if isinstance(data, dict):
            term = data.get("term", "")
            term_num = data.get("term_number")
            if not term_num or term_num == 0:
                data["term_number"] = extract_term_number(term)
        return data


class NoteIndexItem(BaseModel):
    schema_version: int = Field(1, description="Schema version number")
    note_id: str = Field(..., description="Unique note identifier")
    term: str = Field(..., description="Term label")
    term_number: int = Field(1, description="Integer term number")
    subject_code: str = Field(..., description="Course code")
    topic_title: str = Field(..., description="Lecture title")
    tags: List[str] = Field(default_factory=list)
    learning_objectives: List[str] = Field(default_factory=list)
    summary: str = Field("")
    key_takeaways: List[str] = Field(default_factory=list)
    last_updated: str = Field(..., description="ISO 8601 update timestamp")
    approval_status: Literal["draft", "approved"] = Field("approved")

    @model_validator(mode="before")
    @classmethod
    def populate_term_number(cls, data):
        if isinstance(data, dict):
            term = data.get("term", "")
            term_num = data.get("term_number")
            if not term_num or term_num == 0:
                data["term_number"] = extract_term_number(term)
        return data


class NoteUpsertRequest(BaseModel):
    schema_version: int = Field(1, description="Schema version")
    note_id: str = Field(..., pattern=r'^[a-z0-9-]+$', description="Kebab-case note ID")
    term: str = Field(..., description="Term label e.g. 'Term 5'")
    term_number: Optional[int] = Field(None, description="Integer term number")
    subject_code: str = Field(..., description="Subject code e.g. 'CML'")
    topic_title: str = Field(..., description="Topic title")
    tags: List[str] = Field(default_factory=list)
    learning_objectives: List[str] = Field(default_factory=list)
    summary: str = Field(..., description="Summary")
    key_takeaways: List[str] = Field(default_factory=list)
    sections: List[NoteSection] = Field(default_factory=list)
    quiz: Optional[Union[Dict[str, Any], List[Any]]] = Field(default=None)
    approval_status: Literal["draft", "approved"] = Field("approved")
    last_updated: Optional[str] = Field(None, description="Optional ISO timestamp")

    @model_validator(mode="before")
    @classmethod
    def populate_term_number(cls, data):
        if isinstance(data, dict):
            term = data.get("term", "")
            term_num = data.get("term_number")
            if not term_num or term_num == 0:
                data["term_number"] = extract_term_number(term)
        return data
