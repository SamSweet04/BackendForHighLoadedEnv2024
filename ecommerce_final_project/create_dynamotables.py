import boto3

def create_tables():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    # Create Orders Table
    orders_table = dynamodb.create_table(
        TableName='EcommerceOrders',
        KeySchema=[
            {'AttributeName': 'orderId', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'orderId', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Creating Orders Table...")
    orders_table.wait_until_exists()

    # Create Shopping Cart Table
    carts_table = dynamodb.create_table(
        TableName='EcommerceCarts',
        KeySchema=[
            {'AttributeName': 'cartId', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'cartId', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Creating Carts Table...")
    carts_table.wait_until_exists()

if __name__ == '__main__':
    create_tables()