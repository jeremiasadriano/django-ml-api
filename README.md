# This project is a simple implementation of a ml model that can predict the feelings of a person based on the text they write

<h4>The model was trained based on a online dataset downloaded on kaggle</h4>

<h4>How to run</h4>
<p>First you'll need create a new enviroment, to do that you just have to:</p>

<code>python3 -m venv .venv</code>
<code>source .venv/bin/activate</code>
<code>pip install django pandas scikit-learn</code>

<p>Now you've created your django enviroment, so now you need to configure your database. As you can see, on this project you can found a docker-compose file and you just need to run it:</p>

<h4>How to run your docker-compose:</h4>
<code>docker-compose up -d</code>

<p>Now you have your database running, so you need to run the migrations:</p>

<h4>How to run migrations</h4>
<code>python3 manage.py migrate</code>

<p>Now you have your database configured, so you can run the server:</p>

<h4>How to run the server</h4>
<code>python3 manage.py runserver</code>

<p>Now you can access the server on your browser on the address: http://localhost:8000</p>

<p>That is it, now you can enjoy your experience!.</p>
