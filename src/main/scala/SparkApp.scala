import org.apache.spark.sql.SparkSession

object SparkApp {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("SparkPlayground")
      .master("spark://localhost:7077") // Spark master in Docker
      .getOrCreate()

    // Example: Process some local data
    val data = Seq(("Alice", 29), ("Bob", 35), ("Cathy", 28))
    val df = spark.createDataFrame(data).toDF("Name", "Age")
    df.show()

    spark.stop()
  }
}