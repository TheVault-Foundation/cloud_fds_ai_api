import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv('../datafiles/creditcard.csv')
df.head()

NORM_FILE='./datafiles/creditcard_norm.csv'
df_norm.to_csv(NORM_FILE, index=False, header=False)


# split normalized data by label
df_norm_fraud=df_norm[ df_norm.Class==1.0] #fraud
df_norm_nonfraud=df_norm[ df_norm.Class==0.0] #non_fraud

# split non_fraudfor 60%,20%,20% (training,validation,test)
df_norm_nonfraud_train,df_norm_nonfraud_validate,df_norm_nonfraud_test = \
    np.split(df_norm_nonfraud,[int(.6*len(df_norm_nonfraud)),int(.8*len(df_norm_nonfraud))])
# split fraud data to 50%,50% (validation and test)
df_norm_fraud_validate,df_norm_fraud_test = \
    np.split(df_norm_fraud,[int(0.5*len(df_norm_fraud))])
print('number of non fraud training, test, validation dataset = ',\
len(df_norm_nonfraud_train),\
len(df_norm_nonfraud_test),\
len(df_norm_nonfraud_validate))
      
print('number of fraud test,fraud validation dataset =',\
len(df_norm_fraud_test),\
len(df_norm_fraud_validate))

#create train,validate and test dataset with shuffle
df_train = df_norm_nonfraud_train.sample(frac=1) 
df_validate = df_norm_nonfraud_validate.append(df_norm_fraud_validate).sample(frac=1)
df_test = df_norm_nonfraud_test.append(df_norm_fraud_test).sample(frac=1)

print 'size of train,validate,test data =',len(df_train),len(df_validate),len(df_test)

#
## Training data set
#
df_train.head()

#
## Test data set
#
df_test.head()


#
## Validate data set
#
df_validate.head()

len(df_validate[df_validate.Class==1])


TRAIN_FILE='../IpToCountry/creditcard_training.csv'
TEST_FILE='../IpToCountry/creditcard_tesring.csv'
VALIDATE_FILE='../IpToCountry/creditcard_validation.csv'

df_train.to_csv(TRAIN_FILE, index=False, header=False)
df_validate.to_csv(VALIDATE_FILE,index=False,header=False)
df_test.to_csv(TEST_FILE,index=False,header=False)