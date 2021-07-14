import numpy as np
import pandas as pd
########################################################################
#### enter the three positions of the upper triangle of the diamond
##GaAs
# tip = [[-0.397,7.5E-4],[-0.3795,5E-4],[-0.3535,7.5E-4]]
# zero_Vdc = [-0.422,-0.396,-0.3785, -0.352] ## 4 point for 3 trianges

##Bilayer
# tip = [[4.68079332, 2.8*1e-3],[4.74843424,1.8*1e-3],[4.79352818,1.2*1e-3],[4.83862213,1.6*1e-3],[4.88121086,1.2*1e-3]]
# zero_Vdc = [4.6256785, 4.71085595, 4.77098121, 4.8085595, 4.85615866, 4.89624217] ## 6 point for 5 trianges

##Trilayer
# tip = [[2.64133612,2e-3],[2.6914405,1.6e-3],[2.73653445,1.6e-3], [2.78914405,2e-3]]
# zero_Vdc = [2.60375783,2.65887265,2.7039666, 2.74906054, 2.80417537] ## 4 point for 3 trianges
tip = [[2.66889353,1.72e-3],[2.70647182,1.28e-3], [2.73903967,1.28e-3],[2.77661795,1.62e-3]]
zero_Vdc = [2.63632568,2.68141962,2.71649269, 2.74906054, 2.79164927] ## 4 point for 3 trianges

#### record the good diamonds for capacitance calculation
cap_cal = [1,2]
########################################################################

lever_arm, E_add, Capacitance, Cg = [],[],[],[]
e = 1.6021766210e-19
for i in range(len(zero_Vdc)-1):
    delta_Vsd = tip[i][1]
    delta_Vg = zero_Vdc[i+1]-zero_Vdc[i]
    capacitance = e/tip[i][1]
    lever_arm.append(delta_Vsd/delta_Vg)
    E_add.append(delta_Vg*(delta_Vsd/delta_Vg))
    # Capacitance.append(capacitance * 1e18) add this one if you want all the cap(which is wrong!)

    ####Capacitance calculation selection
    if i in cap_cal:
        Capacitance.append(capacitance*1e18)
    else:
        Capacitance.append("N/A")

Cap = Capacitance  ## remember the original list
Cap = [index for index in Cap if index != "N/A"]  ## delete the "N/A"

for j in range(len(zero_Vdc)-1):
    Cg.append(lever_arm[j]*np.mean(Cap))

data = np.hstack((
                  np.reshape((np.append(E_add,["N/A","N/A"])),(-1,1))
                , np.reshape(np.append(lever_arm,[np.mean(lever_arm),np.std(lever_arm)]),(-1,1))
                , np.reshape(np.append(Capacitance,[np.mean(Cap),np.std(Cap)]),(-1,1))
                , np.reshape(np.append(Cg,[np.mean(Cg),np.std(Cg)]),(-1,1))
                  )
                )

pd.set_option('display.max_columns', None)

#### Remember to change the # of index names
df = pd.DataFrame(data=data, index=["n","n+1","n+2","n+3","Mean","Std"],
                  columns=["E_addition","Lever arm a","Total C","Cg"])

print(df)
#### save or not save ...
df.to_csv(r'C:\Users\andrew\Desktop\Thesis\Trilayer.csv')