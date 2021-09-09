from config import read_yaml_data, DB_CONFIG, PROJECT_NAME
DC = read_yaml_data(DB_CONFIG)[PROJECT_NAME]
if 'solr_info' in DC:
    from .querySolr import search_solr
if 'hbase_info' in DC:
    from .queryHBase import PhoenixServer
if 'es_info' in DC:
    from .queryES import elastic_search
if 'mysql_info' in DC:
    from .queryMysql import MysqlServer
if 'redis_info' in DC:
    from .queryRedis import exec_redis
