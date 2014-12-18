import zmq

if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.connect("tcp://127.0.0.1:5555")

    while True:
        try:
            topic, clientId,monitorSourceName,sampleTime,msg = socket.recv_multipart()
            print("{0}:{1}:{2}:{3}:{4}".format(topic, clientId,monitorSourceName,sampleTime,msg))
        except Exception as ex:
            print(ex)
        