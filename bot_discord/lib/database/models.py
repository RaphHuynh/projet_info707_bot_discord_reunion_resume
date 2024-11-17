from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Table intermédiaire pour la relation Many-to-Many
user_resume = Table(
    'user_resume',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('resume_id', Integer, ForeignKey('resumes.id'))
)

message_resume = Table(
    'message_resume',
    Base.metadata,
    Column('message_id', Integer, ForeignKey('messages.id')),
    Column('resume_id', Integer, ForeignKey('resumes.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    id_discord = Column(String(200))


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(Text)


class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True)
    text_resume = Column(Text)
    text_complete = Column(Text)
    users = relationship("User", secondary=user_resume, back_populates="resumes")
    messages = relationship("Message", secondary=message_resume, back_populates="resumes")

# Ajout des relations inverses
User.resumes = relationship("Resume", secondary=user_resume, back_populates="users")
Message.resumes = relationship("Resume", secondary=message_resume, back_populates="messages")
