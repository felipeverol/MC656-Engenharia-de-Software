from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings  # <--- Importação nova

router = APIRouter(prefix="/email", tags=["Email"])

class EmailRequest(BaseModel):
    to: EmailStr
    subject: str
    html: str

# Usa as variáveis carregadas pelo Pydantic
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

@router.post("/send")
async def send_email(email_data: EmailRequest, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=email_data.subject,
        recipients=[email_data.to],
        body=email_data.html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return {"message": "Email enviado para a fila"}