if __name__ == "__main__":
    import os
    import sys 
    cwd = os.getcwd()
    sys.path.append(cwd + '/..')  # for config module
    sys.path.append(cwd + '/../model')  # for config module
    sys.path.append(cwd + '/../utils')  # for config module


import requests
import json

from datetime import datetime

from models import *



'''
1. latest block number
curl "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=ITGMS3Z42MBB9AJ8CMFCTZYV38X8XFHVZ4"
{"jsonrpc":"2.0","id":83,"result":"0x8374ea"}


2. get transaction count by block number
curl "https://api.etherscan.io/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag=0x837512&apikey=ITGMS3Z42MBB9AJ8CMFCTZYV38X8XFHVZ4"
{"jsonrpc":"2.0","id":1,"result":"0x99"}


3. get transaction by block number, index
curl "https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag=0x10d4f&index=0x0&apikey=ITGMS3Z42MBB9AJ8CMFCTZYV38X8XFHVZ4"
{"jsonrpc":"2.0","id":1,"result":{"blockHash":"0x7eb7c23a5ac2f2d70aa1ba4e5c56d89de5ac993590e5f6e79c394e290d998ba8","blockNumber":"0x10d4f","from":"0x4458f86353b4740fe9e09071c23a7437640063c9","gas":"0x5208","gasPrice":"0xba43b7400","hash":"0xa442249820de6be754da81eafbd44a865773e4b23d7c0522d31fd03977823008","input":"0x","nonce":"0x1","to":"0xbf3403210f9802205f426759947a80a9fda71b1e","transactionIndex":"0x0","value":"0xaa9f075c200000","v":"0x1b","r":"0x2c2789c6704ba2606e200e1ba4fd17ba4f0e0f94abe32a12733708c3d3442616","s":"0x2946f47e3ece580b5b5ecb0f8c52604fa5f60aeb4103fc73adcbf6d620f9872b"}}


4. transaction list by address
curl "http://api.etherscan.io/api?module=account&action=txlist&address=0x440dF9458AdFF2eB2a924c8211e6a7dA4231346F&startblock=0&endblock=99999999&sort=asc&apikey=ITGMS3Z42MBB9AJ8CMFCTZYV38X8XFHVZ4"
{"status":"1","message":"OK","result":[{"blockNumber":"8604538","timeStamp":"1569229636","hash":"0x21d7b0a710a11355a31bf06395ce03846749b58b02ebe5f90f9cede6be781aa1","nonce":"51348","blockHash":"0x1987efe1182423e2958caa3cd2a2d96aa552cdbaabe80881aa0adc5511a823de","transactionIndex":"12","from":"0xe4b3dd9839ed1780351dc5412925cf05f07a1939","to":"0x440df9458adff2eb2a924c8211e6a7da4231346f","value":"1000000000000000000","gas":"50000","gasPrice":"25000000000","isError":"0","txreceipt_status":"1","input":"0x","contractAddress":"","cumulativeGasUsed":"486333","gasUsed":"21000","confirmations":"10591"}]}
'''

API_KEY = "ITGMS3Z42MBB9AJ8CMFCTZYV38X8XFHVZ4"

URL_BASE = "https://api.etherscan.io/api?"
URL_LATEST_BLOCK_NUMBER = URL_BASE + "module=proxy&action=eth_blockNumber&apikey=" + API_KEY
URL_TRANSACTION_COUNT = URL_BASE + "module=proxy&action=eth_getBlockTransactionCountByNumber&tag={0}&apikey=" + API_KEY
URL_TRANSACTION_BY_BLOCK_INDEX = URL_BASE + "module=proxy&action=eth_getTransactionByBlockNumberAndIndex&tag={0}&index=0x{1:x}&apikey=" + API_KEY
URL_ADDRESS_TRANSACTION = URL_BASE + "module=account&action=txlist&address={0}&startblock=0&endblock=99999999&sort=asc&apikey=" + API_KEY
URL_ADDRESS_TOKEN_TRANSACTION = URL_BASE + "module=account&action=tokentx&address={0}&startblock=5000000&endblock=999999999&sort=asc&apikey=" + API_KEY

def readFromServer(url):
    try:
        res = requests.get(url)
        return json.loads(res.text)
    except:
        return None


def getLatestBlock():
    res = readFromServer(URL_LATEST_BLOCK_NUMBER)

    return res["result"]


