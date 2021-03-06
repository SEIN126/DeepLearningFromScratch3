# -*- coding: utf-8 -*-
"""step07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UEsua-Bh6uwo_JU2S-iGnAnyXkSB84M3

#Step7 역전파 자동화

## 7.1 역전파 자동화의 시작
"""

import numpy as np

class Variable:
  '''
    - 이 variable을 만들어 준 함수(func : creator)를 지정해줌
    -> define-by-run을 위해서 이 variable이 생성(forward)됨과 동시에
       backward를 위한 func를 연결해주는 역할을 함.
  '''
  def __init__(self, data):
    self.data = data
    self.grad = None
    self.creator = None
  
  def set_creator(self, func):
    self.creator = func

class Function:
  '''
    - output 저장
    - output이 생성됨과 동시에 creator와 연결
  '''
  def __call__(self, input):
    x = input.data
    y = self.forward(x)  
    output = Variable(y)

    output.set_creator(self) # 출력 변수가 생성됨과 동시에 creator를 설정(생성과 동시에 '연결')
    
    self.input = input
    self.output= output # 출력도 저장
    return output

  def forward(self, x):
    raise NotImplementedError()

  def backward(self, gy):
    raise NotImplementedError()

class Square(Function):
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

A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# 계산 그래프를 거꾸로 올라감
'''
assert ... : ...에 조건문이 들어가는데, 이 조건문이 True가 아니면 예외 발생!
'''
assert y.creator == C
assert y.creator.input == b
assert y.creator.input.creator == B
assert y.creator.input.creator.input == a
assert y.creator.input.creator.input.creator == A
assert y.creator.input.creator.input.creator.input == x
# 예외 처리 없이 모두 수행 완료! -> 모두 정상적으로 연결됨을 확인!
# 이 연결은 모두 계산을 수행하는 시점(forward run)에 만들어짐. => define by run
# 결국 링크드 리스트와 비슷한 구조가 됨

"""## 7.2 역전파 도전!"""

y.grad = np.array(1.0)

C = y.creator # 함수를 y와 연결
b = C.input   # 함수의 입력과 연결
b.grad = C.backward(y.grad) # 함수의 backward 메서드를 호출한다

B = b.creator
a = B.input
a.grad = B.backward(b.grad)

A = a.creator
x = A.input
x.grad = A.backward(a.grad)
print(x.grad) # 3.297442541400256

"""## 7.3 backward 메서드 추가"""

class Variable:
  '''
    - 이 variable을 만들어 준 함수(func : creator)를 지정해줌
    -> define-by-run을 위해서 이 variable이 생성(forward)됨과 동시에
       backward를 위한 func를 연결해주는 역할을 함.
  '''
  def __init__(self, data):
    self.data = data
    self.grad = None
    self.creator = None
  
  def set_creator(self, func):
    self.creator = func

  def backward(self):
    '''
      - 앞에 있는 변수들 grad를 재귀적으로 구해보자
    '''
    f = self.creator  # 현재 변수의 creator를 불러옴
    if f is not None: 
      x = f.input     # creator의 input을 가져온다
                      # 이미 다 연결이 되어있기 때문에 가져올 수 있음
      x.grad = f.backward(self.grad)  # creator의 backward를 통해 
                                      # creator의 input의 grad를 구할 수 있음
      x.backward()   # 이 동작을 재귀적으로 수행

A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# 역전파
y.grad = np.array(1.0)
y.backward()
print(x.grad) # 3.297442541400256