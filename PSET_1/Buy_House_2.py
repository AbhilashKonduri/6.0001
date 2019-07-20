Total_Cost= float(input("Enter total cost of the House"))
Portion_Saved = float(input("Enter in decimal the portion of your salery to be saved"))
Initial_Annual_Salery = float(input("Enter your annual Salery"))
Semi_Annual_Range = float(input("Enter your semi annual raise"))
Portion_Downpayment = (0.25*Total_Cost)
Current_Savings=0
Total_months = 0
Salery = Initial_Annual_Salery/12
while (Current_Savings <= Portion_Downpayment):
    Current_Savings += ((Portion_Saved*Salery)+Current_Savings*(0.04/12))
    Total_months +=1
    if Total_months%6 ==0:
        Salery += (Salery*Semi_Annual_Range)
print("Number of months =",Total_months)