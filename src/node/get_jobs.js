#!/usr/bin/env node
const { MongoClient } = require("mongodb");

const URI = "mongodb://127.0.0.1:27017/job_hunt";

const client = new MongoClient(URI);

const privateDescriptor = (value) => ({
  value,
  writable: false,
  enumerable: false,
  configurable: false,
});

class MyCollection {
  constructor(client, database, collection) {
    Object.defineProperty(this, "_client", privateDescriptor(client));
    Object.defineProperty(this, "_database", privateDescriptor(this._client.db(database)));
    Object.defineProperty(this, "_collection", privateDescriptor(this._database.collection(collection)));
  }

  get database() {
    return this._database.s.namespace.db;
  }

  get collection() {
    return this._collection.s.namespace.collection;
  }

  async find(query = {}, options = {}) {
    try {
      await this._client.connect();
      return await this._collection.find(query, options).toArray();
    } finally {
      await this._client.close();
    }
  }
}

const apply = new MyCollection(client, "job_hunt", "apply");
apply.find({}, { projection: { name: true, area: true, responded: true, date: true, platform: true }})
  .then((list) => console.table(list.map(({ _id, ...attributes }) => ({ _id: String(_id), ...attributes }))));
