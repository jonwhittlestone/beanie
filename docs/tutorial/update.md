# Updating & Deleting

Now that we know how to find documents, how do we change them or delete them?


## Saving changes to existing documents

The easiest way to change a document in the database is using either the `replace` or `save` methods on a altered document. These methods both write the document to the database, but `replace` will raise an exception when the document does not exist yet, while `save` will insert the document. 

Using save:
```python
bar = await Product.find_one(Product.name == "Mars")
bar.price = 10
await bar.save()
```
Or similairly using replace, which trows a `ValueError` if the document does not have an `id` yet, or a `beanie.exceptions.DocumentNotFound` if it does but the id is not present in the collection:
```python
bar.price = 10
try:
    await bar.update()
except (ValueError, beanie.exceptions.DocumentNotFound):
    print("Can't replace a non existing document")
```

Note however that these methods requires multiple queries to the database and replace the entire document with the new version. A more tailered solution can often be created by applying update queries directly on the database level.

## Update queries

Update queries can be performed on the result of a `find` or `find_one` query, or on a document that was returned from an earlier query. Simpler updates can be performed using the `set`, `inc`, and `current_date` methods:
```python
bar = await Product.find_one(Product.name == "Mars")
await bar.set({Product.name:"Gold bar"})
bar = await Product.find_all(Product.price > .5).inc({Product.price: 1})
```

More complex update operations can be performed by calling `update()` with a update operator, similair to find queries:
```python
await Product.find_one(Product.name == "Tony's").update(Set({Product.price: 3.33}))
```
The whole list of the update query operators can be found [here](/api-documentation/operators/update).

Native MongoDB syntax is also accepted:
```python
await Product.find_one(Product.name == "Tony's").update({"$set": {Product.price: 3.33}})
```

## Upsert

To insert a document if no one document was matched the search cruteria during update query, the `upsert` method can be used:
```python
await Product.find_one(Product.name == "Tony's").upsert(
    Set({Product.price: 3.33}), 
    on_insert=Product(name="Tony's", price=3.33, category=chocolate)
)
```

## Deleting documents

Deleting objects works just like updating them, you simply call `delete()`: 


```python
bar = await Product.find_one(Product.name == "Milka")
await bar.delete()

await Product.find_one(Product.name == "Milka").delete()

await Product.find(Product.category.name == "Chocolate").delete()
```
