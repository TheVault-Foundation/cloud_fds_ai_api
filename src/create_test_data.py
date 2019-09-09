from bson import json_util

from log import Log
from models import *

def create():
    billing = BillingType(billingType = 'Monthly')
    billing.save()
    billing = BillingType(billingType = 'Metered')
    billing.save()

    device = DeviceType(deviceId = 1, deviceType='PC Wallet')
    device.save()
    device = DeviceType(deviceId = 2, deviceType='Web Browser')
    device.save()
    device = DeviceType(deviceId = 3, deviceType='iPhone App')
    device.save()
    device = DeviceType(deviceId = 4, deviceType='Android App')
    device.save()

    billing = BillingType.objects(billingType = 'Monthly')
    print(json_util.dumps(billing))

    user = User(
                username = 'testUser',
                password = 'testPassword',
                company = 'textCompany',
                email = 'jdk@thevault.foundation',
                contactNumber = '0123456789',
                address = 'test address',
                billingType = billing[0].id,
                # emailVerified = BooleanField(required=True, default=False),
                # roleType = StringField(required=True, default="User", regex=r'^(Admin|User)$'),
                # isActive = BooleanField(required=True, default=True),
                # lastSignin = DateTimeField(),
                # createdAt = DateTimeField(required=True, default = datetime.now),
                createdBy = 'Admin',
                # updatedAt = DateTimeField(),
                # updatedBy = StringField(max_length=100),
    )
    user.save()


    api = UserApi(
                userId = user.id,
                apiKey = 'asfsdfsadf',
                apiSecret = 'aaaaaaaaafffffffffff',
                # isActive = BooleanField(required=True, default=True),
                # createdAt = DateTimeField(required=True, default = datetime.now),
                createdBy = 'Admin',
                # updatedAt = DateTimeField(),
                # updatedBy = StringField(max_length=100),
    )
    api.save()



if __name__ == '__main__':
    create()