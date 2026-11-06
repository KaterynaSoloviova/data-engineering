import org.apache.spark.sql.SparkSession

object Main {

  def main(args: Array[String]): Unit = {

    // 1. Create a local Spark session
    val spark = SparkSession.builder()
      .appName("britmart_foundations")
      .master("local[*]")
      .getOrCreate()

    // 2. Import Spark implicits
    import spark.implicits._

    // 3. Create the data
    val data = Seq(
      (101, "London", 45.50),
      (102, "Manchester", 18.00),
      (103, "Leeds", 30.00)
    )

    // 4. Create a DataFrame
    val df = data.toDF("id", "city", "amount")

    // 5. Display the rows
    df.show()

    // 6. Stop the Spark session
    spark.stop()
  }
}
