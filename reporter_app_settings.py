from pydantic import BaseModel


class ReporterAppSettings(BaseModel):
    title: str
    header: str
    caption: str
    query_input_label: str
    spinner_message: str
