## 3 March 2021
The following insert command does also produce an output:
```python
c.execute("""
INSERT INTO variables (var_name, var_type, timestamp) 
VALUES ('meh', 'int', 10);"""
).fetchall()
```
The output just is an empty list `[]`, but it means that
we do not need to distinquish between database editing and query commands.

----

The `InsertCommand` may seem overkill. It is possible to add a `Answer.store_in_db(db_writer: DatabaseWriter)` method and be done with it. However, the indirection of adding an `InsertCommand` inbetween the `Answer` and the `DatabaseWriter` greatly increases exendability, e.g. by adding an undo functionality.