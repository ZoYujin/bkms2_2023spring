# Assignment 1

> Due: 2023-03-21 23:59

- Please upload a single pdf file.
- If you submit assignments after the due date, each day will decrease by 10% from the score. e.g., Submit before 2023-03-22 23:59: -10%

## Objective 

- Understanding Data Modeling
- Ability to run MongoDB, to do CRUD and Aggregation operation

## Scenario

Consider that you are building a book search system that displays user reviews for books on Amazon's Book Store. Assume that only books and their reviews will be shown, and that login and other functionalities are not considered.

1. (5 pts) Data Modeling: Describe your data model with some explanation (figures, text, etc.). Consider the following points:
    - What will the book search system look like?
    - What kind of data will be displayed to the user?
    - How will collections be set up?
    - What is your schema definition? Will all columns be stored?
    - How will null data be handled?
    - ...

2. (5 pts) Insert your data into your database. Write down all the process how you create your database and collections, also the insertion of data.
3. (5 pts) Information Retrieval & Aggregation Operation: Write at least three to five queries to find valuable information from the current data. You should include at least one aggregation operation.

Since there is no single answer, please feel free to try your self as much as possible. For Q2 and Q3, TA will build the database based on your description. So all the **codes** or **descriptions of operation** should be included with detail desciptions. You can either use MongoDB Shell, MongoDB Compass or python scripts.

## Data

- Please download the data from [https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews) (may need login)
- Better not to change the dataset filename, incase it doesn't work for TA to grade(or you should describe in your document).

## Start MongoDB Shell(`mongosh`)

```bash
$ docker exec -it mongodb /bin/bash
$ mongosh
```

## MongoDB Compass

[MongoDB Compass](https://www.mongodb.com/products/compass) is an interactive tool for querying, optimizing, and analyzing your MongoDB data. Get key insights, drag and drop to build pipelines, and more.

> download: https://www.mongodb.com/try/download/compass

### Connect to MongoDB Compass

```
mongodb://localhost:27017
```
