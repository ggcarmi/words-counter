# Words Counter

`words` is an flask app for counting the frequencies in given text. 


## How to start 


### Requirements 
- `docker`
*or*
- local `redis`, `python 3.7+` and `pipenv` intstalled

### Build and run
first, you should clone the project:
```sh
$ mkdir Project
$ cd Project
$ git clone https://github.com/ggcarmi/words-counter .
```

Then, there are two ways to run the project. 

1. the easiest way is with docker [`docker`](https://www.docker.com/products/docker-desktop) :

    ``` sh 
    $ docker-compose up 
    ```

    it will launch 2 docker containers: flask app and redis.
    
2. The second way is to run redis on docker(or on your machine if you preffer), 
    and manually run the flask app on your machine

    ```sh
    $ docker run -p 6379:6379 redis
    $ pipenv install
    $ flask run
    ```

now the app is available at http://127.0.0.1:5000/


## Project structure

    .
    ├── words                       
    │   ├── api
    │       └── resource          the Rest Resources. in this app we have only one. Word
    │   ├── common                common functionality for parsing text
    │   ├── database              database related operations
    │   └── tests
    ├── docker-compose.yml
    ├── Dockerfile
    ├── .flaskenv
    ├── Pipfile
    ├── Pipefile.lock
    ├── README.md
    
## API

we use `GET  /api/v1/words/<input_word>` to get the occurrence of a given word.

we use `POST /api/v1/words` to insert words.

in the request `body` we have to pass 2 parameters:
   
  1. `input_type`, and his value should be one of the three: `text`, `url`, `file`.
   
  2. `data`, which is the actual data for the given type. text string, url path or path to file. accordingly to `input_type`.
    
    
    
## Sample API Calls


to insert words from text string:

``` POST /api/v1/words    body={ "input_type": "text", "data": "Hi! My name is (what?), my name is (who?), my name is Slim Shady"} ```


to insert words from url:

``` POST /api/v1/words    body={ "input_type": "url", "data": "https://jsonplaceholder.typicode.com/todos"} ```


to insert words from text file(i already copy some test files to the folder words/tests/test_files):

``` POST /api/v1/words    body={ "input_type": "file", "data": "C:\\lemonade\\words\\tests\\test_files\\words3.txt"} ```


to insert words from text file (this version workd on the docker. just run docker compose and than run this request:

``` POST /api/v1/words    body={ "input_type": "file", "data": "./words/tests/test_files/words3.txt"} ```


to get the total occurrence of a given word:

``` GET /api/v1/words/my ```



## How it works?

the app contains 2 components: `Flask` app and `Redis` database.
when we get one of the 3 input types: `text`, `url`, `file`,
we parse it, and store the words in Redis as key=word, value=frequencies.

so when we want to get specific word, its very fast to retrieve it,
we just get the value of that ord in redis.

for very large files (>GB), we use parallel computing. 
we read the file in chunks of X lines at a time.
than we send that chunk to aub-process, to handle it.
when it done, the ,ain process get the result back,
and merge all the results.



## Assumptions
- words are case insensitive - we convert the words to lowercase before saving them.
- results persist between runs - it store in redis
- input file, for processing, located on the same machine of the app.