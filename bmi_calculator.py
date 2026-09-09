print("======== BMI CALCULATOR ========")

# 1. User se input lena
weight = float(input("Apna weight kg me daalo: "))
height = float(input("Apni height meter me daalo: ")) 
# Example: 5 feet 6 inch = 1.67 meter

# 2. BMI Formula: weight / (height * height)
bmi = weight / (height * height)

# 3. Result ko 2 decimal tak round karna
bmi = round(bmi, 2)

print("\nTumhara BMI hai:", bmi)

# 4. Category check karna
if bmi < 18.5:
    print("Category: Underweight - Thoda weight badhao")
elif bmi >= 18.5 and bmi < 24.9:
    print("Category: Normal - Bilkul fit ho 💪")
elif bmi >= 25 and bmi < 29.9:
    print("Category: Overweight - Thoda dhyan do")
else:
    print("Category: Obese - Doctor se salah lo")