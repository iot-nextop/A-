# Lab 4 Multi-variable linear regression
import tensorflow as tf
import numpy as np
from firebase import firebase
import datetime

firebase = firebase.FirebaseApplication('https://smartfarm-1681b.firebaseio.com/', None)
i=0

f = open("test.txt",'w')

result_t = list(firebase.get('temperature',None).keys())
for i in range(len(result_t)):
    print('temperature : ',firebase.get('temperature','%s'%(result_t[i])))
    t = firebase.get('temperature','%s' % (result_t[i]))
    f.write(str(t))
    f.write(',')
f.write('\n')

result_h = list(firebase.get('humidity',None).keys())
for i in range(len(result_h)):
    print('humidity : ',firebase.get('humidity','%s'%(result_h[i])))
    f.write(str(firebase.get('humidity', '%s' % (result_h[i]))))
    f.write(',')
f.write('\n')

result_eh = list(firebase.get('earthhumidity',None).keys())
for i in range(len(result_eh)):
    print('earthhumidity : ',firebase.get('earthhumidity','%s'%(result_eh[i])))
    f.write(str(firebase.get('earthhumidity', '%s' % (result_eh[i]))))
    f.write(',')

f.close()


tf.set_random_seed(777)
xy = np.genfromtxt('test.txt', delimiter=',', dtype=np.float32)
x_data = xy[0:2,:-1]
y_data = xy[2:3,:-1]


print(x_data, "\nx_data shape:", x_data.shape)
print(y_data, "\ny_data shape:", y_data.shape)

X = tf.placeholder(tf.float32, shape=[None, None])
Y = tf.placeholder(tf.float32, shape=[None, None])

W = tf.Variable(tf.random_normal([3, 1]), name='weight')
b = tf.Variable(tf.random_normal([3]), name='bias')


hypothesis = tf.matmul(X, W) + b
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.00001)
#(learning_rate=1e-4)
train = optimizer.minimize(cost)


sess = tf.Session()
sess.run(tf.global_variables_initializer())


for step in range(20001):
    cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                   feed_dict={X: x_data, Y: y_data})
    if step % 1000 == 0:
        print(step, "Cost:", cost_val, "\nPrediction:\n", hy_val)

predict = sess.run(hypothesis,feed_dict={X:[[25,0,0],[40,0,0]]}) #온도값3개, 습도값 3개입력
print("예상값",predict)
