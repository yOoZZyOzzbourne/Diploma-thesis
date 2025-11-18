"""Database models and operations for IoT system"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class SensorReading(Base):
    """Sensor data storage"""
    __tablename__ = 'sensor_readings'

    id = Column(Integer, primary_key=True)
    sensor_id = Column(String(50))
    sensor_type = Column(String(50))
    value = Column(Float)
    unit = Column(String(20))
    timestamp = Column(DateTime, default=datetime.now)

class DeviceLog(Base):
    """Device control log"""
    __tablename__ = 'device_logs'

    id = Column(Integer, primary_key=True)
    device_id = Column(String(50))
    device_type = Column(String(50))
    action = Column(String(100))
    value = Column(String(100))
    timestamp = Column(DateTime, default=datetime.now)

class ParkingEvent(Base):
    """Parking lot events"""
    __tablename__ = 'parking_events'

    id = Column(Integer, primary_key=True)
    spot_id = Column(String(20))
    event_type = Column(String(20))  # 'occupied' or 'vacant'
    timestamp = Column(DateTime, default=datetime.now)
    duration = Column(Integer)  # minutes

# Create database
db_path = 'iot_system.db'
engine = create_engine(f'sqlite:///{db_path}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def log_sensor_reading(sensor_id, sensor_type, value, unit):
    """Log sensor data to database"""
    session = Session()
    reading = SensorReading(
        sensor_id=sensor_id,
        sensor_type=sensor_type,
        value=value,
        unit=unit
    )
    session.add(reading)
    session.commit()
    session.close()

def log_device_action(device_id, device_type, action, value):
    """Log device control action"""
    session = Session()
    log = DeviceLog(
        device_id=device_id,
        device_type=device_type,
        action=action,
        value=str(value)
    )
    session.add(log)
    session.commit()
    session.close()

def log_parking_event(spot_id, event_type, duration=0):
    """Log parking event"""
    session = Session()
    event = ParkingEvent(
        spot_id=spot_id,
        event_type=event_type,
        duration=duration
    )
    session.add(event)
    session.commit()
    session.close()

def get_recent_sensor_data(sensor_type=None, limit=100):
    """Get recent sensor readings"""
    session = Session()
    query = session.query(SensorReading)
    if sensor_type:
        query = query.filter_by(sensor_type=sensor_type)
    results = query.order_by(SensorReading.timestamp.desc()).limit(limit).all()
    session.close()
    return results

def get_device_logs(device_id=None, limit=50):
    """Get device control logs"""
    session = Session()
    query = session.query(DeviceLog)
    if device_id:
        query = query.filter_by(device_id=device_id)
    results = query.order_by(DeviceLog.timestamp.desc()).limit(limit).all()
    session.close()
    return results
