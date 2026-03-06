def BaseToBase(x, y):
    print('success')

b10 = int(input("Please enter a BASE 10 Decimal: "))
convertor = int(input("Please enter which BASE to convert to: "))
if convertor > 2 and convertor < 16:
    BaseToBase(b10,convertor)
else:
    print("invalid conversion integer")