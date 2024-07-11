from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, sum as _sum


class RevenueCalculator:
    @staticmethod
    def compute_monthly_revenue(data):
        data = data.withColumn('order_date', col('order_date').cast('timestamp'))
        data = data.withColumn('total_price', col('product_price') * col('quantity'))
        grouped_data = data.groupBy(year('order_date').alias('year'), month('order_date').alias('month')) \
            .agg(_sum('total_price').alias('total_revenue')) \
            .orderBy('year', 'month')
        return grouped_data

    @staticmethod
    def compute_product_revenue(data):
        data = data.withColumn('total_sales', col('product_price') * col('quantity'))
        grouped_data = data.groupBy('product_id') \
            .agg(_sum('total_sales').alias('total_revenue'))
        return grouped_data

    @staticmethod
    def compute_customer_revenue(data):
        data = data.withColumn('total_price', col('product_price') * col('quantity'))
        grouped_data = data.groupBy('customer_id') \
            .agg(_sum('total_price').alias('total_revenue'))
        return grouped_data

    @staticmethod
    def top_n_customers(data, number_of_customers=10):
        customer_revenue = RevenueCalculator.compute_customer_revenue(data)
        top_customers = customer_revenue.orderBy(col('total_revenue').desc()).limit(number_of_customers)
        return top_customers


if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("RevenueCalculator") \
        .getOrCreate()

    # Read data from a local file
    data = spark.read.csv("../data/orders.csv", header=True, inferSchema=True)

    # Perform the calculations
    monthly_revenue = RevenueCalculator.compute_monthly_revenue(data)
    product_revenue = RevenueCalculator.compute_product_revenue(data)
    customer_revenue = RevenueCalculator.compute_customer_revenue(data)
    top_customers = RevenueCalculator.top_n_customers(data, 10)

    # Show the results
    monthly_revenue.show()
    product_revenue.show()
    customer_revenue.show()
    top_customers.show()

    # dump output to xlsx
    monthly_revenue.toPandas().to_excel('report/monthly_revenue.xlsx', index=False)
    product_revenue.toPandas().to_excel('report/product_revenue.xlsx', index=False)
    customer_revenue.toPandas().to_excel('report/customer_revenue.xlsx', index=False)

    spark.stop()
