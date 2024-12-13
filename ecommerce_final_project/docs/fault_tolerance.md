# Fault Tolerance and Resilience

This document outlines the fault tolerance and resilience strategies I implemented (or designed) for the project. These measures are essential for ensuring system availability, reducing downtime, and safeguarding user data. The implementation includes database redundancy, caching failover, load balancing, and disaster recovery planning.

---

## Tasks Overview

1. **Redundancy in Critical Components**
   - Configured database replication for PostgreSQL.
   - Set up Redis in a clustered mode for high availability.
   - Designed load balancing using Nginx.

2. **Disaster Recovery Plan**
   - Developed a backup and restore strategy for PostgreSQL and DynamoDB.
   - Created a recovery procedure to minimize downtime.

---

## Implementation

### 1. **Redundancy for Critical Components**

#### **PostgreSQL Replication**
To ensure database availability and minimize data loss, I configured replication for PostgreSQL.

**Steps:**
1. **Primary Server Configuration**  
   Modify `postgresql.conf`:
   ```conf
   wal_level = replica
   max_wal_senders = 3
   hot_standby = on
   ```
   
2.	**Standby Server Setup**

On the standby server, execute:
```bash
pg_basebackup -h PRIMARY_HOST -D /path/to/data -U postgres -Fp -Xs -P -R
```

3.	**Verify Replication**

Check replication status on the primary:

```sql
SELECT * FROM pg_stat_replication;
```

**Redis Clustering**

Redis was set up in cluster mode to ensure caching resilience.

Steps:
	1.	Create Redis Cluster
```bash
redis-cli --cluster create 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 --cluster-replicas 1
```

2.	**Update Django Settings**

Configure CACHES in settings.py:

```python 
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': [
            "redis://127.0.0.1:6379",
            "redis://127.0.0.1:6380",
            "redis://127.0.0.1:6381",
        ],
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

**Nginx Load Balancing**

Nginx was configured to distribute requests between multiple backend instances.

Steps:
	1.	Install Nginx

```bash
brew install nginx
```
   2.	Configure Load Balancing
 Add this to /usr/local/etc/nginx/nginx.conf:
```
upstream backend_servers {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend_servers;
    }
}
```

3.	Restart Nginx
```
brew services restart nginx
```


2. **Backup and Disaster Recovery**

PostgreSQL Backup

Steps:

1.	Backup the database using pg_dump:

```
pg_dump -U postgres -h localhost -p 5433 your_database > backup.sql
```

2.	Automate backups with cron:

```
crontab -e
# Add the following line for daily backups at midnight
0 0 * * * pg_dump -U postgres -h localhost -p 5433 your_database > /path/to/backup.sql
```

**DynamoDB Backup**

Steps:
1.	Export DynamoDB tables to S3:
```
aws dynamodb export-table-to-point-in-time \
    --table-name your_table_name \
    --s3-bucket your_backup_bucket \
    --region your_region
```

2.	Automate with a scheduled AWS Lambda function.

### Recovery Plan
1.	Restore PostgreSQL:
```
psql -U postgres -h localhost -p 5433 your_database < backup.sql
```

2.	Restore DynamoDB:
```
aws dynamodb import-table \
    --table-name your_table_name \
    --s3-bucket your_backup_bucket \
    --region your_region
```

## Deliverables

1. **Redundancy:**

   1.1 PostgreSQL replication configuration.

   1.2 Redis cluster setup.

   1.3 Nginx load balancing configuration.

2. **Disaster Recovery:**

   2.1 Backup scripts for PostgreSQL and DynamoDB.

   2.2 Documented recovery steps.

3. **Documentation:**

   3.1 Comprehensive fault tolerance and resilience strategy in `docs/fault_tolerance.md`.

This implementation ensures that the application remains resilient under high load, minimizes downtime, and protects user data. By combining redundancy, failover mechanisms, and disaster recovery, the system is well-prepared for unexpected failures. 💪