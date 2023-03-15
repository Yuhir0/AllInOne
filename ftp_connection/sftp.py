import logging
from typing import Type

import pysftp as pysftp

logger = logging.getLogger(__name__)


class SftpConnectionClosed(Exception):
    pass


class SftpConfig:
    URI: str
    USER: str
    PASSWORD: str


def _load_host_key(config):
    cnopts = pysftp.CnOpts()
    if cnopts.hostkeys.lookup(config.URI) is None:
        logger.info("New host - will accept any host key")
        hostkeys = cnopts.hostkeys
        cnopts.hostkeys = None
        with pysftp.Connection(config.URI, config.USER, password=config.PASSWORD,
                               cnopts=cnopts) as sftp:
            logger.info("Connected to new host, caching its hostkey")
            hostkeys.add(
                config.URI, sftp.remote_server_key.get_name(), sftp.remote_server_key)
            hostkeys.save(pysftp.helpers.known_hosts())


class Sftp:
    """
    Class wraps a pysftp.Connection
    If is instantiated from different parts, the connection only will be closed by the last
    instance that call the method 'close' or if the method 'close_all' is called too.

    To use the connection you need to call the property 'connection'
        sftp = Sftp(SftpConfig)
        sftp.connection.put(...)
        sftp.close()

    You may use the 'with' statement. This returns the pysftp.Connection. The connection
    and the instance will be closed on exit the 'with'
        with Sftp(SftpConfig) as sftp:
            sftp.put(...)
    """
    __connection = None
    __instances_per_config = dict()
    __connections_per_config = dict()

    def __init__(self, config: Type[SftpConfig]) -> None:
        logger.info('Init sftp')
        self.__active = True
        self.config = config
        if self.config not in self.__class__.__instances_per_config:
            self.__class__.__instances_per_config[self.config] = []
        self.__class__.__instances_per_config[self.config].append(self)
        self.__class__.__connections_per_config[self.config] = \
            self.__class__.__connections_per_config.get(self.config, 0) + 1

    def __connect(self):
        logger.info('connect')
        logger.info(f"config => {self.config.URI}, {self.config.USER}")
        _load_host_key(self.config)
        cnopts = pysftp.CnOpts()
        self.__class__.__connection = pysftp.Connection(
            host=self.config.URI,
            username=self.config.USER,
            password=self.config.PASSWORD,
            cnopts=cnopts
        )
        self.__class__.__connections_per_config[self.config] = 1

    @property
    def connection(self) -> pysftp.Connection:
        if not self.__active:
            raise SftpConnectionClosed('The connection was close for this instance')
        if self.__class__.__connection is None:
            self.__connect()
        return self.__class__.__connection

    def close(self):
        if self.__class__.__connection and \
                self.__class__.__connections_per_config[self.config] == 1:
            self.__class__.__connection.close()
            self.__class__.__connection = None
        if self.__class__.__connections_per_config[self.config] > 0:
            self.__class__.__connections_per_config[self.config] -= 1

        if self in self.__class__.__instances_per_config[self.config]:
            self.__class__.__instances_per_config[self.config].remove(self)
        self.__active = False

    def close_all(self):
        for instance in self.__class__.__instances_per_config[self.config]:
            instance.close()

    def __enter__(self) -> pysftp.Connection:
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()
