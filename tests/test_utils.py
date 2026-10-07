import pytest
from utils import check_watering_condition

# 1. ทดสอบกรณีปกติ (Normal Case)
def test_normal_watering_needed():
    # ความชื้น 30%, เกณฑ์ 40%, โหมด Auto -> ต้องเปิดปั๊ม (True)
    assert check_watering_condition(current_moisture=30.0, threshold=40.0, auto_mode=True) == True

def test_normal_no_watering_needed():
    # ความชื้น 50%, เกณฑ์ 40%, โหมด Auto -> ไม่ต้องเปิดปั๊ม (False)
    assert check_watering_condition(current_moisture=50.0, threshold=40.0, auto_mode=True) == False

def test_manual_mode_prevents_auto_water():
    # ความชื้น 30%, เกณฑ์ 40%, แต่ปิด Auto Mode -> ระบบต้องไม่สั่งรดน้ำเอง (False)
    assert check_watering_condition(current_moisture=30.0, threshold=40.0, auto_mode=False) == False

# 2. ทดสอบกรณีขอบเขต (Boundary Case)
def test_boundary_moisture_equals_threshold():
    # ความชื้นเท่ากับเกณฑ์พอดี (40%) -> ไม่เปิดปั๊ม (เพราะต้องน้อยกว่าถึงจะเปิด)
    assert check_watering_condition(current_moisture=40.0, threshold=40.0, auto_mode=True) == False

# 3. ทดสอบกรณีข้อมูลผิดปกติ (Invalid Case)
def test_invalid_negative_moisture():
    # เซนเซอร์เพี้ยน ส่งค่าติดลบ -> ระบบต้องฟ้อง Error (ValueError)
    with pytest.raises(ValueError):
        check_watering_condition(current_moisture=-5.0, threshold=40.0, auto_mode=True)

def test_invalid_over_hundred_moisture():
    # เซนเซอร์เพี้ยน ส่งค่าเกิน 100% -> ระบบต้องฟ้อง Error (ValueError)
    with pytest.raises(ValueError):
        check_watering_condition(current_moisture=150.0, threshold=40.0, auto_mode=True)