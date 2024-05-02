"""
conding: utf-8
@time:2024/4/16 16:11
"""
import logging

logger = logging.getLogger('items')


class LocalRemoteRouter(object):
    """
    A router to decide select local or remote sae db
    """
    init = True
    local = True

    def is_local_env(self):
        local_env = False
        try:
            import sae
        except(ImportError):
            local_env = True
            logger.info("import sae error")
        else:
            local_env = False
            logger.info("import sae ok")
        return local_env

    def db_for_read(self, model, **hints):
        if self.init == True:
            self.init = False
            self.local = self.is_local_env()

        if self.local == True:
            return 'default'
        else:
            return 'remote'

    def db_for_write(self, model, **hints):
        if self.init == True:
            self.init = False
            self.local = self.is_local_env()

        if self.local == True:
            return 'default'
        else:
            return 'remote'
