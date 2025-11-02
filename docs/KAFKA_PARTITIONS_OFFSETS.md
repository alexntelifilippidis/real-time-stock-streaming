"""
Kafka Partitions & Offsets Explanation
========================================

## What are Partitions?

Partitions are like separate "lanes" or "buckets" within a Kafka topic:

- A topic can have multiple partitions (e.g., stock_prices might have 3 partitions: 0, 1, 2)
- Messages are distributed across partitions for parallel processing
- Each partition maintains its own ordered sequence of messages

### Partition Assignment:
1. **With Key** (our approach): Messages with the same key go to the same partition
   - Example: All AAPL messages → Partition 1
   - Example: All GOOGL messages → Partition 2
   - Ensures ordering for messages with the same key

2. **Without Key**: Round-robin distribution across partitions
   - Message 1 → Partition 0
   - Message 2 → Partition 1
   - Message 3 → Partition 2
   - Message 4 → Partition 0 (cycles back)

## What are Offsets?

Offsets are unique sequential IDs for messages within a partition:

- Each partition has its own offset sequence starting at 0
- Offsets increment by 1 for each new message
- They act like bookmarks to track position in the stream

### Example:
```
Partition 0:
  Offset 0: {"symbol": "AAPL", "price": 150.00}
  Offset 1: {"symbol": "AAPL", "price": 151.25}
  Offset 2: {"symbol": "AAPL", "price": 149.80}

Partition 1:
  Offset 0: {"symbol": "GOOGL", "price": 140.00}
  Offset 1: {"symbol": "GOOGL", "price": 141.50}

Partition 2:
  Offset 0: {"symbol": "MSFT", "price": 380.00}
```

## In Kafka UI:

When you open Kafka UI (http://localhost:8080), you'll see:

1. **Topics Tab**:
   - Click on "stock_prices"
   - See number of partitions (e.g., 3)
   - See total messages across all partitions

2. **Messages Tab**:
   - Filter by partition (0, 1, 2, etc.)
   - See offset numbers for each message
   - See the key (stock symbol) and value (price data)

3. **Consumer Groups Tab**:
   - See which offset each consumer is reading from
   - Track consumer lag (how far behind they are)

## Why This Matters:

✅ **Ordering**: Messages with the same key are ordered within their partition
✅ **Scalability**: Multiple consumers can read different partitions in parallel
✅ **Fault Tolerance**: If a consumer crashes, it can resume from its last offset
✅ **Replay**: Can rewind to any offset to reprocess messages

## Our Implementation:

In `src/kafka/producer.py`, we use:
```python
future = self.producer.send(
    self.topic,
    key=record.symbol.encode('utf-8'),  # ← Stock symbol as key
    value=record.model_dump()
)
```

This means:
- All AAPL messages → Same partition (consistent ordering)
- All GOOGL messages → Same partition (consistent ordering)
- etc.

The logs show:
```
✅ AAPL   | $150.00 | Vol: 5,234 | 📍 Partition: 1 | 📌 Offset: 42
✅ GOOGL  | $140.00 | Vol: 8,192 | 📍 Partition: 2 | 📌 Offset: 38
```

You can see exactly which partition and offset each message lands in!

