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
        # 确保输入值不为None
        if input_number is None:
            print("警告: 输入数字为None，将使用默认值0")
            input_number = 0
            
        if coefficient is None:
            print("警告: 系数为None，将使用默认值1.0")
            coefficient = 1.0
        
        # 确保输入值是正确的数值类型
        input_number = int(input_number)
        coefficient = float(coefficient)
            
        # 执行基本数学运算
        if operation == "加法":
            result = input_number + coefficient
        elif operation == "减法":
            result = input_number - coefficient
        elif operation == "乘法":
            result = input_number * coefficient
        elif operation == "除法":
            if coefficient == 0 or coefficient is None:
                print("警告: 除数不能为零或None，将使用默认值1.0")
                coefficient = 1.0
            result = input_number / coefficient
        
        # 计算整数和浮点数结果
        integer_result = int(round(result))  # 确保整数结果是int类型
        float_result = float(result)         # 确保浮点结果是float类型
        
        # 根据输出类型返回结果
        return (integer_result, float_result)
