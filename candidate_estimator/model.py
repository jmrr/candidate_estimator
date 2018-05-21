from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy import (
    Column, Boolean, DateTime, Text,
    Integer, Float, ForeignKey,
)

DBSession = scoped_session(sessionmaker())
Base = declarative_base()


def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


class SpeechToText(Base):
    __tablename__ = 'speech_to_text'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    time = Column(Float)
    duration = Column(Float)
    confidence = Column(Float)
    candidate_id = Column(Integer, ForeignKey('candidates.id'))


class Candidates(Base):
    __tablename__ = 'candidates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    applicationId = Column(Text)
    candidateId = Column(Integer)
    isRetake = Column(Boolean)
    invitationDate = Column(DateTime)
    applicationTime = Column(DateTime)
    speechToText = relationship(SpeechToText)
    videoLength = Column(Float)
    score = Column(Integer)
    predictedScore = Column(Integer)

    def serialize(self):
        return {
            'id': self.id,
            'applicationId': self.applicationId,
            'candidateId': self.candidateId,
            'isRetake': self.isRetake,
            'invitationDate': self.invitationDate.isoformat(),
            'applicationTime': self.applicationTime.isoformat(),
            'speechToText': [
                dict(
                    name=obj.name,
                    time=obj.time,
                    duration=obj.duration,
                    confidence=obj.confidence,
                )
                for obj in self.speechToText
            ],
            'videoLength': self.videoLength,
            'score': self.score,
        }

    @staticmethod
    def deserialize(candidate):
        return Candidates(
            applicationId=candidate['applicationId'],
            candidateId=candidate['candidateId'],
            isRetake=candidate['isRetake'],
            invitationDate=candidate['invitationDate'],
            applicationTime=candidate['applicationTime'],
            speechToText=[
                SpeechToText(
                    name=obj['name'],
                    time=obj['time'],
                    duration=obj['duration'],
                    confidence=obj['confidence'],
                )
                for obj in candidate['speechToText']
            ],
            videoLength=candidate['videoLength'],
            score=candidate['score'],
        )
