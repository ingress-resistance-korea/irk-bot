from src.worker.worker import Worker

if '__main__' == __name__:
    print('Start...')
    print('Initialize Message Queue Listener')
    worker = Worker()
    worker.run()
