
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
    return {"message": "Order created successfully!"}


def get_order(order_id, use_strong_consistency=False):

    cache_key = f'order_{order_id}'
    cached_order = cache.get(cache_key)


    if cached_order:
        return cached_order


    table = dynamodb.Table('EcommerceOrders')
    response = table.get_item(
        Key={'orderId': order_id},
        ConsistentRead=use_strong_consistency
    )
    order = response.get('Item', None)


    if order:
        cache.set(cache_key, order, timeout=60 * 5)

    return order


def update_order_status(order_id, status):
    table = dynamodb.Table('EcommerceOrders')
    table.update_item(
        Key={'orderId': order_id},
        UpdateExpression="SET #s = :status",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":status": status},
    )
    return {"message": f"Order {order_id} updated to {status}!"}