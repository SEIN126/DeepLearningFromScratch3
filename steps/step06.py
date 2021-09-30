# -*- coding: utf-8 -*-
"""step06.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1osB9TTmswphjcf6Qd-tKAhlo4iSW6g98

#Step6 수동 역전파

## 6.1 Variable 클래스 추가 구현
"""

import numpy as np

class Variable:
  '''
    - gradient까지 Variable에 저장
  '''
  def __init__(self, data):
    self.data = data
    self.grad = None

"""##6.2 Function 클래스 추가 구현"""

class Function:
  '''
    - 미분을 계산하는 역전파(backward 메서드)
    - forward 메서드 호출 시 건네받은 variable 인스턴스 유지
  '''
  def __call__(self, input):
    x = input.data
    y = self.forward(x)  # 구체적인 계산은 forward method에서 함.
    output = Variable(y)
    self.input = input
    return output

  def forward(self, x):
    raise NotImplementedError()

  def backward(self, gy):
    raise NotImplementedError()

"""## 6.3 Square와 Exp 클래스 추가 구현"""

class Square(Function):
  '''
    - backward 까지 구현
  '''
  def forward(self, x):
    y = x ** 2
    return y

  def backward(self, gy):
    x = self.input.data
    gx = 2 * x * gy
    return gx

class Exp(Function):
  def forward(self, x):
    y = np.exp(x)
    return y

  def backward(self, gy):
    x = self.input.data
    gx = np.exp(x) * gy
    return gx

"""## 6.4 역전파 구현"""

A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# 수동으로 역전파 과정 구현
y.grad = 1
b.grad = C.backward(y.grad)
a.grad = B.backward(b.grad)
x.grad = A.backward(a.grad)
print(x.grad)