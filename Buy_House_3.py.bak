Initial_Annual_Salery = float(input("Enter your annual Salery"))
Total_Cost=1000000
low=0
high=1
Semi_Annual_Range = 0.07
Portion_Downpayment = (0.25*Total_Cost)
Total_months = 0
Current_Savings =0
steps=0
Portion_Saved = 1
# checking the feasibility
Salery = Initial_Annual_Salery/12
while (Total_months < 36):
        Current_Savings += ((Portion_Saved*Salery)+Current_Savings*(0.04/12))
        Total_months +=1
        if(Total_months%6 == 0):
            Salery += Salery*Semi_Annual_Range
if Current_Savings > Portion_Downpayment :          
    Current_Savings =0
    while abs(Current_Savings - Portion_Downpayment) >= 100:
        Total_months=0
        Portion_Saved = (low+high)/2
        Current_Savings =0
        Salery = Initial_Annual_Salery/12
        while (Total_months < 36):
            Current_Savings += ((Portion_Saved*Salery)+Current_Savings*(0.04/12))
            Total_months +=1
            if(Total_months%6 == 0):
                Salery += Salery*Semi_Annual_Range
        if(Current_Savings > Portion_Downpayment):
            high = Portion_Saved
        if(Current_Savings < Portion_Downpayment):
            low = Portion_Saved
        steps+=1
    print("Best Savings Rate is",Portion_Saved)
    print("Steps in bisection search",steps)
else:
    print ("It is not possible to pay the down payment in three years. ")