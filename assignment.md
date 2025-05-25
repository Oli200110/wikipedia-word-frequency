# Assignment: Wikipedia Word-Frequency Dictionary

## Objective

Develop a Python server application that takes an _article_ and a _depth_ parameter as input, and generates a word-frequency dictionary by traversing Wikipedia articles up to the specified depth.

## Traversing Functionality

- The application should start with the given _article_ and retrieve its content.
- It should then identify and follow the links to other Wikipedia articles referenced within the original article.
- This process should continue recursively, up to the specified _depth_ parameter.
- For example, if _depth_ is set to 2, the application should analyze the original article, the articles referenced by the original article, and the articles referenced by those articles.
- Ensure that the traversal does not revisit articles that have already been processed to avoid infinite loops.

## Requirements

1. **APIs:**

   - **GET /word-frequency**

     - **Parameters:**
       - `article` (string): The title of the Wikipedia article to start from.
       - `depth` (int): The depth of traversal within Wikipedia articles.

     - **Response:**
       - A word-frequency dictionary that includes the count and percentage frequency of each word found in the traversed articles.

   - **POST /keywords**

     - **Request Body:**
       - `article` (string): The title of the Wikipedia article.
       - `depth` (int): The depth of traversal.
       - `ignore_list` (array[string]): A list of words to ignore.
       - `percentile` (int): The percentile threshold for word frequency.

     - **Response:**
       - A dictionary similar to the one returned by /word-frequency, but excluding words in the ignore list and filtered by the specified percentile.

2. **Additional Requirements:**

   - No authentication is required.
   - No database is needed.
   - Include unit tests for your code.
   - You are encouraged to use AI tools if needed.

## Submission

- Push your code to a GitHub repository.
- Share the repository link with us.