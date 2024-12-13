# Scaling Backend Systems

## Tasks
- **Identify opportunities for sharding or transitioning to microservices**.
- **Plan and document implementation of microservices** for key features, such as product management and order processing.

---

## Proposed Architecture

The backend system will be divided into four key microservices to enhance scalability, reliability, and maintainability.

### Microservices
1. **Product Management Service**:

   1.1. Manages product catalog operations (CRUD).  
   1.2. Implements Redis caching for frequently accessed product details.

2. **Order Processing Service**:
   2.1. Handles order creation, updates, and retrieval.  
   2.2. Supports both eventual and strong consistency models.  
   2.3. Implements caching to optimize repeated reads.

3. **Cart Management Service**:
   3.1. Manages shopping cart operations (add/remove items).  
   3.2. Tracks cart sessions for individual users.

4. **User Management Service**:
   4.1. Handles user authentication and profile management.  
   4.2. Manages secure access to resources.

---

## Architecture Diagram (Plaintext Representation)

```plaintext
+----------------------+       +----------------------+       +----------------------+
| Product Service      |       | Order Service        |       | Cart Service         |
| - Products Table     |       | - Orders Table       |       | - Carts Table        |
| - Redis Cache        |       | - Redis Cache        |       | - Redis Cache        |
+----------------------+       +----------------------+       +----------------------+
            \                      |                       /
             \                     |                      /
              \____________________|_____________________/                      
                              Load Balancer
                                   |
                         +------------------+
                         |    API Gateway   |
                         +------------------+
                                   |
                         +------------------+
                         |  Frontend (UI)   |
                         +------------------+

```
## Code Examples

### Product Management Service

```python
from django.core.cache import cache
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def get_product(product_id):
    cache_key = f'product_{product_id}'
    product = cache.get(cache_key)
    
    if product:
        return product

    table = dynamodb.Table('EcommerceProducts')
    response = table.get_item(Key={'productId': product_id})
    product = response.get('Item', None)

    if product:
        cache.set(cache_key, product, timeout=300)
    return product

def create_product(product_id, name, price, stock):
    table = dynamodb.Table('EcommerceProducts')
    table.put_item(
        Item={
            'productId': product_id,
            'name': name,
            'price': price,
            'stock': stock
        }
    )

```
### Order Processing Service

```python
from django.core.cache import cache
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

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

def get_order(order_id, strong_consistency=False):
    cache_key = f'order_{order_id}'
    order = cache.get(cache_key)

    if order:
        return order

    table = dynamodb.Table('EcommerceOrders')
    response = table.get_item(
        Key={'orderId': order_id},
        ConsistentRead=strong_consistency
    )
    order = response.get('Item', None)

    if order:
        cache.set(cache_key, order, timeout=300)
    return order
```

## Implementation Plan

### Step 1: Transition to Microservices
1. Separate the backend into individual microservices:

   1.1. **Product Management Service**: Handles CRUD operations for the product catalog.  
   1.2. **Order Processing Service**: Manages order-related operations.  
   1.3. **Cart Management Service**: Tracks user cart items and sessions.  
   1.4. **User Management Service**: Handles user authentication and profile management.

### Step 2: Add Caching with Redis
1. Use Redis for frequently accessed data:

   1.1. Cache product details and order information to minimize database reads.  
   1.2. Set caching expiration times (e.g., 5-10 minutes) to balance performance and freshness.

### Step 3: Implement Load Balancing
1. Deploy a load balancer:

   1.1. Place the load balancer between the frontend and backend services.  
   1.2. Ensure it distributes traffic evenly for scalability and high availability.

### Step 4: Shard DynamoDB Tables
1. Implement partition keys for sharding:

   1.1. **EcommerceOrders table**: Use `userId` as a partition key.  
   1.2. **EcommerceCarts table**: Use `cartId` as a partition key.

### Step 5: Deployment
1. Use containerization tools:

   1.1. Leverage Docker or Kubernetes for managing microservice instances.  
   1.2. Deploy microservices independently for ease of scaling and updates.
