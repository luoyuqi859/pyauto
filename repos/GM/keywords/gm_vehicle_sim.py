import json
import socket
import threading
import time
import traceback
from queue import Queue

from utils.log import logger
from loguru import logger


class GMVehicleSim:

    def __init__(self, server_address=None):
        if not server_address:
            server_address = ('localhost', 55555)
        self._server_address = server_address

        self._tx_queue = None
        self._rx_queue = None
        self._shutdown = threading.Event()
        self._connection = None
        self._connected = False
        self._threads = []

    def get_connection(self):
        try:
            self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._connection.connect(self._server_address)
        except Exception as ex:
            logger.warning(ex)

        return self._connection

    def open(self):
        logger.info('connecting with: ' + str(self._server_address))
        self._tx_queue = Queue()
        self._rx_queue = Queue()

        # self.get_connection()

        try:
            self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self._connection.connect(self._server_address)
        except Exception as ex:
            logger.warning(ex)

        self._connected = True
        self._threads = []  # reset?
        self._threads.append(threading.Thread(target=self._tx_handler, args=[]))
        self._threads.append(threading.Thread(target=self._rx_handler, args=[]))

        for thread in self._threads:
            thread.start()

    def close(self):
        self._shutdown.set()
        self._connection.shutdown(socket.SHUT_WR)
        self._connection.close()

        self._tx_queue = None
        self._rx_queue = None

        self._connection = None
        self._connected = False

    def send(self, payload):
        """
        Adds to Tx Queue
        Args:
            signals: Arrary of signals.
        Returns:
            Return True or False if connected
        """
        # with self._tx_queue.mutex:
        if self._tx_queue is not None:
            if len(payload) > 0:
                # Important not know number, but if send to many errors on json parsing...
                chunks = self._divide_chunks(payload, 100)
                for chunk in chunks:
                    self._tx_queue.put(chunk)
        else:
            pass
        return self._connected

    def receive(self):
        """
        Pulls from Rx Queu
        Returns:
            Return signal list, else None
        """
        result = None
        if self._rx_queue is not None and not self._rx_queue.empty():
            # with self._rx_queue.mutex:
            result = self._rx_queue.get(False)  # no wait
            self._rx_queue.task_done()
        return result

    def _tx_handler(self):
        while not self._shutdown.is_set():
            if self._tx_queue is not None and not self._tx_queue.empty() and self._connection is not None:
                item = None
                # with self._tx_queue.mutex:
                item = self._tx_queue.get()
                self._tx_queue.task_done()

                length = self._tx_queue.qsize()
                logger.debug("Tx Queue: " + str(length))

                if item:
                    try:
                        tx_buffer = json.dumps(item, indent=0).encode()
                        if tx_buffer:
                            payload = tx_buffer
                            try:
                                self._connection.sendall(payload)
                            except socket.error:
                                self._connected = False
                                break
                    except Exception as ex:
                        if self._shutdown.is_set():
                            break
                        logger.error(traceback.format_exc())
                        logger.error(ex)  # Todo: handle better
                    finally:
                        pass  # tx_queue.task_done()
            else:
                time.sleep(0.05)  # not completely lock up system!

    def _rx_handler(self):
        rx_buffer = bytearray()  # buffer until can parse full list
        while not self._shutdown.is_set():
            try:
                if self._connection is not None:
                    recv_peek = 0
                    try:
                        recv_peek = len(self._connection.recv(1, socket.MSG_PEEK))
                    except socket.error:
                        self._connected = False

                    if recv_peek > 0:  # check if have data yet
                        try:
                            rx_buffer_temp = self._connection.recv(512000)  # ~512kKB (matches server RX as well)
                        except socket.error:
                            self._connected = False
                            continue

                        for buff in rx_buffer_temp:  # append to buffer
                            rx_buffer.append(buff)

                        # decode "list" message(s) at a time
                        try:
                            rx_buffer_temp = rx_buffer.decode()
                        except:
                            continue  # need more data cannot decode

                        # parse signals array
                        start = '['
                        end = ']'
                        start_index = rx_buffer_temp.find(start)
                        end_index = rx_buffer_temp.find(end)

                        if start_index < 0 or end_index < 0:
                            # if for whatever reason buffer data is missed and goes whacky (should not happen)
                            # happens under bad disconnect (un-plug USB) with partial data stream
                            if end_index < start_index:
                                rx_buffer = rx_buffer[:end_index]
                            continue

                        data = rx_buffer_temp[start_index:end_index + 1]
                        rx_buffer = rx_buffer[:rx_buffer_temp.find(start)] + rx_buffer[rx_buffer_temp.find(end) + 1:]

                        payload = json.loads(data)
                        if self._rx_queue is not None:
                            self._rx_queue.put(payload)

                            length = self._rx_queue.qsize()
                            logger.debug("Rx Queue: " + str(length))
                    else:
                        time.sleep(0.05)  # not completely lock up system!
                else:
                    time.sleep(0.125)  # not completely lock up system!
            except Exception as ex:
                if self._shutdown.is_set():
                    break
                logger.error(traceback.format_exc())
                logger.error(ex)  # Todo: handle better
            finally:
                pass

    def _divide_chunks(self, l, n):
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]


class GMSignal():

    def sendSignal(self, Signal=None, Value=None, Type='Signal', Mode='HS', times=1):
        """
        方式一（发一个信号）：
        :param Signal: 信号名称，如：TeenDrvFtrAvl
        :param Value: 信号值，如：“1”
        方式二（发多个信号）：
        :param Signal: 信号的字典{“信号名称”：“信号值”，“信号名称2”：”信号值2“......},
                       如：{”TeenDrvFtrAvl“：”1“，”AirQltySnsCstStAvl“：”0“}
        :param Value: None
        """
        _gmVehicleSim = GMVehicleSim()
        payload_Tx = []
        if isinstance(Signal, dict):
            for i in Signal:
                entry = {'Type': Type, 'Mode': Mode, 'Name': i, 'Value': str(Signal[i])}
                payload_Tx.append(entry)
        # entry = can.Message(arbitration_id=0x4C1, data=[0x01, 0x02, 0x03, 0x04, 0x05, 0x06], dlc=0x8, extended_id=False)
        else:
            entry = {'Type': Type, 'Mode': Mode, 'Name': Signal, 'Value': str(Value)}
            payload_Tx.append(entry)
        _gmVehicleSim.open()

        try:
            for _ in range(int(times)):
                _gmVehicleSim.send(payload_Tx)
                # _gmVehicleSim.send_msg(  payload_Tx) # send
                time.sleep(0.15)  # do not want to kill CPU, so play nice, but also go FAST...
                _gmVehicleSim.close()
        except Exception as ex:
            logger.error(ex)
            _gmVehicleSim.close()


GMS = GMSignal()
