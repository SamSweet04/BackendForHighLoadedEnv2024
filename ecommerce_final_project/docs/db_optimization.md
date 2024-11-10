# Database Optimization Strategies

In this project, we implemented several optimizations to improve database performance, especially under high load.

## 1. Indexing

Indexes help speed up data retrieval. We added indexes on frequently queried fields:

- **Product Model**:
  - Index on `category` to improve product search by category.

- **Order Model**:
  - Composite index on `user` and `created_at` to speed up order search by user and date.

- **OrderItem Model**:
  - Index on `product` for faster lookup of order items by product.

These indexes make data access faster and reduce query time.

## 2. Query Optimization

To avoid the N+1 query issue and reduce database load, we used `select_related` and `prefetch_related` in key views:

- **OrderViewSet**: Loads orders with users and items in a single query.
- **ProductViewSet**: Loads products with their categories.
- **ShoppingCartViewSet**: Loads shopping carts with associated users.
- **CartItemViewSet**: Loads cart items with carts and products.
- **ReviewViewSet**: Loads reviews with users and products.
- **WishlistViewSet and WishlistItemViewSet**: Loads wishlists with users and items with products.

These optimizations reduce the number of database queries and improve overall performance.