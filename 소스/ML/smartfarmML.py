# Lab 4 Multi-variable linear regression
import tensorflow as tf
import numpy as np
from firebase import firebase
import datetime

firebase = firebase.FirebaseApplication('https://smartfarm-1681b.firebaseio.com/', None)
i=0

f = open("test.txt",'w')

result_h = list(firebase.get('humidity',None).keys())
result_t = list(firebase.get('temperature',None).keys())
result_eh = list(firebase.get('earthhumidity',None).keys())

for i in range(len(result_t)):
    print('temperature : ',firebase.get('temperature','%s'%(result_t[i])))
    t = firebase.get('temperature','%s' % (result_t[i]))
    f.write(str(t))
    f.write(',')
    print('humidity : ',firebase.get('humidity','%s'%(result_h[i])))
    f.write(str(firebase.get('humidity', '%s' % (result_h[i]))))
    f.write(',')
    print('earthhumidity : ',firebase.get('earthhumidity','%s'%(result_eh[i])))
    f.write(str(firebase.get('earthhumidity', '%s' % (result_eh[i]))))
    f.write(',')
    f.write('\n')

f.close()


tf.set_random_seed(777)
xy = np.genfromtxt('test.txt', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-2]
y_data = xy[:, [-2]]


print(x_data, "\nx_data shape:", x_data.shape)
print(y_data, "\ny_data shape:", y_data.shape)

X = tf.placeholder(tf.float32, shape=[None, 2])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([2, 1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')


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

predict = sess.run(hypothesis,feed_dict={X:[[25,48]]}) #온도값, 습도값입력
print("예상값",int(predict[0]))


firebase.post('예측값 log',int(predict[0]))