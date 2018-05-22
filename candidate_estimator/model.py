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
    candidate_id = Column(Integer, ForeignKey('profile.id'))


class Profile(Base):
    __tablename__ = 'profile'

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
            'predictedScore': self.predictedScore,
        }

    @staticmethod
    def deserialize(profile):
        return Profile(
            applicationId=profile['applicationId'],
            candidateId=profile['candidateId'],
            isRetake=profile['isRetake'],
            invitationDate=profile['invitationDate'],
            applicationTime=profile['applicationTime'],
            speechToText=[
                SpeechToText(
                    name=obj['name'],
                    time=obj['time'],
                    duration=obj['duration'],
                    confidence=obj['confidence'],
                )
                for obj in profile['speechToText']
            ],
            videoLength=profile['videoLength'],
            score=profile['score'],
        )
