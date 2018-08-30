import logging
from cassandra.cluster import Cluster

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

KEY_SPACE = "MNISTSpace"

cluster = Cluster(contact_points=['127.0.0.1'])
session = cluster.connect()

space_names = list(map(lambda space: space.keyspace_name, session.execute("SELECT * FROM system_schema.keyspaces")))


def cassandra_setup():
    create_key_space()
    create_table()


def create_key_space():
    log.info("run create key space")
    try:
        log.info("Creating Keyspace...")

        if KEY_SPACE not in space_names:
            log.info("Keyspace %s does not exist, creating..." % KEY_SPACE)
            session.execute("""
                CREATE KEYSPACE %s WITH replication = 
                { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % KEY_SPACE)
            log.info("Keyspace %s created successfully." % KEY_SPACE)
        else:
            log.info("Keyspace %s exists." % KEY_SPACE)

        log.info("Setting Keyspace...")
        session.set_keyspace(KEY_SPACE)
        session.execute('use %s' % KEY_SPACE)
    except Exception as e:
        log.error("Unable to create keyspace.")
        log.error(e)


def create_table():
    log.info("run create table")
    table_name = "%s.MNISTDataTable" % KEY_SPACE
    session.execute("""CREATE TABLE IF NOT EXISTS %s 
        (id uuid PRIMARY KEY, softmax_prediction int , convolution_prediction int , create_time float)
        """ % table_name)
