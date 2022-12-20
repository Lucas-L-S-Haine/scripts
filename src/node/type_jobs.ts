#!/usr/bin/env ts-node
import { MongoClient, ObjectId, Db, Collection } from "mongodb";

const URI = "mongodb://127.0.0.1:27017/job_hunt";

const client = new MongoClient(URI);

interface Descriptor<T> {
  value: T;
  writable: boolean;
  enumerable: boolean;
  configurable: boolean;
}

const privateDescriptor = (value: unknown): Descriptor<typeof value> => ({
  value,
  writable: false,
  enumerable: false,
  configurable: false,
});

class MyCollection {
  private _client: MongoClient;
  private _database: Db;
  private _collection: Collection;
  readonly database: string;
  readonly collection: string;

  constructor(client: MongoClient, database: string, collection: string) {
    this._client = client;
    this._database = this._client.db(database);
    this._collection = this._database.collection(collection);
    this.database = this._database.namespace;
    this.collection = this._collection.namespace.split(".")[1];

    Object.defineProperty(this, "_client", privateDescriptor(this._client));
    Object.defineProperty(this, "_database", privateDescriptor(this._database));
    Object.defineProperty(this, "_collection", privateDescriptor(this._collection));
  }

  async find(query = {}, options = {}) {
    try {
      await this._client.connect();
      return await this._collection.find(query, options).toArray();
    } finally {
      await this._client.close();
    }
  }

  async findOne(query = {}, options = {}) {
    try {
      await this._client.connect();
      return await this._collection.findOne(query, options);
    } finally {
      await this._client.close();
    }
  }
}

export const apply = new MyCollection(client, "job_hunt", "apply");
apply.find({}, { projection: { name: true, area: true, responded: true, date: true, platform: true }})
  .then((list) => console.table(list.map(({ _id , ...attributes }: { _id: ObjectId }) => ({ _id: String(_id), ...attributes }))));
