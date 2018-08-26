import Drawer from "./Drawer";
import Cassandra from "./Cassandra";

require('jquery');

$(() => {
    const drawer = new Drawer();
    const cassandra = new Cassandra();

    $('#clear').click(() => {
        drawer.initialize();
        cassandra.initialize();
    });
});