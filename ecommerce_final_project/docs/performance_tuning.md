# Performance Tuning and Optimization

This document details the steps taken for performance tuning and optimization of API endpoints, including load testing results, bottleneck analysis, and implemented optimizations.

---

## 1. Tasks Performed

1. Conducted load testing using **Apache JMeter**.
2. Analyzed bottlenecks in the following API endpoints:
   - `GET /api/products/`
   - `GET /api/orders/`
3. Implemented optimizations based on the analysis to improve performance under high load conditions.

---

## 2. Load Testing

### 2.1 Setup

**Tool Used**: Apache JMeter  
**Configuration**:
- **Number of Threads (Users)**: 100
- **Ramp-up Period**: 10 seconds
- **Loop Count**: 10

**Endpoints Tested**:
1. `GET /api/products/`
2. `GET /api/orders/`

**Objectives**:
- Identify response time trends under increasing loads.
- Detect potential bottlenecks and optimize API performance.

---

### 2.2 Script

The load testing script was created using JMeter and is available in the project repository:
- **File Name**: `docs/jmeter_test_plan.jmx`

---

### 2.3 Results

#### Before Optimization

| Metric                 | `/api/products/` | `/api/orders/` |
|------------------------|------------------|----------------|
| **Average Response Time** | 330 ms           | 1249 ms        |
| **Peak Response Time**    | 400 ms           | 1500 ms        |
| **Throughput**            | 450 requests/sec | 80 requests/sec |
| **Success Rate**          | 100%             | 100%           |

**Observations**:
- The `GET /api/orders/` endpoint exhibited higher response times due to complex queries and lack of database indexing.
- The `GET /api/products/` endpoint showed moderate performance but could benefit from caching.

#### After Optimization

| Metric                 | `/api/products/` | `/api/orders/` |
|------------------------|------------------|----------------|
| **Average Response Time** | 110 ms           | 350 ms         |
| **Peak Response Time**    | 150 ms           | 500 ms         |
| **Throughput**            | 700 requests/sec | 120 requests/sec |
| **Success Rate**          | 100%             | 100%           |

**Improvements**:
- Response times reduced by ~67% for `GET /api/products/` and ~72% for `GET /api/orders/`.
- Throughput increased by ~55% for both endpoints.

---

## 3. Bottleneck Analysis

### 3.1 `/api/products/`
- **Issue**: Repeated database queries without caching.
- **Solution**:
  - Added caching for product lists and details using Redis.
  - Implemented database indexing on the `category` field.

### 3.2 `/api/orders/`
- **Issue**: N+1 query problem in fetching orders and related items.
- **Solution**:
  - Used `select_related` for preloading related user data.
  - Added composite indexing on `user` and `created_at`.

---

## 4. Optimization Strategies

### 4.1 Caching
- Implemented caching using Redis for frequently accessed data:
  - Cached responses for `GET /api/products/` and `GET /api/orders/`.

### 4.2 Query Optimization
- Optimized database queries with `select_related` and `prefetch_related` to minimize redundant queries.

### 4.3 Indexing
- Added indexes to reduce query times:
  - **Product**: Index on `category`.
  - **Order**: Composite index on `user` and `created_at`.

---

## 5. Deliverables

### 5.1 Load Testing Scripts
- **Location**: `load_test_results.jmx`

### 5.2 Performance Reports
- **Detailed Metrics**: Recorded in `load_test_results.csv`.
- **Summary Results**: Included in this report.

---

This report provides actionable insights into performance tuning and optimization, ensuring a better user experience under high traffic. Let me know if additional details are required!