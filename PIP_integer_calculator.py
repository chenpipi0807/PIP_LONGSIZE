import torch
import math

class PIP_IntegerCalculator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_number": ("INT", {
                    "default": 0,
                    "min": -2147483648,
                    "max": 2147483647,
                    "step": 1
                }),
                "coefficient": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1000000.0,
                    "step": 0.01
                }),
                "operation": (["加法", "减法", "乘法", "除法"],),
                "output_type": (["整数", "浮点数"],),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT")
    RETURN_NAMES = ("integer_result", "float_result")
    FUNCTION = "calculate"
    CATEGORY = "数学运算"

    def calculate(self, input_number, coefficient, operation, output_type):
        # 执行基本数学运算
        if operation == "加法":
            result = input_number + coefficient
        elif operation == "减法":
            result = input_number - coefficient
        elif operation == "乘法":
            result = input_number * coefficient
        elif operation == "除法":
            if coefficient == 0:
                print("警告: 除数不能为零，将使用默认值1.0")
                coefficient = 1.0
            result = input_number / coefficient
        
        # 根据输出类型返回结果
        if output_type == "整数":
            # 四舍五入取整
            integer_result = round(result)
            return (integer_result, float(result))
        else:
            # 保持浮点数
            return (int(result), result)
