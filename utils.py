import random

def check_watering_condition(current_moisture: float, threshold: float, auto_mode: bool) -> bool:
    """
    ตรวจสอบเงื่อนไขความปลอดภัยและตัดสินใจว่าต้องรดน้ำหรือไม่
    """
    # 1. ตรวจสอบค่าผิดปกติ (Invalid Case)
    if current_moisture < 0 or threshold < 0:
        raise ValueError("ค่าความชื้นและเกณฑ์ไม่สามารถติดลบได้")
    if current_moisture > 100 or threshold > 100:
        raise ValueError("ค่าความชื้นและเกณฑ์ไม่สามารถเกิน 100% ได้")
        
    # 2. ตรวจสอบเงื่อนไขการรดน้ำอัตโนมัติ (Normal/Boundary Case)
    if auto_mode and current_moisture < threshold:
        return True
        
    return False

def get_new_moisture(current_moisture: float, pump_on: bool) -> float:
    """
    คำนวณค่าความชื้นใหม่หลังเวลาผ่านไป
    """
    if pump_on:
        new_moisture = current_moisture + random.uniform(5.0, 10.0)
        return min(new_moisture, 90.0) # ล็อกไม่เกิน 90%
    else:
        new_moisture = current_moisture - random.uniform(3.8, 5.7)
        return max(new_moisture, 10.0) # ล็อกไม่ให้ต่ำกว่า 10%