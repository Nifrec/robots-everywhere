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

The `InsertCommand` may seem overkill. 
It is possible to add a `Answer.store_in_db(db_writer: DatabaseWriter)` 
method and be done with it. 
However, the indirection of adding an `InsertCommand` 
inbetween the `Answer` and the `DatabaseWriter` greatly increases extendability,
e.g. by allowing an undo functionality.

----

It is currently not possible to insert multiple values for the same `Variable`
in the same second. 
Given the usecase this does not seem probematic? 
It would be easy to change.