def getTransactionCount(block):
    res = readFromServer(URL_TRANSACTION_COUNT.format(block))

    return res["result"]


def getTransaction(block, index):
    res = readFromServer(URL_TRANSACTION_BY_BLOCK_INDEX.format(block, index))

    return res["result"]


def getTransactionList(address):
    res = readFromServer(URL_ADDRESS_TRANSACTION.format(address))

    return res["result"]


'''
"blockNumber":"5999708","timeStamp":"1532114373","hash":"0x9ab3b4c0897c2d032b74a5eafce39e6e399ada66802d467dbf15c56ded46e6ab","nonce":"9888","blockHash":"0x082298475c4b2abf7880a6e6e20511e1c8bcb8e5e3ecd1398901df40609733e4","from":"0xba826fec90cefdf6706858e5fbafcb27a290fbe0","contractAddress":"0xc5bbae50781be1669306b9e001eff57a2957b09d","to":"0x4aee792a88edda29932254099b9d1e06d537883f","value":"1819140188","tokenName":"Gifto","tokenSymbol":"GTO","tokenDecimal":"5","transactionIndex":"23","gas":"152387","gasPrice":"60000000000","gasUsed":"52387","cumulativeGasUsed":"1314990","input":"deprecated","confirmations":"2648498"}
'''
def getTokenTransactionList(address):
    res = readFromServer(URL_ADDRESS_TOKEN_TRANSACTION.format(address))

    return res["result"]




if __name__ == "__main__":
    # print(URL_LATEST_BLOCK_NUMBER)
    # print(URL_TRANSACTION_COUNT.format("0x12345"))
    # print(URL_TRANSACTION_BY_BLOCK_INDEX.format("0x123345", 0x23))
    # print(URL_ADDRESS_TRANSACTION.format("0x440dF9458AdFF2eB2a924c8211e6a7dA4231346F"))

    # Transaction.objects(txHash__ne=None).delete()
    # exit()

    block = getLatestBlock()
    print(block)

    count = getTransactionCount(block)
    print(count)
    if count:
        for i in range(0, int(count, 16)):
            # print(str(i) + ' -------->')
            trans = getTransaction(block, i)
            # print(res)

            list = getTokenTransactionList(trans["from"])
            if list:
                for e in list:
                    if e["value"] != '0':
                        try:
                            Transaction.objects(fromAddress = e["from"], toAddress = e["to"], txHash = e["hash"]).modify(
                                        upsert=True, new=True,
                                        userId = ObjectId("5d8c17c43402a409bd39f40c"),
                                        set__fromAddress = e["from"],
                                        set__fromCurrency = e["tokenSymbol"],
                                        set__toAddress = e["to"],
                                        set__toCurrency = e["tokenSymbol"],
                                        set__amount = float(e["value"])/(10**int(e["tokenDecimal"])),
                                        set__senderDeviceId = 0,
                                        set__transactedAt = datetime.utcfromtimestamp(int(e["timeStamp"])),
                                        set__score = 0,
                                        set__txHash = e["hash"],
                                        set__createdAt = datetime.utcnow)


                            print(e)
                            print("{0}:{1} -> {2}:{3} eth:{4}".format(e["hash"], e["from"], e["to"], float(e["value"])/(10**int(e["tokenDecimal"])), datetime.utcfromtimestamp(int(e["timeStamp"]))))
                        except:
                            print(e)

            list = getTransactionList(trans["from"])
            if list:
                for e in list:
                    if e["isError"] == '0' and e["value"] != '0':
                        try:
                            Transaction.objects(fromAddress = e["from"], toAddress = e["to"], txHash = e["hash"]).modify(
                                        upsert=True, new=True,
                                        userId = ObjectId("5d8c17c43402a409bd39f40c"),
                                        set__fromAddress = e["from"],
                                        set__fromCurrency = "ETH",
                                        set__toAddress = e["to"],
                                        set__toCurrency = "ETH",
                                        set__amount = float(e["value"])/(10**18),
                                        set__senderDeviceId = 0,
                                        set__transactedAt = datetime.utcfromtimestamp(int(e["timeStamp"])),
                                        set__score = 0,
                                        set__txHash = e["hash"],
                                        set__createdAt = datetime.utcnow)


                            print(e)
                            print("{0}:{1} -> {2}:{3} eth:{4}".format(e["hash"], e["from"], e["to"], float(e["value"])/(10**18), datetime.utcfromtimestamp(int(e["timeStamp"]))))
                        except:
                            print(e)
