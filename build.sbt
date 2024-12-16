ThisBuild / version := "0.1.0-SNAPSHOT"
ThisBuild / scalaVersion := "2.13.12"

lazy val sparkVersion = "3.5.0"

lazy val root = (project in file("."))
  .settings(
    name := "SparkPlayground",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-core" % sparkVersion,
      "org.apache.spark" %% "spark-sql" % sparkVersion,
      "org.scala-lang" % "scala-reflect" % scalaVersion.value
    ),
    javaOptions ++= Seq(
      "-Djava.home=/path/to/your/jdk8"
    )
  )
