import logging
from cassandra.cluster import Cluster

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

KEYSPACE = "MNISTSpace"

cluster = Cluster(contact_points=['127.0.0.1'])
session = cluster.connect()

spacenames = list(map(lambda space: space.keyspace_name, session.execute("SELECT * FROM system_schema.keyspaces")))


def setUp():
    createKeySpace()
    createTable()


def createKeySpace():
    log.info("run create key space")
    try:
        log.info("Creating Keyspace...")

        if KEYSPACE not in spacenames:
            log.info("Keyspace %s does not exist, creating..." % KEYSPACE)
            session.execute("""
                CREATE KEYSPACE %s WITH replication = 
                { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % KEYSPACE)
            log.info("Keyspace %s created successfully." % KEYSPACE)
        else:
            log.info("Keyspace %s already existed." % KEYSPACE)

        log.info("Setting Keyspace...")
        session.set_keyspace(KEYSPACE)
        session.execute('use %s' % KEYSPACE)
    except Exception as e:
        log.error("Unable to create keyspace.")
        log.error(e)


def createTable():
    log.info("run create table")
    tablename = "%s.MNISTDataTable" % KEYSPACE
    session.execute("""CREATE TABLE IF NOT EXISTS %s 
        (id int PRIMARY KEY, img_data text, prediction text, create_time DATE)
        """ % tablename)