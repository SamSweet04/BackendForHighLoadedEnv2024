# Distributed Systems and Data Consistency

## Overview
This project implements a distributed architecture using Amazon DynamoDB for storing and managing order and cart data. The implementation supports eventual and strong consistency models, API interactions, and caching for improved performance.

---

## DynamoDB Tables

### 1. Orders Table (`EcommerceOrders`)
- **Primary Key**: `orderId` (String)
- **Attributes**:
  - `userId`: User who placed the order
  - `totalAmount`: Total amount of the order
  - `status`: Status of the order (e.g., `PENDING`, `COMPLETED`)

### 2. Carts Table (`EcommerceCarts`)
- **Primary Key**: `cartId` (String)
- **Attributes**:
  - `userId`: User owning the cart
  - `products`: List of products in the cart
  - `totalAmount`: Total amount of the cart

---

## Core Operations

### 1. Table Creation
The DynamoDB tables were created programmatically using the following script:
```python
import boto3

def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Orders Table
    orders_table = dynamodb.create_table(
        TableName='EcommerceOrders',
        KeySchema=[{'AttributeName': 'orderId', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'orderId', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    orders_table.wait_until_exists()

    # Carts Table
    carts_table = dynamodb.create_table(
        TableName='EcommerceCarts',
        KeySchema=[{'AttributeName': 'cartId', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'cartId', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    carts_table.wait_until_exists()

if __name__ == '__main__':
    create_tables()
```

### 2. Adding an Order
The following function adds a new order to the `EcommerceOrders` table:
```python
def create_order(order_id, user_id, total_amount):
    table = dynamodb.Table('EcommerceOrders')
    table.put_item(
        Item={
            'orderId': order_id,
            'userId': user_id,
            'totalAmount': str(total_amount),
            'status': 'PENDING'
        }
    )
```
### 3. Retrieving an Order

This function retrieves an order using eventual or strong consistency:
```python
def get_order(order_id, use_strong_consistency=False):
    table = dynamodb.Table('EcommerceOrders')
    response = table.get_item(
        Key={'orderId': order_id},
        ConsistentRead=use_strong_consistency
    )
    return response.get('Item', None)
```

### 4. Updating Order Status

The function below updates the status of an order:
```
def update_order_status(order_id, status):
    table = dynamodb.Table('EcommerceOrders')
    table.update_item(
        Key={'orderId': order_id},
        UpdateExpression="SET #s = :status",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":status": status}
    )
```
## Consistency Models

### Eventual Consistency
- Default model in DynamoDB.
- Provides better performance by allowing slightly stale reads.

### Strong Consistency
- Ensures the latest data is always returned.
- Enabled by setting `ConsistentRead=True` when reading data.

---

## Caching with Redis

Frequently accessed data is cached using Redis to reduce DynamoDB read costs. Example:
```python
from django.core.cache import cache

def get_order_with_cache(order_id):
    cache_key = f'order_{order_id}'
    cached_order = cache.get(cache_key)

    if cached_order:
        return cached_order

    order = get_order(order_id)
    if order:
        cache.set(cache_key, order, timeout=300)
    return order
```
## Summary
- DynamoDB was successfully integrated as the distributed database.
- Tables `EcommerceOrders` and `EcommerceCarts` were created and tested.
- API endpoints support CRUD operations with caching and consistency models.