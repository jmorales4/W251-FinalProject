import object_storage

sl_storage = object_storage.get_client('SLOS431078-4:SL431078', 'c52b259c2ff5ece265e453b917e0dcf8100ecc2e05c4cbe01410e47a81edd1cc', datacenter='dal05')

print sl_storage.containers()

sl_storage['foo2'].create()
#
print sl_storage.containers()
#
print sl_storage['foo2'].properties
#
sl_storage['foo2']['bar.txt'].create()
#
sl_storage['foo2']['bar.txt'].send('my name is milad')
#
print sl_storage['foo2']['bar.txt'].read()
#
print sl_storage['foo2'].objects()
#
sl_storage['foo2']['bar.txt'].delete()
#
sl_storage['foo2'].delete()


# Now we read a local file and push it up to the Object Store

newSwiftObject = open("../tweetdata/tweets.Apr12-2318.txt", "r")

print('Now creating a new object')

sl_storage['foo2']['tweets.Apr12-2318.txt'].send(newSwiftObject)

#Now we will read the file from the object store and write it to local disk
#Prep a local file for writing

newLocalFile = open("test.txt", "w+b")

swiftObject = sl_storage['foo2']['tweets.Apr12-2318.txt'].read()

newLocalFile.write(swiftObject)

newLocalFile.close()

print('done')