# Lab 4 Multi-variable linear regression
import tensorflow as tf
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



cred = credentials.Certificate('C:/smartfarm-1681b-firebase-adminsdk-2sevr-cbd30f81c0.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://smartfarm-1681b.firebaseio.com/'
})

tf.set_random_seed(777)  # for reproducibility

ref = db.reference('humidity/')
print(ref.get())




xy = np.loadtxt('smartfarm-1681b-export.json', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-1]
y_data = xy[:, [-1]]


# Make sure the shape and data are OK
print(x_data, "\nx_data shape:", x_data.shape)
print(y_data, "\ny_data shape:", y_data.shape)


# placeholders for a tensor that will be always fed.
X = tf.placeholder(tf.float32, shape=[None, 2])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([2, 1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')

# Hypothesis
hypothesis = tf.matmul(X, W) + b

# Simplified cost/loss function
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# Minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0003)
#(learning_rate=1e-4)
train = optimizer.minimize(cost)

# Launch the graph in a session.
sess = tf.Session()
# Initializes global variables in the graph.
sess.run(tf.global_variables_initializer())


for step in range(20001):
    cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                   feed_dict={X: x_data, Y: y_data})
    if step % 1000 == 0:
        print(step, "Cost:", cost_val, "\nPrediction:\n", hy_val)


# Ask my score

predict = sess.run(hypothesis,feed_dict={X:[[50,25]]})
print("예상값",predict)

ref = db.reference() #db 위치 지정
ref.update({'예측값' : int(predict[0])})

