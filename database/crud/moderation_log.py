from sqlalchemy.orm import Session
from database.models import ModerationLog

def create_log(db: Session, request_id, text: str, toxicity: float, label: str, action: str):
    log = ModerationLog(
        request_id=request_id,
        text=text,
        toxicity=toxicity,
        label=label,
        action=action
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_log_by_request_id(db, request_id):
    return db.query(ModerationLog).filter(
        ModerationLog.request_id == request_id
    ).first()