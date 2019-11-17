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
result_eh = list(firebase.get('earthhumidity',None).keys()) #DB에서 각각의 키값을 불러옴

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
#학습데이터로 쓰기위해 test.txt파일에 온도,습도, 토양습도순으로 기록함

f.close()


tf.set_random_seed(777)
xy = np.genfromtxt('test.txt', delimiter=',', dtype=np.float32)
x_data = xy[:, 0:-2]
y_data = xy[:, [-2]]
#test.txt에 저장된 데이터를 온도,습도를 x데이터로 토양습도값을 y데이터로 사용

print(x_data, "\nx_data shape:", x_data.shape)
print(y_data, "\ny_data shape:", y_data.shape)

X = tf.placeholder(tf.float32, shape=[None, 2])
Y = tf.placeholder(tf.float32, shape=[None, 1])

W = tf.Variable(tf.random_normal([2, 1]), name='weight')
b = tf.Variable(tf.random_normal([1]), name='bias')
#2개의 x데이터가 하나의 배열을 이루기 때문에 2,1형태 y데이터는 1개의 데이터이므로 1형태

hypothesis = tf.matmul(X, W) + b
cost = tf.reduce_mean(tf.square(hypothesis - Y))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.00001)
#학습률= W값의 이동범위 크기가 작을수록 느림, 클수록 빠르나 적절한 값의 범위 넘을 확률 올라감
train = optimizer.minimize(cost)


sess = tf.Session()
sess.run(tf.global_variables_initializer())


for step in range(20001):
    cost_val, hy_val, _ = sess.run([cost, hypothesis, train],
                                   feed_dict={X: x_data, Y: y_data})
    if step % 1000 == 0:
        print(step, "Cost:", cost_val, "\nPrediction:\n", hy_val)
#20001번 학습중 1000단위마다 코스트값, 예측값을 출력함

predict = sess.run(hypothesis,feed_dict={X:[[25,48]]}) #온도값, 습도값입력
print("예상값",int(predict[0]))
#학습된 직선에 내가 예상하고싶은 x데이터를 넣어 예상값을 출력

firebase.post('예측값 log',int(predict[0]))