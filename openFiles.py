import os
import threading
#import urllib.request
from queue import Queue
import glob
from parsePeople import PeopleParser



class Parsing(threading.Thread):

    def __init__(self, queue):
        """Инициализация потока"""
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Получаем url из очереди
            url = self.queue.get()
            # Скачиваем файл
            self.parsing_file(url)

            # Отправляем сигнал о том, что задача завершена
            self.queue.task_done()

    def parsing_file(self, url):
        """сканируем файл"""
        PeopleParser(url)


def main(urls):

    """Запускаем программу"""
    queue = Queue()

    # Запускаем поток и очередь
    # в 22 потока обрабатывает за 2.24 минуты
    # в 1 потока обрабатывает за 2.21 минуты
    for i in range(1):
        t = Parsing(queue)
        t.setDaemon(True)
        t.start()

    # Даем очереди нужные нам файлы
    for url in urls:
        queue.put(url)

    # Ждем завершения работы очереди
    queue.join()


if __name__ == "__main__":

    urls = []
    folder = 'РНКБ'
    folderTest = 'test'
    for filename in glob.glob('xml/'+folder+'/*.xml'):
        urls.append(filename)

    main(urls)
