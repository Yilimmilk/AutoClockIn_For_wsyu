from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime

from database.database import Base, engine


class UserInfo(Base):
    # 数据库表名
    __tablename__ = 'user_info'

    student_id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False, default="")
    location = Column(String(255), nullable=False, default="湖北省武汉市")
    enable = Column(Boolean(), nullable=False, default=True)
    last_clockin = Column(DateTime(), nullable=False, default=datetime.now)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
