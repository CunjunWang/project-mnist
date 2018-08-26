const cassandra = require('cassandra-driver');

import {KEYSAPCE, LOCALHOST} from 'constants';

export default class Cassandra {

    constructor() {
        this.client = new cassandra.Client({ contactPoints: [ LOCALHOST ], keyspace: KEYSAPCE });
        this.initialize();
    }

    initialize() {

        const query = 'SELECT * FROM users WHERE key = ?';
    }


}