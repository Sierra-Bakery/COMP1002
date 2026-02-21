import numpy as np #numpy used for arrays as python doesn't have built in array support
temperatures = np.zeros(7)
#logic for array with temperature elements. To comply with assesment instructions the loop reassigns a new array everytime a new temp is added.
for i in range(7):
	temp = input("Input temperature: ")
	temperatures[i-1] = temp
print (temperatures)