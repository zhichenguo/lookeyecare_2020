<p>Look Eye Care Optical Online Store</p>
<p>First, download this repository or pull this repository to your local machine:</p>
<pre><code>git clone https://github.com/zhichenguo/lookeyecare.git</code></pre>
<p>Recommend Python version 3.8. To create a new environment simply run:</p>
<pre><code>conda create --name env python=3.8 -y</code></pre>
<p>Once it's created, then activate it by running:</p>
<pre><code>conda activate env</code></pre>
<p>Please navigate to <code>lookeyecare/</code> directory, then run the following commands to install all the package required:</p>
<pre><code>pip install -r requirements.txt</code></pre>
<p>Run the following commands to start the Django development server:</p>
<pre><code>python manage.py runserver</code></pre>
<p>The Website can be accessed via <a href="http://127.0.0.1:8000/home/" rel="nofollow">http://127.0.0.1:8000/home/</a> with any browser to test the features</p>
<p> Before Login, You can browse the products list and detail</p>
<p>Login with one of the un-superuser <code>username: bill    password: Bb_123456</code> to test the basic features.</p>
<p>Login with the superuser <code>username: John    password: Jj_123456</code> to test all the features including create, update and delete.</p>
<p>This project is built on Django Framework. Styling with Boostrape 4. django-allauth would take care of the Authentication. Stripe would handle the payment system.</p>

