import time
import threading


class Snowflake:
    """
    雪花算法ID生成器
    结构: 1位符号位 + 41位时间戳 + 10位机器ID + 12位序列号
    """

    def __init__(self, worker_id=0, datacenter_id=0):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

        self.worker_id_bits = 5
        self.datacenter_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)
        self.sequence_bits = 12

        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits

        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        if self.worker_id > self.max_worker_id or self.worker_id < 0:
            raise ValueError(f'worker_id must be between 0 and {self.max_worker_id}')

        if self.datacenter_id > self.max_datacenter_id or self.datacenter_id < 0:
            raise ValueError(f'datacenter_id must be between 0 and {self.max_datacenter_id}')

    @staticmethod
    def _current_millis():
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp

    def generate_id(self):
        with self.lock:
            timestamp = self._current_millis()

            if timestamp < self.last_timestamp:
                raise Exception(
                    f'Clock moved backwards. Refusing to generate id for {self.last_timestamp - timestamp} milliseconds'
                )

            if self.last_timestamp == timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            snowflake_id = ((timestamp - 1288834974657) << self.timestamp_shift) | \
                           (self.datacenter_id << self.datacenter_id_shift) | \
                           (self.worker_id << self.worker_id_shift) | self.sequence

            return str(snowflake_id)


# 全局单例
_snowflake = Snowflake(worker_id=1, datacenter_id=1)


def generate_snowflake_id():
    """生成雪花算法ID"""
    return _snowflake.generate_id()
